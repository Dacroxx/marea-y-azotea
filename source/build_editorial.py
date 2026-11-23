"""Faithful reference adaptation. Build offline; refresh CSS separately with Chrome."""
import hashlib
import json
import re
import sys
from html import escape
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
SOURCE_SHA256 = '7bd51e2854517647430d5d64a197a49d230a8298027c76c9a2daf6c4dfaa3c15'
AXES = ['Territorio, Saberes y Herramientas Ancestrales', 'Hierbas de Azotea y Aromas de la Selva', 'Coco, Tubérculos y Fogón', 'Frutos del Mar, Río y Manglar', 'Bebidas, Cultura Viva e Identidad']

def build(runtime=False):
    source = ROOT/'source/editorial-template.html'
    assert hashlib.sha256(source.read_bytes()).hexdigest() == SOURCE_SHA256, 'Review source provenance before changing its checksum'
    text = source.read_text(encoding='utf-8')
    photos = json.loads((ROOT/'audit/curated-selection.json').read_text(encoding='utf-8'))
    videos_path = ROOT/'audit/curated-videos.json'
    videos = json.loads(videos_path.read_text(encoding='utf-8')) if videos_path.exists() else []
    total_photos = len(photos)
    total_videos = len(videos)
    assert total_photos > 0 and len({r['sourceId'] for r in photos}) == total_photos
    cover = next((r for r in photos if r.get('isCover')), photos[0])
    spans = ['sm:col-span-2 lg:row-span-2', '', '', 'lg:row-span-2', '', 'sm:col-span-2', '', '']
    vid_styles = [
        ('bg-selva text-coco', 'bg-platano text-carbon'),
        ('bg-marea text-coco', 'bg-platano text-carbon'),
        ('bg-achiote text-coco', 'bg-coco text-achiote'),
        ('bg-carbon text-coco', 'bg-platano text-carbon'),
    ]
    chron_photo_counts = []
    chron_video_counts = []
    for i, axis in enumerate(AXES, 1):
        ckey = f'c{i}'
        selected = [r for r in photos if r['chronicle'] == ckey]
        selected_vids = [v for v in videos if v['chronicle'] == ckey]
        chron_photo_counts.append(len(selected))
        chron_video_counts.append(len(selected_vids))
        payload = [{'id': r['sourceId'], 'caption': f"[{r['code']}] {r['visualDescription']}", 'originalName': r['curatedFileName'], 'primaryCategory': r['primaryCategory'], 'span': spans[n % len(spans)]} for n, r in enumerate(selected)]
        pattern = rf'({ckey}: \{{.*?photos: )\[.*?\](,\s*cards:)'
        text, count = re.subn(pattern, lambda m: m[1] + json.dumps(payload, ensure_ascii=False) + m[2], text, count=1, flags=re.S)
        assert count == 1
        vid_payload = [
            {
                'id': v['sourceId'],
                'title': f"[{v['code']}] {v['title']}",
                'subtitle': v.get('subtitle', ''),
                'cardBg': vid_styles[n % len(vid_styles)][0],
                'badgeBg': vid_styles[n % len(vid_styles)][1],
            }
            for n, v in enumerate(selected_vids)
        ]
        v_pattern = rf'({ckey}: \{{.*?videos: )\[.*?\](.*?\}})'
        text, v_count = re.subn(v_pattern, lambda m: m[1] + json.dumps(vid_payload, ensure_ascii=False) + m[2], text, count=1, flags=re.S)
        assert v_count == 1

    text = text.replace('1r4OYEQtf00TzGKc7I8qH2Dg-lIHsKg9o', cover['sourceId'])
    text = text.replace('alt="Portada editorial Marea & Azotea"', 'alt="' + escape(cover['visualDescription'], quote=True) + '"')
    text = text.replace('>78</span>', f'>{total_photos}</span>').replace('>18</span>', f'>{total_videos}</span>').replace('Memorias en Video</span>', 'Videos publicados</span>').replace('1 / 78', f'1 / {total_photos}')
    p_iter = iter(chron_photo_counts)
    v_iter = iter(chron_video_counts)
    text = re.sub(r'\d+ fotos · \d+ videos', lambda m: f'{next(p_iter)} fotos · {next(v_iter)} videos', text)
    vr_iter = iter(chron_video_counts)
    text = re.sub(r'\d+ registros audiovisuales', lambda m: (lambda c: f'{c} videos publicados' if c > 0 else '0 videos publicados · 29 en carpeta de revisión')(next(vr_iter)), text)
    text = text.replace('Espiritualidad, Fiesta y Ética Culinaria', 'Bitácora de Brigada, Cultura Viva y Ética Culinaria')
    text = re.sub(r'<!-- Mosaico Visual Editorial.*?-->', '<!-- Mosaico: selección curada sin duplicados + cápsulas editoriales -->', text)
    text = re.sub(r'<!-- Franja Memorias en Movimiento.*?-->', '<!-- Archivo audiovisual en revisión (carpeta 06 en Drive) -->', text)
    text = text.replace('img.parentElement.querySelector(', 'img.parentElement?.querySelector(')
    text = text.replace('78 FOTOS ÚNICAS + 18 VIDEOS', f'{total_photos} FOTOS CURADAS · {total_videos} VIDEOS')
    text = text.replace('Algunas fotografías se muestran en modo reserva. Asegúrate de que la carpeta compartida en Google Drive esté configurada como <em>"Cualquier persona con el enlace · Lector"</em>.', 'Algunas vistas previas no están disponibles. Puede deberse a la conexión, al servicio o al acceso al archivo; el enlace a Drive permite comprobarlo.')
    text = text.replace('Activa el acceso público en Google Drive o ábrela directamente desde el enlace.', 'Vista previa no disponible: comprueba la conexión, el servicio o al acceso mediante el enlace a Drive.')
    counts_desc = ', '.join(f'{c}' for c in chron_photo_counts)
    note = f'''<aside id="editorial-scope" class="mt-8 rounded-3xl bg-arena p-6 text-sm text-carbon leading-relaxed"><strong>Sobre esta edición.</strong> Las crónicas, las cápsulas y las 44 voces del glosario se conservan del material editorial aportado, con sus créditos originales a Aida Arteaga. Esta selección publica <strong>{total_photos} fotografías curadas y deduplicadas</strong> ({counts_desc} por crónica) y <strong>{total_videos} videos publicados</strong>, excluyendo tomas repetidas o de aula con celulares. Portada: ''' + escape(cover['curatedFileName']) + '''.</aside>'''
    pos = text.index('        <!-- Tarjeta de Firma Editorial -->')
    idx = text[:pos].rfind('        </div>')
    text = text[:idx] + note + '\n' + text[idx:]
    start = text.index('    function buildChronicle(key)')
    end = text.index('    // =========================================================================', start)
    text = text[:start] + (ROOT/'source/chronicle-renderer.js').read_text(encoding='utf-8') + '\n\n' + text[end:]
    manifest = [{k: r[k] for k in ('code', 'sourceId', 'curatedFileName', 'originalName', 'primaryCategory', 'visualDescription')} for r in photos]
    text = text.replace('  <script>\n    // =========================================================================', '<script id="published-photos" type="application/json">' + json.dumps(manifest, ensure_ascii=False).replace('<', '\\u003c') + '</script>\n  <script>\n    // =========================================================================', 1)
    text = text.replace('${query}', '${escapeHTML(query)}')
    behavior = (ROOT/'source/accessibility.js').read_text(encoding='utf-8')
    text = text.replace('</body>', '<script>\n' + behavior + '\n</script>\n<noscript><p>Los mosaicos y el glosario interactivo requieren JavaScript. Las crónicas se pueden leer sin él.</p></noscript>\n</body>')
    extra = (ROOT/'source/standalone.css').read_text(encoding='utf-8')
    text = text.replace('</head>', '<style id="editorial-refinements">' + extra + '</style>\n</head>')
    if not runtime:
        css = (ROOT/'source/tailwind.generated.css').read_text(encoding='utf-8')
        text = re.sub(r'  <!-- Tailwind CSS CDN -->.*?</script>\s*<!-- Configuración.*?</script>', lambda m: '<style id="compiled-tailwind">' + css + '</style>', text, count=1, flags=re.S)
        assert 'cdn.tailwindcss.com' not in text
    target = ROOT/('source/build-runtime.html' if runtime else 'index.html')
    target.write_text(text, encoding='utf-8', newline='\n')
    print(f'Built {target.name}: {total_photos} curated photos, {total_videos} videos, five chronicles, 44 glossary entries; runtime={runtime}')

if __name__=='__main__':
    build('--runtime' in sys.argv)
