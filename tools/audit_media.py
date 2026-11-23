"""Read-only inventory of the authorized public Drive folder and page references.
Run: python tools/audit_media.py
Never modifies Drive or downloads original media. Python standard library only.
"""
import csv
import json
import re
import urllib.request
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FOLDER_ID = '1Fqf4PVjly0UXCLWEN4zByLekWpJAmOPk'
OUT = ROOT / 'audit' / 'current'  # Never overwrite the committed historical snapshot.

class FolderParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.entries = []
        self.current = None
        self.in_title = False
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'div' and 'flip-entry' in a.get('class', '').split():
            self.current = {'id': a['id'].removeprefix('entry-'), 'name': '', 'url': ''}
            self.entries.append(self.current)
        if self.current and tag == 'a' and not self.current['url']:
            self.current['url'] = a.get('href', '')
        if tag == 'div' and 'flip-entry-title' in a.get('class', '').split():
            self.in_title = True
    def handle_data(self, data):
        if self.in_title and self.current:
            self.current['name'] += data
    def handle_endtag(self, tag):
        if tag == 'div':
            self.in_title = False

def get(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'MareaMediaAudit/1.0'})
    return urllib.request.urlopen(req, timeout=40)

def inventory():
    rows, visited = [], set()
    def visit(folder, path):
        if folder in visited:
            return
        visited.add(folder)
        with get(f'https://drive.google.com/embeddedfolderview?id={folder}') as response:
            text = response.read().decode('utf-8')
        parser = FolderParser()
        parser.feed(text)
        if not parser.entries and 'folder' not in text.lower():
            raise RuntimeError(f'Unrecognized listing for {folder}')
        print(f'{path}: {len(parser.entries)} entries', flush=True)
        for entry in parser.entries:
            entry['folder'] = path
            entry['parentId'] = folder
            entry['isFolder'] = '/drive/folders/' in entry['url']
            rows.append(entry)
            if entry['isFolder']:
                visit(entry['id'], path + '/' + entry['name'].strip())
    visit(FOLDER_ID, 'Fotitos importantes')
    return rows

def references(source):
    # New static magazine has an explicit, verified-only publication manifest.
    manifest = re.search(r'<script\b[^>]*\bid="published-photos"[^>]*>(.*?)</script>', source, re.S)
    if manifest:
        rows = json.loads(manifest[1])
        if any(r.get('reviewStatus') != 'verified' or r.get('mediaType') != 'photo' for r in rows):
            raise ValueError('Publication manifest must contain verified photographs only')
        return [{'id': r['sourceId'], 'name': r['originalName'], 'category': r['primaryCategory'], 'kind': 'photo'} for r in rows]
    # Retain the parser for historical three-chapter HTML snapshots.
    refs = []
    for m in re.finditer(r"\{\s*id:\s*'([^']+)',\s*name:\s*'([^']+)'", source):
        pos = m.start()
        category = 'sensorial' if pos < source.index('const agostoPhotos') else 'agosto' if pos < source.index('const driveVideos') else 'videos'
        if category == 'videos':
            end = source.find('localUrl:', pos)
            block = source[pos:end]
            category = 'sensorial' if "chapter: 'Taller Sensorial'" in block else 'agosto'
        refs.append({'id': m[1], 'name': m[2], 'category': category, 'kind': 'video' if m[2].lower().endswith('.mov') else 'photo'})
    return refs

def check_thumbnail(ref):
    if ref['kind'] != 'photo':
        return {'id': ref['id'], 'status': 'not-tested-video'}
    url = f"https://drive.google.com/thumbnail?id={ref['id']}&sz=w1200"
    try:
        with get(url) as response:
            content_type = response.headers.get('Content-Type', '')
            data = response.read()
            return {'id': ref['id'], 'status': response.status, 'contentType': content_type, 'bytes': len(data), 'validImageResponse': content_type.startswith('image/') and len(data) > 0}
    except Exception as exc:
        return {'id': ref['id'], 'status': 'error', 'error': str(exc), 'validImageResponse': False}

def main():
    OUT.mkdir(exist_ok=True)
    rows = inventory()
    refs = references((ROOT / 'index.html').read_text(encoding='utf-8'))
    by_id = {r['id']: r for r in refs}
    by_name = defaultdict(list)
    for ref in refs:
        by_name[ref['name'].casefold()].append(ref)
    media = [r for r in rows if not r['isFolder']]
    for item in media:
        exact = by_id.get(item['id'])
        same_name = by_name.get(item['name'].casefold(), [])
        folder = item['folder'].lower()
        folder_cat = 'sensorial' if folder.endswith('/taller sensorial') else 'agosto' if folder.endswith('/clase 31 agosto') else 'cangrejos' if folder.endswith('/clase cangrejos') else ''
        item['category'] = folder_cat or (exact['category'] if exact else same_name[0]['category'] if same_name else 'pending-review')
        item['categoryEvidence'] = 'source-folder' if folder_cat else 'page-id' if exact else 'same-filename-candidate-not-content-verified' if same_name else 'none'
        item['usedByPage'] = bool(exact)
        item['pageNameMatches'] = bool(exact and exact['name'] == item['name'])
        item['sameNamePageIds'] = ';'.join(r['id'] for r in same_name if r['id'] != item['id'])
        item['proposedName'] = (item['category'] + '--' + item['name']) if item['category'] != 'pending-review' else item['name']
    checks = list(ThreadPoolExecutor(max_workers=4).map(check_thumbnail, refs))
    ids = {r['id'] for r in media}
    summary = {
        'checkedAt': datetime.now(timezone.utc).isoformat(),
        'sourceFolderId': FOLDER_ID,
        'listingMethod': 'public embeddedfolderview, recursive; no visible pagination controls; public visibility only',
        'visibleFolders': sum(r['isFolder'] for r in rows),
        'visibleMedia': len(media),
        'mediaByFolder': dict(Counter(r['folder'] for r in media)),
        'mediaByCategory': dict(Counter(r['category'] for r in media)),
        'pageReferences': len(refs),
        'pagePhotos': sum(r['kind'] == 'photo' for r in refs),
        'pageVideos': sum(r['kind'] == 'video' for r in refs),
        'missingPageIds': [r['id'] for r in refs if r['id'] not in ids],
        'notReferencedByPage': sum(not r['usedByPage'] for r in media),
        'validThumbnailResponses': sum(bool(r.get('validImageResponse')) for r in checks),
        'thumbnailErrors': [r for r in checks if r.get('validImageResponse') is False],
        'limitations': ['Same filename does not prove duplicate contents.', 'Caption accuracy has not been visually verified.', 'HTTP image response is not an end-to-end browser rendering test.', 'Video playback not tested.', 'Public listings do not establish whether inaccessible files exist.']
    }
    for name, obj in [('inventory.json', rows), ('page-references.json', refs), ('thumbnail-checks.json', checks), ('summary.json', summary)]:
        (OUT / name).write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    fields = ['name', 'id', 'folder', 'category', 'categoryEvidence', 'proposedName', 'usedByPage', 'pageNameMatches', 'sameNamePageIds', 'url']
    with (OUT / 'media-catalog.csv').open('w', newline='', encoding='utf-8-sig') as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, extrasaction='ignore')
        writer.writeheader()
        writer.writerows(media)
    print(json.dumps(summary, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
