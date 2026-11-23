"""Faithful reference adaptation. Build offline; refresh CSS separately with Chrome."""
import hashlib
import json
import re
import sys
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE_SHA256 = '7bd51e2854517647430d5d64a197a49d230a8298027c76c9a2daf6c4dfaa3c15'
AXES = [
    'Territorio, Saberes y Herramientas Ancestrales',
    'Hierbas de Azotea y Aromas de la Selva',
    'Coco, Tubérculos y Fogón',
    'Frutos del Mar, Río y Manglar',
    'Bebidas, Cultura Viva e Identidad',
]

CUSTOM_LOGO_SVG = (
    '<span class="w-10 h-10 rounded-full bg-selva text-platano flex items-center justify-center shadow-sm '
    'group-hover:bg-marea transition-colors" aria-hidden="true">'
    '<svg class="w-6 h-6" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">'
    '<path d="M5 20C8.5 17 12.5 17 16 20C19.5 23 23.5 23 27 20" stroke="#E9B44C" stroke-width="2.4" stroke-linecap="round"/>'
    '<path d="M7 24.5C10 22.5 13 22.5 16 24.5C19 26.5 22 26.5 25 24.5" stroke="#FAF6EE" stroke-width="1.8" stroke-linecap="round" stroke-opacity="0.85"/>'
    '<path d="M16 15.5C16 10.5 19.5 6.5 24.5 6.5C24.5 11.5 21 15.5 16 15.5Z" fill="#E9B44C"/>'
    '<path d="M16 15.5C16 11 12.5 7.5 8 7.5C8 12 11.5 15.5 16 15.5Z" fill="#FAF6EE" fill-opacity="0.9"/>'
    '</svg></span>'
)


def build_videos_section(videos):
    groups = [
        ('Taller Sensorial y Maíz', 'c1', 'bg-selva text-coco', 'bg-platano text-carbon'),
        ('Refrito y Soasado de Hoja', 'c2', 'bg-achiote text-coco', 'bg-coco text-achiote'),
        ('Arroz con Coco y Fufú', 'c3', 'bg-marea text-coco', 'bg-platano text-carbon'),
        ('Camarón al Fogón', 'c4', 'bg-carbon text-coco', 'bg-platano text-carbon'),
    ]
    blocks = []
    for title, ckey, card_bg, badge_bg in groups:
        grp_vids = [v for v in videos if v['chronicle'] == ckey]
        if not grp_vids:
            continue
        cards = []
        for v in grp_vids:
            vurl = f"https://drive.google.com/file/d/{v['sourceId']}/view"
            cards.append(
                f'<a href="{vurl}" target="_blank" rel="noopener noreferrer" '
                f'class="group rounded-3xl p-6 shadow-md hover:-translate-y-1 hover:shadow-xl transition-all flex flex-col justify-between {card_bg}">'
                f'<div class="flex items-center justify-between gap-2">'
                f'<span class="px-3 py-1 rounded-full text-[11px] font-bold uppercase tracking-widest {badge_bg}">{escape(v["code"])}</span>'
                f'<span class="text-xs opacity-75 group-hover:opacity-100">Ver en Drive ↗</span>'
                f'</div>'
                f'<div class="mt-5">'
                f'<h4 class="font-editorial font-bold text-lg leading-snug">{escape(v["driveName"])}</h4>'
                f'<p class="text-xs opacity-85 mt-2 leading-relaxed">{escape(v["title"])}</p>'
                f'</div>'
                f'</a>'
            )
        blocks.append(
            f'<div class="mt-10">'
            f'<h3 class="font-editorial font-bold text-2xl text-marea mb-4">{escape(title)}</h3>'
            f'<div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">{"".join(cards)}</div>'
            f'</div>'
        )

    return f'''
  <!-- ===================================================================== -->
  <!-- SECCIÓN AUDIOVISUAL · VIDEOS EN SECUENCIA                             -->
  <!-- ===================================================================== -->
  <section id="videos-eje" class="py-20 sm:py-28 bg-coco border-b border-selva/15">
    <div class="max-w-7xl mx-auto px-5 sm:px-8">
      <div class="max-w-3xl reveal">
        <span class="px-4 py-1.5 rounded-full bg-marea text-platano text-xs font-bold uppercase tracking-widest">Archivo Audiovisual</span>
        <h2 class="mt-4 font-editorial font-black text-4xl sm:text-5xl text-marea leading-[1.06]">
          Videos de Clase en Secuencia
        </h2>
        <p class="mt-4 text-base sm:text-lg text-carbon/80 leading-relaxed">
          Registros audiovisuales de las prácticas en cocina ordenados por secuencia de preparación ({len(videos)} videos seleccionados).
        </p>
      </div>
      {"".join(blocks)}
    </div>
  </section>
'''


