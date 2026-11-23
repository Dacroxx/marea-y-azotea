"""Read-only thumbnail evidence and reproducible thematic catalogue. No originals.
Commands: python tools/thematic_media.py prepare | build | validate
Human observations live in audit/thematic-observations.json; never infer from filenames.
Evidence is local in ../visual-evidence (not publishable, not tracked by git).
"""
import csv
import hashlib
import io
import json
import sys
import unicodedata
import re
import urllib.request
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from datetime import datetime, timezone
from PIL import Image, ImageOps, ImageDraw, ImageFont
ROOT = Path(__file__).resolve().parents[1]
LOCAL = ROOT.parent / 'visual-evidence'
CATEGORIES = [
'Territorio, Saberes y Herramientas Ancestrales',
'Hierbas de Azotea y Aromas de la Selva',
'Frutos del Mar, Río y Manglar',
'Coco, Tubérculos y Fogón',
'Bebidas, Cultura Viva e Identidad']
def load(path):
    return json.loads(path.read_text(encoding='utf-8'))
def save(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
def media():
    return [r for r in load(ROOT/'audit/inventory.json') if not r['isFolder']]
def prepare():
    LOCAL.mkdir(exist_ok=True)
    items = media()
    items.sort(key=lambda r:(r['name'].lower().endswith('.mov'), r['folder'], r['name'], r['id']))
    def fetch(pair):
        i, r = pair
        path = LOCAL / 'thumbs' / (r['id']+'.jpg')
        path.parent.mkdir(exist_ok=True)
        result = dict(sourceId=r['id'], originalName=r['name'], mediaType='video' if r['name'].lower().endswith('.mov') else 'photo', number=i+1, sheet=f'sheet-{i//16+1:02}.jpg', cell=i%16+1)
        try:
            if not path.exists():
                req=urllib.request.Request(f"https://drive.google.com/thumbnail?id={r['id']}&sz=w640", headers={'User-Agent':'MareaThematicAudit/1.0'})
                with urllib.request.urlopen(req, timeout=35) as res:
                    data=res.read()
                    if not res.headers.get('Content-Type','').startswith('image/'):
                        raise ValueError('Not image response')
                with Image.open(io.BytesIO(data)) as im:
                    im.verify()
                path.write_bytes(data)
            data=path.read_bytes()
            result.update(thumbnailSha256=hashlib.sha256(data).hexdigest(), thumbnailPath=str(path), status='downloaded')
        except Exception as e:
            result.update(status='error',error=str(e))
        return result
    rows=list(ThreadPoolExecutor(max_workers=8).map(fetch,enumerate(items)))
    save(LOCAL/'map.json',rows)
    try: font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',16)
    except OSError: font=ImageFont.load_default()
    for start in range(0,len(rows),16):
        sheet=Image.new('RGB',(1600,1640),'#eeeeee')
        d=ImageDraw.Draw(sheet)
        for j,r in enumerate(rows[start:start+16]):
            x,y=(j%4)*400,(j//4)*410
            if r['status']=='downloaded':
                with Image.open(r['thumbnailPath']) as im:
                    im=ImageOps.contain(ImageOps.exif_transpose(im).convert('RGB'),(390,342))
                    sheet.paste(im,(x+(400-im.width)//2,y+(342-im.height)//2))
            d.text((x+6,y+346),f"{r['number']:03} / celda {j+1} / {r['originalName']}",font=font,fill='black')
            d.text((x+6,y+370),r['sourceId'],font=font,fill='black')
            d.text((x+6,y+390),r['mediaType']+' / '+r['status'],font=font,fill='black')
        sheet.save(LOCAL/rows[start]['sheet'],quality=94)
    # Public inventory comparison is separate; never overwrite baseline.
    import audit_media
    current=audit_media.inventory()
    old={r['id']:r for r in load(ROOT/'audit/inventory.json')}
    new={r['id']:r for r in current}
    save(LOCAL/'inventory-comparison.json',dict(checkedAt=datetime.now(timezone.utc).isoformat(),added=sorted(new.keys()-old.keys()),removed=sorted(old.keys()-new.keys()),changed=[k for k in old.keys()&new.keys() if any(old[k].get(f)!=new[k].get(f) for f in ['name','folder','isFolder'])],visibleMedia=sum(not r['isFolder'] for r in current)))
    print(Counter(r['status'] for r in rows))
def slug(text):
    text=unicodedata.normalize('NFKD',text).encode('ascii','ignore').decode().lower()
    return re.sub('[^a-z0-9]+','-',text).strip('-')[:100]
def build():
    evidence=load(LOCAL/'map.json')
    observations=[]
    for path in sorted((ROOT/'audit').glob('thematic-observations*.tsv')):
        with path.open(encoding='utf-8',newline='') as f:
            for r in csv.DictReader(f,delimiter='\t'):
                observations.append(dict(number=int(r['number']),category=int(r['category']),secondary=[int(c) for c in r['secondary'].split(',') if c],status=r['status'],confidence=r['confidence'],label=r['label'],description=r['description']))
    originals={r['number']:r for r in observations}
    for target,source in load(ROOT/'audit/thematic-visual-matches.json')['matches'].items():
        observations.append(dict(originals[source],number=int(target)))
    for o in observations:
        o['inspection']='Miniatura estática de MOV examinada; vídeo y audio NO reproducidos.' if o['number']>181 else 'Foto examinada visualmente en hoja de contacto, orden de lectura izquierda-derecha y arriba-abajo.'
    observations.sort(key=lambda r:r['number'])
    save(ROOT/'audit/thematic-observations.json',observations)
    assert len(observations)==len({r['number'] for r in observations})
    assert {r['number'] for r in observations}=={r['number'] for r in evidence}
    assert all(0<=o['category']<=5 and all(1<=c<=5 for c in o['secondary']) for o in observations)
    obs={r['number']:r for r in observations}
    rows=[]
    for e in evidence:
        base=next(r for r in media() if r['id']==e['sourceId'])
        o=obs[e['number']]
        cat=o['category']
        rows.append(dict(sourceId=base['id'],originalName=base['name'],sourceFolder=base['folder'],mediaType=e['mediaType'],primaryCategory=CATEGORIES[cat-1] if cat else None,secondaryCategories=[CATEGORIES[c-1] for c in o.get('secondary',[])],visualDescription=o['description'],proposedFilename=slug(o['label'])+'--'+base['id'][:12]+Path(base['name']).suffix,evidence=dict(sheet=e['sheet'],cell=e['cell'],number=e['number'],thumbnailSha256=e.get('thumbnailSha256'),inspection=o['inspection'],localEvidenceDirectory='../visual-evidence'),confidence=o['confidence'],reviewStatus=o['status']))
    save(ROOT/'audit/thematic-catalog.json',rows)
    with (ROOT/'audit/thematic-catalog.csv').open('w',encoding='utf-8-sig',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]))
        writer.writeheader()
        for r in rows:
            writer.writerow({k:json.dumps(v,ensure_ascii=False) if isinstance(v,(dict,list)) else v for k,v in r.items()})
    summary=dict(total=len(rows),byMediaType=dict(Counter(r['mediaType'] for r in rows)),byPrimaryCategory=dict(Counter(r['primaryCategory'] or 'null' for r in rows)),byStatus=dict(Counter(r['reviewStatus'] for r in rows)),byConfidence=dict(Counter(r['confidence'] for r in rows)))
    hashes=defaultdict(list)
    for e in evidence:
        if e.get('thumbnailSha256'): hashes[e['thumbnailSha256']].append(e['sourceId'])
    summary['identicalThumbnailGroups']=[dict(thumbnailSha256=k,sourceIds=v) for k,v in hashes.items() if len(v)>1]
    summary['inventoryComparison']=load(LOCAL/'inventory-comparison.json')
    save(ROOT/'audit/thematic-summary.json',summary)
    lines=['# Informe de curaduría temática','',
    'Fuente base: fork https://github.com/Dacroxx/marea-y-azotea, dev 678392e9a285d16288e03a395b2f25459d06761d. Inventario anterior preservado sin cambios. Fuente visual: miniaturas públicas del Drive autorizado, no nombres ni captions. Sin escrituras en Drive, push, despliegue ni modificación de la web.',
    '', '## Método y límites', '',
    'Se examinaron visualmente 181 fotos y 31 miniaturas estáticas de MOV mediante 14 hojas de contacto (16 celdas/hoja; última hoja 4). El contenido temporal y audio de los 31 MOV NO se reprodujo: todos conservan categoría null y uninspected-video. Las descripciones de vídeo se refieren únicamente a la miniatura. No se identifican personas, etnias, festividades, especies concretas ni recetas por asociación. Una categoría culinaria amplia no confirma coco, variedad de hierba ni nombre de plato. Las escenas genéricas sin sujeto temático suficiente quedan null.',
    '', 'verified confirma el sujeto visual y su eje amplio, no autenticidad ancestral ni procedencia. provisional propone un eje con incertidumbre; no es autorización para publicarlo como hecho. confidence mide fuerza de la asignación temática, no calidad de la receta. Los vídeos tienen none por no evaluar su contenido completo.',
    '', '## Conteos calculados', '', '```json',json.dumps(summary,ensure_ascii=False,indent=2),'```',
    '', 'Los grupos por SHA-256 indican bytes idénticos de miniatura descargada; NO prueban que originales sean idénticos. Ningún ID fue eliminado o fusionado. Previsualizaciones parecidas con hashes diferentes no se declaran duplicados.',
    '', '## Preguntas específicas para David / revisión', '',
    'Los grupos siguientes son preguntas, no afirmaciones. Se listan todos los IDs pendientes, sin convertirlos en una sexta categoría. Ver descripción por ID en el catálogo.']
    groups=defaultdict(list)
    for r in rows:
        if r['reviewStatus']=='uninspected-video': question='¿Puede revisarse el MOV (imagen completa y audio) antes de asignar tema? La miniatura no basta.'
        elif r['primaryCategory'] is None: question='¿Qué ingrediente, objeto, lectura o actividad aparece y a qué eje pertenece? La imagen sola no permite asignación.'
        elif r['reviewStatus']=='provisional': question='¿Se confirma este eje y qué ingredientes/actividad concreta aparecen? Propuesta: '+r['primaryCategory']
        else: continue
        groups[question].append(r)
    for question,group in groups.items():
        lines+=['','### '+question,'']
        for r in group:
            lines.append('- '+r['sourceId']+' — '+r['originalName']+' — '+r['visualDescription'])
    lines+=['','## Reproducibilidad y evidencia local','',
    'Desde el clon: `python tools/thematic_media.py prepare` descarga solo miniaturas w640, genera hojas/mapa y registra comparación pública aparte; no sobrescribe audit/inventory.json. `python tools/thematic_media.py build` expande anotaciones TSV y coincidencias visuales documentadas, genera CSV/JSON/resumen/informe y valida. `python tools/thematic_media.py validate` no usa red. `python -m unittest discover -s tests -p "test*.py"` ejecuta pruebas.',
    '', 'Las hojas y miniaturas SOLO se conservan localmente en '+str(LOCAL)+'. map.json contiene número/ID/hoja/celda/hash/ruta. Son material privado de revisión: NO adjuntar ni subir imágenes a GitHub. Los catálogos incluyen trazabilidad, no archivos de imagen. Las coincidencias descriptivas de thematic-visual-matches.json se anotaron tras observar cada celda; no equivalen a duplicación de originales.',
    '', '## Fuera de alcance','', 'No se cambió index.html, categorías de la página, Drive ni archivos del clon compartido. proposedFilename conserva extensión y añade los primeros 12 caracteres del ID; es solo propuesta. El catálogo reemplaza la clasificación por fecha únicamente como entregable, no aplica cambios a la web. No hay afirmación de reparación de carga. Requiere revisión sustantiva por david-reviewer antes de integración.']
    (ROOT/'audit/THEMATIC-REPORT.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    print(json.dumps(summary,ensure_ascii=False,indent=2))
    validate()
def validate(rows=None):
    if rows is None: rows=load(ROOT/'audit/thematic-catalog.json')
    base=media()
    assert len(rows)==len(base)==212
    assert len({r['sourceId'] for r in rows})==212
    assert {r['sourceId'] for r in rows}=={r['id'] for r in base}
    assert len({r['proposedFilename'].casefold() for r in rows})==212
    by_id={r['id']:r for r in base}
    evidence_by_id={r['sourceId']:r for r in load(LOCAL/'map.json')}
    for r in rows:
        b=by_id[r['sourceId']]
        e=evidence_by_id[r['sourceId']]
        assert r['mediaType']==e['mediaType']==('video' if b['name'].lower().endswith('.mov') else 'photo')
        assert all(r['evidence'][k]==e[k] for k in ['sheet','cell','number','thumbnailSha256'])
        assert (LOCAL/e['sheet']).is_file()
        assert hashlib.sha256(Path(e['thumbnailPath']).read_bytes()).hexdigest()==e['thumbnailSha256']
        assert r['originalName']==b['name'] and r['sourceFolder']==b['folder']
        assert '--'+r['sourceId'][:12] in r['proposedFilename']
        assert Path(r['proposedFilename']).suffix==Path(b['name']).suffix
        assert r['primaryCategory'] is None or r['primaryCategory'] in CATEGORIES
        assert all(c in CATEGORIES and c!=r['primaryCategory'] for c in r['secondaryCategories'])
        assert r['reviewStatus'] in ['verified','provisional','needs-human','uninspected-video','out-of-scope']
        assert r['confidence'] in ['high','medium','low','none']
        assert len(r['secondaryCategories'])==len(set(r['secondaryCategories']))
        if r['reviewStatus']=='verified': assert r['primaryCategory'] is not None and r['confidence']=='high'
        if r['reviewStatus']=='needs-human': assert r['primaryCategory'] is None
        assert r['visualDescription'] and r['evidence']['inspection']
        assert 1<=r['evidence']['cell']<=16
        if r['mediaType']=='video': assert r['reviewStatus']=='uninspected-video' and r['primaryCategory'] is None and not r['secondaryCategories'] and r['confidence']=='none'
    with (ROOT/'audit/thematic-catalog.csv').open(encoding='utf-8-sig',newline='') as f:
        csvrows=list(csv.DictReader(f))
    assert len(csvrows)==len(rows)
    for a,b in zip(csvrows,rows):
        for k,v in b.items():
            if isinstance(v,(list,dict)): assert json.loads(a[k])==v
            else: assert a[k]==('' if v is None else str(v))
    print('VALIDATED: 212 IDs, exact coverage, taxonomy, extensions, unique names, CSV/JSON parity')
if __name__=='__main__':
    {'prepare':prepare,'build':build,'validate':validate}[sys.argv[1]]()
