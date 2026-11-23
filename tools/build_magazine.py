"""Build the static magazine from verified photographs only. Standard library.
Run from any directory: python tools/build_magazine.py
Does not edit the catalog, download images, or deduplicate source records.
"""
import json
from html import escape as e
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AXES = [
    ('territorio', 'Territorio y herramientas', 'Territorio, Saberes y Herramientas Ancestrales', 'Objetos, materiales y gestos', 'Recipientes, utensilios y plátanos abren una lectura de los objetos y los gestos visibles. Las imágenes no establecen por sí solas el origen ni la historia de cada herramienta.'),
    ('hierbas', 'Hierbas y aromas', 'Hierbas de Azotea y Aromas de la Selva', 'Acercarse a lo aromático', 'Hojas, picado y mezclas: una mirada a sus formas y a su preparación. Los pies conservan los límites de lo observado, sin atribuir especies a partir de una imagen.'),
    ('mar', 'Mar, río y manglar', 'Frutos del Mar, Río y Manglar', 'Mirar de cerca', 'El registro permite observar crustáceos y su manipulación. No basta para determinar especies, lugares de captura ni nombres de recetas.'),
    ('fogon', 'Coco y fogón', 'Coco, Tubérculos y Fogón', 'Alrededor de la preparación', 'Esta selección reúne registros vinculados al eje del fogón. El título es una puerta temática, no una confirmación de que cada preparación contenga coco o tubérculos.'),
    ('cultura', 'Bebidas e identidad', 'Bebidas, Cultura Viva e Identidad', 'Una página por construir', 'Este eje forma parte de la revista, pero aún no tiene fotografías con estado verified en el catálogo. Preferimos dejar visible esta ausencia antes que completar el relato con atribuciones sin confirmar.'),
]


def thumb(row, size=640):
    return f'https://drive.google.com/thumbnail?id={row["sourceId"]}&sz=w{size}'


def photo(row, cover=False):
    return f'''<figure class="{'cover-photo' if cover else 'photo-card'}" data-source-id="{e(row['sourceId'])}" data-category="{e(row['primaryCategory'])}">
    <button class="image-open" type="button" data-open="{e(row['sourceId'])}" aria-label="Ampliar {e(row['originalName'])}">
      <img src="{e(thumb(row,1200 if cover else 640))}" alt="{e(row['visualDescription'])}" loading="{'eager' if cover else 'lazy'}" {'fetchpriority="high"' if cover else ''} width="800" height="600">
      <span class="image-fallback" hidden>Vista previa no disponible.<br>Puede deberse a la conexión, al servicio o al acceso al archivo.<br>Abre el enlace a Drive para comprobarlo.</span>
      <span class="zoom-hint" aria-hidden="true">Ampliar ↗</span>
    </button>
    <figcaption><span class="photo-category">{e(row['primaryCategory'])}</span><p class="description">{e(row['visualDescription'])}</p>
      <div class="file-line"><span class="original-name">{e(row['originalName'])}</span><a href="https://drive.google.com/file/d/{e(row['sourceId'])}/view" target="_blank" rel="noopener noreferrer">Ver en Drive ↗</a></div>
    </figcaption></figure>'''