def build(runtime=False):
    source = ROOT / 'source/editorial-template.html'
    assert hashlib.sha256(source.read_bytes()).hexdigest() == SOURCE_SHA256, 'Review source provenance before changing its checksum'
    text = source.read_text(encoding='utf-8')
    photos = json.loads((ROOT / 'audit/curated-selection.json').read_text(encoding='utf-8'))
    videos_path = ROOT / 'audit/curated-videos.json'
    videos = json.loads(videos_path.read_text(encoding='utf-8')) if videos_path.exists() else []
    total_photos = len(photos)
    total_videos = len(videos)
    assert total_photos > 0 and len({r['sourceId'] for r in photos}) == total_photos
    cover = next((r for r in photos if r.get('isCover')), photos[0])
    spans = ['sm:col-span-2 lg:row-span-2', '', '', 'lg:row-span-2', '', 'sm:col-span-2', '', '']

    # Map 4 curated photo axes into c1, c2, c3 (combined Fogon+Mar), and c5 (Eje IV Brigada/Cultura), keeping c4 empty/hidden
    grouped = {
        'c1': [r for r in photos if r['chronicle'] == 'c1'],
        'c2': [r for r in photos if r['chronicle'] == 'c2'],
        'c3': [r for r in photos if r['chronicle'] in ('c3', 'c4')],
        'c4': [],
        'c5': [r for r in photos if r['chronicle'] == 'c5'],
    }

    for i in range(1, 6):
        ckey = f'c{i}'
        selected = grouped[ckey]
        payload = [
            {
                'id': r['sourceId'],
                'caption': f"[{r['code']}] {r['visualDescription']}",
                'originalName': r['curatedFileName'],
                'primaryCategory': r['primaryCategory'],
                'span': spans[n % len(spans)],
            }
            for n, r in enumerate(selected)
        ]
        pattern = rf'({ckey}: \{{.*?photos: )\[.*?\](,\s*cards:)'
        text, count = re.subn(pattern, lambda m: m[1] + json.dumps(payload, ensure_ascii=False) + m[2], text, count=1, flags=re.S)
        assert count == 1

    text = re.sub(r'videos: \[.*?\]', 'videos: []', text, flags=re.S)

    # Cambio #1: Logo SVG propio en lugar de la "M" en círculo verde
    text = re.sub(
        r'<span class="w-9 h-9 rounded-full bg-selva text-platano[^>]*>\s*M\s*</span>',
        CUSTOM_LOGO_SVG,
        text,
        count=1,
    )

    # Cambio #2: Cintillo de portada
    text = text.replace('<span>Crónica de Aida Arteaga</span>', '<span>Crónica Estudiantes Cocina del Pacífico 2026-2</span>')

    # Portada y contadores globales
    text = text.replace('1r4OYEQtf00TzGKc7I8qH2Dg-lIHsKg9o', cover['sourceId'])
    text = text.replace('alt="Portada editorial Marea & Azotea"', 'alt="' + escape(cover['visualDescription'], quote=True) + '"')
    text = text.replace('>78</span>', f'>{total_photos}</span>').replace('>18</span>', f'>{total_videos}</span>').replace('Memorias en Video</span>', 'Videos en Secuencia</span>').replace('1 / 78', f'1 / {total_photos}')
    text = text.replace('78 FOTOS ÚNICAS + 18 VIDEOS', f'{total_photos} FOTOS CURADAS · {total_videos} VIDEOS')

    # Navegación superior y menú móvil alineados a 4 Ejes + Videos + Glosario
    old_nav = '''      <nav class="hidden lg:flex items-center gap-5 text-xs font-semibold uppercase tracking-wider text-carbon/80">
        <a href="#cronica-1" class="hover:text-selva transition-colors">I. Territorio</a>
        <a href="#cronica-2" class="hover:text-achiote transition-colors">II. Azotea</a>
        <a href="#cronica-3" class="hover:text-chontaduro transition-colors">III. Coco &amp; Fogón</a>
        <a href="#cronica-4" class="hover:text-marea transition-colors">IV. Mar &amp; Manglar</a>
        <a href="#cronica-5" class="hover:text-achiote transition-colors">V. Cultura Viva</a>
        <a href="#glosario" class="px-3 py-1.5 rounded-full bg-selva/10 text-selva hover:bg-selva hover:text-coco transition-colors">Glosario</a>
      </nav>'''
    new_nav = '''      <nav class="hidden lg:flex items-center gap-5 text-xs font-semibold uppercase tracking-wider text-carbon/80">
        <a href="#cronica-1" class="hover:text-selva transition-colors">I. Taller Sensorial</a>
        <a href="#cronica-2" class="hover:text-achiote transition-colors">II. Azotea</a>
        <a href="#cronica-3" class="hover:text-chontaduro transition-colors">III. Fogón, Mar &amp; Mesa</a>
        <a href="#cronica-5" class="hover:text-marea transition-colors">IV. Brigada &amp; Cultura</a>
        <a href="#videos-eje" class="hover:text-achiote transition-colors">Videos</a>
        <a href="#glosario" class="px-3 py-1.5 rounded-full bg-selva/10 text-selva hover:bg-selva hover:text-coco transition-colors">Glosario</a>
      </nav>'''
    assert old_nav in text
    text = text.replace(old_nav, new_nav, 1)

    old_mobile = '''    <div id="mobile-menu" class="hidden lg:hidden bg-coco border-t border-selva/15 px-4 py-4 space-y-1 text-xs font-semibold uppercase tracking-wider">
      <a href="#editorial" class="block py-2.5 px-3 rounded-xl hover:bg-arena text-marea">Carta Editorial e Índice</a>
      <a href="#cronica-1" class="block py-2.5 px-3 rounded-xl hover:bg-arena text-selva">I · Territorio y Herramientas Ancestrales</a>
      <a href="#cronica-2" class="block py-2.5 px-3 rounded-xl hover:bg-arena text-achiote">II · Hierbas de Azotea y Aromas de la Selva</a>
      <a href="#cronica-3" class="block py-2.5 px-3 rounded-xl hover:bg-arena text-chontaduro">III · Coco, Tubérculos y Fogón</a>
      <a href="#cronica-4" class="block py-2.5 px-3 rounded-xl hover:bg-arena text-marea">IV · Frutos del Mar, Río y Manglar</a>
      <a href="#cronica-5" class="block py-2.5 px-3 rounded-xl hover:bg-arena text-achiote">V · Bebidas, Cultura Viva e Identidad</a>
      <a href="#glosario" class="block py-2.5 px-3 rounded-xl bg-selva/10 text-selva">Glosario Interactivo del Pacífico</a>
    </div>'''
    new_mobile = '''    <div id="mobile-menu" class="hidden lg:hidden bg-coco border-t border-selva/15 px-4 py-4 space-y-1 text-xs font-semibold uppercase tracking-wider">
      <a href="#editorial" class="block py-2.5 px-3 rounded-xl hover:bg-arena text-marea">Reflexión e Índice</a>
      <a href="#cronica-1" class="block py-2.5 px-3 rounded-xl hover:bg-arena text-selva">I · Taller Sensorial y Saberes</a>
      <a href="#cronica-2" class="block py-2.5 px-3 rounded-xl hover:bg-arena text-achiote">II · Azotea, Aromas y Mise en Place</a>
      <a href="#cronica-3" class="block py-2.5 px-3 rounded-xl hover:bg-arena text-chontaduro">III · Fogón, Mar y Mesa del Pacífico</a>
      <a href="#cronica-5" class="block py-2.5 px-3 rounded-xl hover:bg-arena text-marea">IV · Bitácora de Brigada y Cultura Viva</a>
      <a href="#videos-eje" class="block py-2.5 px-3 rounded-xl hover:bg-arena text-achiote">Archivo Audiovisual en Secuencia</a>
      <a href="#glosario" class="block py-2.5 px-3 rounded-xl bg-selva/10 text-selva">Glosario del Pacífico</a>
    </div>'''
    assert old_mobile in text
    text = text.replace(old_mobile, new_mobile, 1)

    # Cambio #3: Dejar solo el texto en la tarjeta de reflexión (quitar "Nota de la Autora" y firma/nombre de abajo)
    old_aside = '''        <!-- Tarjeta de Firma Editorial -->
        <aside class="lg:col-span-5 reveal">
          <div class="rounded-3xl bg-selva text-coco p-8 sm:p-10 shadow-xl relative overflow-hidden">
            <div class="absolute -right-8 -top-8 w-40 h-40 rounded-full bg-platano/15 pointer-events-none"></div>
            <span class="text-[11px] font-bold uppercase tracking-[0.22em] text-platano">Nota de la Autora</span>
            <p class="mt-4 font-fraunces italic text-xl sm:text-2xl leading-snug text-coco/95">
              “En el fogón del Pacífico descubrimos que el sabor nunca es un accidente técnico: es paisaje, es canto, es resistencia y es mesa compartida.”
            </p>
            <div class="mt-6 pt-5 border-t border-coco/20 flex items-center justify-between gap-4">
              <div>
                <p class="font-editorial font-bold text-lg text-platano">Aida Arteaga</p>
                <p class="text-xs text-coco/75">Gastronomía y Artes Culinarias · PUJ Cali</p>
              </div>
              <span class="w-11 h-11 rounded-full bg-achiote text-coco flex items-center justify-center font-editorial font-bold text-lg">A</span>
            </div>
          </div>
        </aside>'''
    new_aside = '''        <!-- Tarjeta de Reflexión -->
        <aside class="lg:col-span-5 reveal">
          <div class="rounded-3xl bg-selva text-coco p-8 sm:p-10 shadow-xl relative overflow-hidden">
            <div class="absolute -right-8 -top-8 w-40 h-40 rounded-full bg-platano/15 pointer-events-none"></div>
            <p class="font-fraunces italic text-xl sm:text-2xl leading-snug text-coco/95">
              “En el fogón del Pacífico descubrimos que el sabor no es un accidente técnico: es territorio, oficio y mesa compartida.”
            </p>
          </div>
        </aside>'''
    assert old_aside in text
    text = text.replace(old_aside, new_aside, 1)

    # Depurar lenguaje exagerado/romantizado en la introducción y mapa de lectura
    text = text.replace(
        'Esta revista nace del asombro compartido en la cátedra de <strong>Cocinas del Pacífico</strong> de la Pontificia Universidad Javeriana Cali. Más que un recetario académico, estas páginas condensan una memoria sensorial: el peso sereno de la',
        'Esta bitácora reúne el registro de las prácticas de la asignatura <strong>Cocinas del Pacífico</strong> de la Pontificia Universidad Javeriana Cali. Más allá de un recetario, documenta el trabajo directo con ingredientes y utensilios: el uso de la',
    )
    text = text.replace(
        'el perfume verde e indomable de la',
        'el aroma fresco de las hierbas de',
    )
    text = text.replace(
        'la paciencia de estrujar la',
        'la extracción manual de la',
    )
    text = text.replace(
        'y el orgullo con el que cada preparación cuenta la historia de un litoral entero.',
        'y el diálogo técnico con las preparaciones tradicionales del litoral.',
    )
    text = text.replace(
        'Organizamos nuestro archivo en cinco crónicas temáticas que dialogan entre sí. Cada capítulo entrelaza fotografía documental, memorias en movimiento y voces reales recogidas en el aula para honrar a las cocineras tradicionales, a las comunidades afrodescendientes e indígenas del Pacífico y a la responsabilidad ética que asumimos como futuros gastrónomos.',
        'Organizamos esta bitácora en cuatro ejes temáticos y una sección audiovisual en secuencia, integrando las fotografías de clase, los registros de cocina y las voces recogidas durante el semestre.',
    )
    text = text.replace('Cinco Crónicas del Litoral', 'Cuatro Ejes y Archivo Audiovisual')
    text = text.replace('Selecciona cualquier capítulo para sumergirte en sus crónicas, mosaicos fotográficos y memorias en video.', 'Selecciona un eje para recorrer las fotografías de clase o ve directamente a la sección de videos en secuencia.')

    # Actualizar las 5 tarjetas del Mapa de Lectura con los conteos reales y la nueva estructura
    c1_n, c2_n, c3_n, c5_n = len(grouped['c1']), len(grouped['c2']), len(grouped['c3']), len(grouped['c5'])
    text = text.replace('18 fotos · 4 videos', f'{c1_n} fotos')
    text = text.replace('15 fotos · 3 videos', f'{c2_n} fotos', 1)
    text = text.replace('15 fotos · 4 videos', f'{c3_n} fotos', 1)
    text = text.replace('15 fotos · 4 videos', f'{c5_n} fotos', 1)
    text = text.replace('15 fotos · 3 videos', f'{total_videos} videos', 1)

    text = text.replace(
        '<h4 class="font-editorial font-bold text-xl leading-snug group-hover:text-platano transition-colors">Mar, Río y Manglar</h4>\n              <p class="text-xs text-coco/80 mt-2">Piangüeras, bocana, cangrejos, jaiba y biodiversidad.</p>',
        '<h4 class="font-editorial font-bold text-xl leading-snug group-hover:text-platano transition-colors">Brigada y Cultura Viva</h4>\n              <p class="text-xs text-coco/80 mt-2">Trabajo en equipo, libros de consulta y tradición oral.</p>',
    )
    text = text.replace('href="#cronica-4"', 'href="#cronica-5"')
    text = text.replace(
        '<h4 class="font-editorial font-bold text-xl leading-snug group-hover:text-carbon transition-colors">Bebidas y Cultura Viva</h4>\n              <p class="text-xs text-coco/90 mt-2">Viche, cantos de cocina, San Pacho y pueblos originarios.</p>',
        '<h4 class="font-editorial font-bold text-xl leading-snug group-hover:text-carbon transition-colors">Videos en Secuencia</h4>\n              <p class="text-xs text-coco/90 mt-2">Taller sensorial, maíz, refrito, arroz con coco, fufú y camarón.</p>',
    )
    text = text.replace('href="#cronica-5" class="group rounded-3xl p-6 bg-chontaduro', 'href="#videos-eje" class="group rounded-3xl p-6 bg-chontaduro')
    text = text.replace('Coco, Tubérculos y Fogón</h4>', 'Fogón, Mar y Mesa</h4>')

    # Actualizar encabezados de Crónica III (unifica Fogón + Mar), ocultar Crónica IV vacía, y alinear Crónica V como Eje IV
    text = text.replace(
        '<h2 class="font-editorial font-black text-4xl sm:text-6xl text-carbon leading-[1.04]">\n          Coco, Tubérculos y Fogón\n        </h2>',
        '<h2 class="font-editorial font-black text-4xl sm:text-6xl text-carbon leading-[1.04]">\n          Fogón, Mar y Mesa del Pacífico\n        </h2>',
    )
    text = text.replace('<article id="cronica-4"', '<article id="cronica-4" class="hidden"')
    text = text.replace('>Crónica V</span>', '>Eje IV</span>')
    text = text.replace('Espiritualidad, Fiesta y Ética Culinaria', 'Bitácora de Brigada, Cultura Viva y Ética Culinaria')
    text = text.replace(
        '<h2 class="font-editorial font-black text-4xl sm:text-6xl text-marea leading-[1.04]">\n          Bebidas, Cultura Viva e Identidad\n        </h2>',
        '<h2 class="font-editorial font-black text-4xl sm:text-6xl text-marea leading-[1.04]">\n          Bitácora de Brigada y Cultura Viva\n        </h2>',
    )

    # Cambio #5: Quitar por completo las franjas de Memorias en Movimiento dentro de las crónicas e insertar sección propia antes del Glosario
    text = re.sub(
        r'\s*<!-- Franja Memorias en Movimiento.*?<div id="videos-c\d"[^>]*></div>\s*</div>',
        '',
        text,
        flags=re.S,
    )
    text = text.replace('  <!-- ===================================================================== -->\n  <!-- 6. GLOSARIO INTERACTIVO', build_videos_section(videos) + '\n  <!-- ===================================================================== -->\n  <!-- 6. GLOSARIO INTERACTIVO', 1)

    # Cambio #6: Footer -> Aida Arteaga y David González
    text = text.replace(
        '<p class="font-editorial font-bold text-xl text-coco mt-1">Aida Arteaga</p>',
        '<p class="font-editorial font-bold text-xl text-coco mt-1">Aida Arteaga y David González</p>',
    )

    # Limpieza de textos técnicos/avisos
    text = text.replace('img.parentElement.querySelector(', 'img.parentElement?.querySelector(')
    text = text.replace('Algunas fotografías se muestran en modo reserva. Asegúrate de que la carpeta compartida en Google Drive esté configurada como <em>"Cualquier persona con el enlace · Lector"</em>.', 'Algunas vistas previas no están disponibles. Puede deberse a la conexión, al servicio o al acceso al archivo; el enlace a Drive permite comprobarlo.')
    text = text.replace('Activa el acceso público en Google Drive o ábrela directamente desde el enlace.', 'Vista previa no disponible: comprueba la conexión, el servicio o el acceso mediante el enlace a Drive.')

    # Cambio #4: NO insertar #editorial-scope ("Sobre esta edición...")
    start = text.index('    function buildChronicle(key)')
    end = text.index('    // =========================================================================', start)
    text = text[:start] + (ROOT / 'source/chronicle-renderer.js').read_text(encoding='utf-8') + '\n\n' + text[end:]
    manifest = [{k: r[k] for k in ('code', 'sourceId', 'curatedFileName', 'originalName', 'primaryCategory', 'visualDescription')} for r in photos]
    text = text.replace('  <script>\n    // =========================================================================', '<script id="published-photos" type="application/json">' + json.dumps(manifest, ensure_ascii=False).replace('<', '\\u003c') + '</script>\n  <script>\n    // =========================================================================', 1)
    text = text.replace('${query}', '${escapeHTML(query)}')
    behavior = (ROOT / 'source/accessibility.js').read_text(encoding='utf-8')
    text = text.replace('</body>', '<script>\n' + behavior + '\n</script>\n<noscript><p>Los mosaicos y el glosario interactivo requieren JavaScript. Las crónicas se pueden leer sin él.</p></noscript>\n</body>')
    extra = (ROOT / 'source/standalone.css').read_text(encoding='utf-8')
    text = text.replace('</head>', '<style id="editorial-refinements">' + extra + '</style>\n</head>')
    if not runtime:
        css = (ROOT / 'source/tailwind.generated.css').read_text(encoding='utf-8')
        text = re.sub(r'  <!-- Tailwind CSS CDN -->.*?</script>\s*<!-- Configuración.*?</script>', lambda m: '<style id="compiled-tailwind">' + css + '</style>', text, count=1, flags=re.S)
        assert 'cdn.tailwindcss.com' not in text
    target = ROOT / ('source/build-runtime.html' if runtime else 'index.html')
    target.write_text(text, encoding='utf-8', newline='\n')
    print(f'Built {target.name}: {total_photos} curated photos, {total_videos} videos in dedicated section, 4 axes + videos, 44 glossary entries; runtime={runtime}')


if __name__ == '__main__':
    build('--runtime' in sys.argv)
