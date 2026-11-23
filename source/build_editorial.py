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
    rows = json.loads((ROOT/'audit/thematic-catalog.json').read_text(encoding='utf-8'))
    photos = [r for r in rows if r['mediaType']=='photo' and r['reviewStatus']=='verified']
    assert len(photos)==58 and len({r['sourceId'] for r in photos})==58
    cover = next(r for r in photos if r['sourceId']=='1jMeLokjKWlpVlkg_X67NqsVLP9nFM-QV')
    spans = ['sm:col-span-2 lg:row-span-2', '', '', 'lg:row-span-2', '', 'sm:col-span-2', '', '']
    for i, axis in enumerate(AXES,1):
        selected = [r for r in photos if r['primaryCategory']==axis]
        payload = [{'id':r['sourceId'], 'caption':r['visualDescription'], 'originalName':r['originalName'], 'primaryCategory':r['primaryCategory'], 'span':spans[n%len(spans)]} for n,r in enumerate(selected)]
        pattern = rf'(c{i}: \{{.*?photos: )\[.*?\](,\s*cards:)'
        text, count = re.subn(pattern, lambda m:m[1]+json.dumps(payload,ensure_ascii=False)+m[2],text,count=1,flags=re.S)
        assert count==1
    text = re.sub(r'videos: \[.*?\]', 'videos: []',text,flags=re.S)
    text = text.replace('1r4OYEQtf00TzGKc7I8qH2Dg-lIHsKg9o',cover['sourceId'])
    text = text.replace('alt="Portada editorial Marea & Azotea"', 'alt="'+escape(cover['visualDescription'],quote=True)+'"')
    text = text.replace('>78</span>', '>58</span>').replace('>18</span>', '>0</span>').replace('Memorias en Video</span>','Videos publicados</span>').replace('1 / 78','1 / 58')
    counts = iter([29,15,5,9,0])
    text = re.sub(r'\d+ fotos · \d+ videos',lambda m:f'{next(counts)} fotos · 0 videos',text)
    text = re.sub(r'\d+ registros audiovisuales', '0 videos publicados · revisión pendiente', text)
    text = re.sub(r'<!-- Mosaico Visual Editorial.*?-->', '<!-- Mosaico: selección verified + cápsulas editoriales -->',text)
    text = re.sub(r'<!-- Franja Memorias en Movimiento.*?-->', '<!-- Archivo audiovisual pendiente de revisión -->',text)
    text = text.replace('img.parentElement.querySelector(', 'img.parentElement?.querySelector(')
    text = text.replace('78 FOTOS ÚNICAS + 18 VIDEOS','58 IDS VERIFIED; VIDEOS PENDIENTES')
    text = text.replace('Algunas fotografías se muestran en modo reserva. Asegúrate de que la carpeta compartida en Google Drive esté configurada como <em>"Cualquier persona con el enlace · Lector"</em>.','Algunas vistas previas no están disponibles. Puede deberse a la conexión, al servicio o al acceso al archivo; el enlace a Drive permite comprobarlo.')
    text = text.replace('Activa el acceso público en Google Drive o ábrela directamente desde el enlace.','Vista previa no disponible: comprueba la conexión, el servicio o el acceso mediante el enlace a Drive.')
    note = '''<aside id="editorial-scope" class="mt-8 rounded-3xl bg-arena p-6 text-sm text-carbon leading-relaxed"><strong>Sobre esta edición.</strong> Las crónicas, las cápsulas y las 44 voces del glosario se conservan del material editorial aportado, con sus créditos originales a Aida Arteaga. No se presentan como citas transcritas ni revisión científica verificada. Los pies fotográficos son independientes: reproducen lo observable del catálogo, sin certificar recetas, especies, procedencias ni identidades. Se publican 58 IDs verified (puede haber escenas repetidas); quedan fuera 91 fotos provisionales, 32 por revisión humana y 31 MOV no inspeccionados. Portada: '''+escape(cover['originalName'])+'''.</aside>'''
    pos = text.index('        <!-- Tarjeta de Firma Editorial -->')
    idx = text[:pos].rfind('        </div>')
    text = text[:idx]+note+'\n'+text[idx:]
    start = text.index('    function buildChronicle(key)')
    end = text.index('    // =========================================================================',start)
    text = text[:start]+(ROOT/'source/chronicle-renderer.js').read_text(encoding='utf-8')+'\n\n'+text[end:]
    manifest = [{k:r[k] for k in ('sourceId','originalName','primaryCategory','visualDescription','mediaType','reviewStatus')} for r in photos]
    text = text.replace('  <script>\n    // =========================================================================', '<script id="published-photos" type="application/json">'+json.dumps(manifest,ensure_ascii=False).replace('<','\\u003c')+'</script>\n  <script>\n    // =========================================================================',1)
    text = text.replace('${query}', '${escapeHTML(query)}')
    behavior = (ROOT/'source/accessibility.js').read_text(encoding='utf-8')
    text = text.replace('</body>','<script>\n'+behavior+'\n</script>\n<noscript><p>Los mosaicos y el glosario interactivo requieren JavaScript. Las crónicas se pueden leer sin él.</p></noscript>\n</body>')
    extra = (ROOT/'source/standalone.css').read_text(encoding='utf-8')
    text = text.replace('</head>','<style id="editorial-refinements">'+extra+'</style>\n</head>')
    if not runtime:
        css = (ROOT/'source/tailwind.generated.css').read_text(encoding='utf-8')
        text = re.sub(r'  <!-- Tailwind CSS CDN -->.*?</script>\s*<!-- Configuración.*?</script>',lambda m:'<style id="compiled-tailwind">'+css+'</style>', text,count=1,flags=re.S)
        assert 'cdn.tailwindcss.com' not in text
    target = ROOT/('source/build-runtime.html' if runtime else 'index.html')
    target.write_text(text,encoding='utf-8',newline='\n')
    print(f'Built {target.name}: 58 verified IDs, five original chronicles, 44 glossary entries; runtime={runtime}')

if __name__=='__main__':
    build('--runtime' in sys.argv)