def build():
    catalog = json.loads((ROOT/'audit/thematic-catalog.json').read_text(encoding='utf-8'))
    photos = [r for r in catalog if r['reviewStatus'] == 'verified' and r['mediaType'] == 'photo']
    assert len({r['sourceId'] for r in photos}) == len(photos)
    assert all(r['primaryCategory'] in [a[2] for a in AXES] for r in photos)
    by_axis = {a[0]: [r for r in photos if r['primaryCategory']==a[2]] for a in AXES}
    cover = next(r for r in photos if r['sourceId']=='1jMeLokjKWlpVlkg_X67NqsVLP9nFM-QV')
    nav = ''.join(f'<a href="#{a[0]}">{e(a[1])}</a>' for a in AXES)
    contents = ''.join(f'<li><a href="#{a[0]}"><span>{e(a[2])}</span><span class="index-count">{len(by_axis[a[0]])} fotos ↗</span></a></li>' for a in AXES)
    sections = []
    for axis in AXES:
        slug, short, title, lead, intro = axis
        rows = by_axis[slug]
        # One opening image per axis; the complete selection appears only in the gallery.
        image = photo(rows[0]) if rows else '<div class="empty-state"><span class="empty-mark" aria-hidden="true">—</span><h3>Sin selección fotográfica por ahora</h3><p>0 fotos verified. Las propuestas y los registros pendientes siguen en el catálogo de auditoría; no se publican aquí.</p><a href="audit/thematic-catalog.json">Consultar el catálogo completo ↗</a></div>'
        sections.append(f'''<section id="{slug}" class="axis {'dark-axis' if slug in ('hierbas','fogon') else ''}" data-axis="{slug}" aria-labelledby="title-{slug}"><div class="wrap axis-layout"><div class="axis-copy"><span class="folio">{len(rows)} fotos en la selección</span><h2 id="title-{slug}">{e(title)}</h2><p class="section-lead">{e(lead)}</p><p>{e(intro)}</p><a class="text-link" data-gallery-filter="{slug}" href="#galeria">Ver este eje en la galería →</a></div><div class="axis-image">{image}</div></div></section>''')
    filters = '<button type="button" data-filter="all" aria-pressed="true">Todas <span>'+str(len(photos))+'</span></button>' + ''.join(f'<button type="button" data-filter="{a[0]}" aria-pressed="false">{e(a[1])} <span>{len(by_axis[a[0]])}</span></button>' for a in AXES)
    payload = [{k:r[k] for k in ('sourceId','originalName','primaryCategory','visualDescription','mediaType','reviewStatus')} for r in photos]
    html = f'''<!doctype html>
<html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>MAREA &amp; AZOTEA · Cocinas del Pacífico</title><meta name="description" content="Una revista visual de las Cocinas del Pacífico: cinco ejes y una selección fotográfica con descripciones trazables al catálogo.">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,500;0,700;0,900;1,400;1,600&family=Plus+Jakarta+Sans:wght@400;500;600;700&family=Space+Mono:wght@400;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/magazine.css"><script src="assets/magazine.js" defer></script></head>
<body><a class="skip-link" href="#editorial">Saltar al contenido</a>
<header class="site-header"><a class="brand" href="#portada" aria-label="Marea y Azotea, portada">M<span>&amp;</span>A</a><nav aria-label="Cinco ejes temáticos">{nav}</nav><a class="archive-link" href="#galeria">Galería ↗</a></header>
<main><section id="portada" class="cover"><div class="wrap"><div class="edition"><span>Edición temática · Archivo visual</span><span>Cocinas del Pacífico colombiano</span></div><h1>MAREA <em>&amp;</em> AZOTEA</h1><div class="cover-layout"><div class="cover-copy"><p class="kicker">Entre la selva y la marea</p><p class="cover-title">Un territorio.<br>Cinco miradas.</p><p>Una revista para recorrer las cocinas del Pacífico desde sus objetos, sus materiales y los gestos que la cámara alcanza a guardar.</p><a class="primary-link" href="#editorial">Abrir la revista ↓</a><p class="cover-note">{len(photos)} registros fotográficos seleccionados.<br>Descripciones de lo visible, sin completar lo incierto.</p></div>{photo(cover,True)}</div><div class="cover-bottom"><span>Herramientas · Aromas · Aguas · Fogón · Identidad</span><a href="#galeria">Explorar las fotografías →</a></div></div></section>
<section id="editorial" class="editorial wrap"><div><span class="kicker">Carta editorial</span><h2>Primero mirar.<br><em>Después, contar.</em></h2><p class="drop-cap">Una fotografía puede acercarnos a una textura, a una herramienta o a una mano trabajando. No siempre puede decirnos el nombre de un plato, la especie de una hoja o la historia de una preparación.</p><p>Esta edición organiza una selección revisada en cinco ejes. Publicamos únicamente los {len(photos)} registros de fotos con estado <code>verified</code> del catálogo: ese estado indica un sujeto visible y un encaje temático amplio; no certifica recetas, procedencias ni identidades.</p><p>Las propuestas provisionales, las dudas y los videos sin inspeccionar quedan fuera de esta selección. El archivo completo sigue disponible para consulta, separado de la revista.</p><a class="text-link" href="audit/thematic-catalog.json">Consultar catálogo completo (212 registros) ↗</a><p class="small-note">Se cuentan archivos por ID, sin deduplicarlos por nombre ni por semejanza visual. Puede haber escenas repetidas.</p></div><aside aria-label="Sumario editorial"><h3>En esta edición</h3><ol>{contents}</ol><a class="text-link" href="#galeria">Galería de la selección →</a></aside></section>
{''.join(sections)}
<section id="galeria" class="gallery wrap" aria-labelledby="gallery-title"><div class="gallery-heading"><div><span class="kicker">Archivo de la edición</span><h2 id="gallery-title">Mirar con tiempo</h2><p>La selección completa. Abre una imagen para ampliar el registro y consultar su archivo original.</p></div><button id="print-button" type="button">Imprimir / PDF</button></div><div class="filters" role="group" aria-label="Filtrar fotografías por eje">{filters}</div><p id="gallery-count" role="status" aria-live="polite">{len(photos)} de {len(photos)} fotografías · Todas</p><p class="print-note">La impresión incluye la selección completa, aunque haya un filtro activo en pantalla. Se usa el diálogo de impresión del navegador; no se guarda una revista editable.</p><p id="gallery-empty" class="empty-state" hidden>No hay fotografías publicadas en este eje. Las propuestas siguen en el <a href="audit/thematic-catalog.json">catálogo de auditoría</a>.</p><div id="archive-grid">{''.join(photo(r) for r in photos)}</div></section>
</main><footer><div class="wrap"><p class="footer-brand">MAREA <em>&amp;</em> AZOTEA</p><p>Cocinas del Pacífico · Una lectura visual abierta a revisión.</p><a href="audit/TAXONOMY.md">Criterios de lectura</a> · <a href="audit/thematic-catalog.json">Catálogo de auditoría</a><p class="small-note">Las imágenes se solicitan a Drive. Su disponibilidad puede variar. No se alojan originales en esta revista.</p><a href="#portada">Volver a la portada ↑</a></div></footer>
<dialog id="lightbox" aria-labelledby="lightbox-name" aria-describedby="lightbox-description"><div class="lightbox-toolbar"><span id="lightbox-count"></span><button id="lightbox-close" aria-label="Cerrar visor">Cerrar ×</button></div><div class="lightbox-media"><img id="lightbox-image" src="{e(thumb(cover,1200))}" alt="{e(cover['visualDescription'])}" hidden><p id="lightbox-fallback" hidden>Vista previa no disponible. Puede deberse a la conexión, al servicio o al acceso al archivo. Usa el enlace a Drive para comprobarlo.</p></div><div class="lightbox-caption"><p id="lightbox-category"></p><h2 id="lightbox-name"></h2><p id="lightbox-description"></p><a id="lightbox-drive" target="_blank" rel="noopener noreferrer">Ver archivo en Drive ↗</a></div><div class="lightbox-controls"><button id="lightbox-prev" aria-label="Fotografía anterior">← Anterior</button><span>Teclas ← → · Esc para cerrar</span><button id="lightbox-next" aria-label="Fotografía siguiente">Siguiente →</button></div></dialog>
<script id="published-photos" type="application/json">{json.dumps(payload,ensure_ascii=False).replace('<','\\u003c')}</script>
<noscript><p class="wrap">Puedes recorrer las cinco secciones y la galería sin JavaScript. Para ampliar imágenes utiliza los enlaces a Drive; los filtros y el visor necesitan JavaScript.</p></noscript></body></html>'''
    (ROOT/'index.html').write_text(html+'\n',encoding='utf-8')
    print(f'Built index.html: {len(photos)} verified photo records; '+', '.join(f'{a[0]}={len(by_axis[a[0]])}' for a in AXES))

if __name__ == '__main__':
    build()
