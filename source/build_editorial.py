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
    ]
    blocks = []
    for title, ckey, card_bg, badge_bg in groups:
        grp_vids = [v for v in videos if v['chronicle'] == ckey]
        if not grp_vids:
            continue
        cards = []
        dots = []
        for idx, v in enumerate(grp_vids):
            vprev = f"https://drive.google.com/file/d/{v['sourceId']}/preview"
            vtitle = v.get('displayTitle', v['driveName'])
            active_cls = ' is-active' if idx == 0 else ''
            cards.append(
                f'<article class="video-slide rounded-3xl p-4 sm:p-5 shadow-md flex flex-col justify-between {card_bg}{active_cls}" data-slide-index="{idx}" data-video-src="{vprev}">'
                f'<div class="w-full rounded-2xl overflow-hidden bg-carbon/80" style="aspect-ratio: 16 / 9; min-height: 210px;">'
                f'<iframe src="{vprev}" title="{escape(vtitle)}" loading="lazy" allow="autoplay; fullscreen" allowfullscreen style="width: 100%; height: 100%; min-height: 210px; border: 0;"></iframe>'
                f'</div>'
                f'<div class="mt-4 flex items-center justify-between gap-2">'
                f'<span class="px-3 py-1 rounded-full text-[11px] font-bold uppercase tracking-widest {badge_bg}">{escape(v["code"])}</span>'
                f'</div>'
                f'<div class="mt-3">'
                f'<h4 class="font-editorial font-bold text-lg leading-snug">{escape(vtitle)}</h4>'
                f'<p class="text-xs opacity-85 mt-1.5 leading-relaxed">{escape(v["title"])}</p>'
                f'</div>'
                f'</article>'
            )
            dots.append(
                f'<button type="button" class="video-dot{active_cls}" data-dot-index="{idx}" aria-label="Ir al video {idx + 1}: {escape(vtitle)}"></button>'
            )
        blocks.append(
            f'<div class="mt-12 video-group" data-video-group="{ckey}">'
            f'<div class="flex flex-wrap items-center justify-between gap-4 mb-4">'
            f'<h3 class="font-editorial font-bold text-2xl text-marea">{escape(title)}</h3>'
            f'<div class="flex items-center gap-2">'
            f'<span class="video-counter text-xs font-bold uppercase tracking-widest text-carbon/70 mr-2">1 / {len(grp_vids)}</span>'
            f'<button type="button" class="video-nav-btn video-prev" aria-label="Video anterior de {escape(title)}" disabled>←</button>'
            f'<button type="button" class="video-nav-btn video-next" aria-label="Siguiente video de {escape(title)}">→</button>'
            f'</div>'
            f'</div>'
            f'<div class="video-carousel-viewport">'
            f'<div class="video-carousel-track" role="region" aria-roledescription="carrusel" aria-label="{escape(title)}" tabindex="0">{"".join(cards)}</div>'
            f'</div>'
            f'<div class="video-dots flex items-center justify-center gap-2 mt-4">{"".join(dots)}</div>'
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
          Videos y Momentos de Clase
        </h2>
        <p class="mt-4 text-base sm:text-lg text-carbon/80 leading-relaxed">
          Fragmentos y registros audiovisuales de las prácticas en cocina agrupados por preparación ({len(videos)} clips seleccionados).
        </p>
      </div>
      {"".join(blocks)}
    </div>
  </section>
'''


def build_references_section():
    return '''
  <!-- ===================================================================== -->
  <!-- 7. REFERENCIAS Y FUENTES BIBLIOGRÁFICAS                               -->
  <!-- ===================================================================== -->
  <section id="referencias" class="py-20 sm:py-24 bg-coco border-b border-selva/15">
    <div class="max-w-7xl mx-auto px-5 sm:px-8">
      <div class="max-w-3xl reveal">
        <span class="px-4 py-1.5 rounded-full bg-selva text-platano text-xs font-bold uppercase tracking-widest">Fuentes &amp; Repositorio</span>
        <h2 class="mt-4 font-editorial font-black text-3xl sm:text-5xl text-selva leading-[1.08]">
          Referencias y Documentación de Clase
        </h2>
        <p class="mt-3 text-base text-carbon/80 leading-relaxed">
          Bibliografía consultada en el repositorio de la asignatura y publicaciones oficiales del Estado colombiano sobre cocinas tradicionales, biodiversidad y patrimonio cultural del Pacífico.
        </p>
      </div>

      <div class="mt-10 grid grid-cols-1 lg:grid-cols-2 gap-8">
        <div class="rounded-3xl bg-arena p-7 sm:p-8 border border-selva/15">
          <h3 class="font-editorial font-bold text-2xl text-marea">Repositorio de la Materia (PUJ Cali)</h3>
          <ul class="mt-5 space-y-3.5 text-sm text-carbon/90 leading-relaxed">
            <li><strong>Arocha, Jaime (2007).</strong> <em>Encocaos con papa, ¿otro etnoboom usurpador?</em> Revista Colombiana de Antropología, vol. 43, pp. 91–117. Instituto Colombiano de Antropología e Historia (ICANH), Bogotá.</li>
            <li><strong>Ministerio de Cultura de Colombia (2012).</strong> <em>Política para el conocimiento, la salvaguardia y el fomento de la alimentación y las cocinas tradicionales de Colombia.</em> Biblioteca Básica de Cocinas Tradicionales de Colombia (Tomo 17), Dirección de Patrimonio.</li>
            <li><strong>Ministerio de Cultura &amp; Fundación ACUA (2018).</strong> <em>Biodiversidad, cocina e identidad en el Pacífico Colombiano: la cocina tradicional de Tumaco (Nariño) y Buenaventura (Valle del Cauca).</em> Cultura Culinaria y Biodiversidad.</li>
            <li><strong>Ministerio de Cultura &amp; Fundación ACUA (2018).</strong> <em>Saberes &amp; Sabores del Pacífico Colombiano: Buenaventura – Tumaco.</em> Cultura Culinaria y Biodiversidad.</li>
            <li><strong>SENA · Grupo Fogones y Comunidades (2013).</strong> <em>Sabor Pacífico, Sabor a Memoria.</em> Servicio Nacional de Aprendizaje (SENA).</li>
            <li><strong>Grueso Romero, Mary (2015).</strong> <em>Cuando los ancestros llaman: poesía afrocolombiana.</em> Editorial Universidad del Cauca, Popayán.</li>
            <li><strong>Palacios, Arnoldo (1949 / ed. 2010).</strong> <em>Las estrellas son negras.</em> Biblioteca de Literatura Afrocolombiana (Tomo II), Ministerio de Cultura, Bogotá.</li>
            <li><strong>Material de cátedra (PUJ Cali).</strong> <em>El Festín de las Mujeres del Pacífico.</em> Archivo bibliográfico del curso Cocinas del Pacífico.</li>
          </ul>
        </div>

        <div class="rounded-3xl bg-selva text-coco p-7 sm:p-8 shadow-lg">
          <h3 class="font-editorial font-bold text-2xl text-platano">Publicaciones y Normativa del Estado Colombiano</h3>
          <ul class="mt-5 space-y-3.5 text-sm text-coco/90 leading-relaxed">
            <li><strong>Congreso de la República de Colombia (2021).</strong> <em>Ley 2158 de 2021</em>, por medio de la cual se reconoce, impulsa y protege el Viche/Biche y sus derivados como Patrimonio Cultural Inmaterial de la Nación y patrimonio colectivo de las comunidades negras del Pacífico.</li>
            <li><strong>Presidencia de la República / MinCultura (2024).</strong> <em>Decreto 1456 de 2024</em>, reglamentación integral de la Ley 2158 de 2021 para la salvaguardia del Paisaje Cultural Vichero en Chocó, Valle del Cauca, Cauca y Nariño.</li>
            <li><strong>Ministerio de Cultura de Colombia.</strong> <em>Biblioteca Básica de Cocinas Tradicionales de Colombia</em> y plataforma <em>GastroHerencia</em>: compilación regional de saberes culinarios (incluyendo <em>Saberes y Sabores del Pacífico: Guapi – Quibdó</em> y <em>El fogón de los ríos</em>).</li>
            <li><strong>UNESCO &amp; Ministerio de Cultura de Colombia.</strong> <em>Músicas de marimba, cantos y bailes tradicionales del Pacífico Sur colombiano</em> (Lista Representativa del Patrimonio Cultural Inmaterial de la Humanidad), contexto cultural de instrumentos como el guasá y los cantos de cocina.</li>
          </ul>
        </div>
      </div>
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

    CURATED_CARDS = {
        'c1': [
            {
                'insertAfterIndex': 2,
                'span': 'sm:col-span-2',
                'bgClass': 'bg-selva text-coco',
                'tag': 'Ana Rosa Heredia · Saberes & Sabores (MinCultura)',
                'tagClass': 'text-platano',
                'quote': '“Nuestros platos son las joyas producto de nuestra tradición; olvidarnos de ellos es olvidar nuestra región.”',
            },
            {
                'insertAfterIndex': 6,
                'span': '',
                'bgClass': 'bg-platano text-carbon',
                'tag': 'Sabor Pacífico, Sabor a Memoria · SENA',
                'tagClass': 'text-selva',
                'quote': '“Quien conoce lo ancestral, descubre lo esencial.”',
            },
            {
                'insertAfterIndex': 9,
                'span': 'sm:col-span-2',
                'bgClass': 'bg-marea text-coco',
                'tag': 'Apunte de taller · Piedra y masa',
                'tagClass': 'text-platano',
                'quote': 'En el territorio se distinguen dos piedras: una más rústica para quebrar el maíz y otra fina para molerlo hasta formar masa.',
            },
        ],
        'c2': [
            {
                'insertAfterIndex': 2,
                'span': 'sm:col-span-2',
                'bgClass': 'bg-achiote text-coco',
                'tag': 'Sabor Pacífico · Grupo Fogones y Comunidades',
                'tagClass': 'text-platano',
                'quote': '“Iniciamos con el refrito, confundido con el ahogao vallecaucano, pero de singular composición por las hierbas que lo integran.”',
            },
            {
                'insertAfterIndex': 5,
                'span': '',
                'bgClass': 'bg-platano text-carbon',
                'tag': 'Aliños de Azotea · Recetario SENA',
                'tagClass': 'text-achiote',
                'quote': 'Cebolla larga, ajíes dulces criollos, chillangua (cimarrón), albahaca negra (chirarán), oreganón y semillas de achiote.',
            },
        ],
        'c3': [
            {
                'insertAfterIndex': 3,
                'span': 'sm:col-span-2',
                'bgClass': 'bg-marea text-coco',
                'tag': 'Sabor Pacífico, Sabor a Memoria · SENA',
                'tagClass': 'text-platano',
                'quote': '“Al fondo, la cocina con su fogón y su barbacoa, donde pescados y carnes se ahúman lentamente con leña de mangle para el encocado o el sancocho con leche de coco.”',
            },
            {
                'insertAfterIndex': 8,
                'span': 'sm:col-span-2',
                'bgClass': 'bg-selva text-coco',
                'tag': 'Saberes & Sabores · MinCultura / ACUA',
                'tagClass': 'text-platano',
                'quote': '“El almuerzo siempre lleva arroz con o sin coco, y plátano frito o cocido; sancocho o sudado de pescado con coco (encocado), jaiba, camarón o piangua.”',
            },
            {
                'insertAfterIndex': 12,
                'span': 'sm:col-span-2',
                'bgClass': 'bg-platano text-carbon',
                'tag': 'Técnica del Coco · Práctica en clase',
                'tagClass': 'text-selva',
                'quote': 'La segunda leche cocina los tubérculos y carnes; la primera extracción se reserva para el cierre a fuego suave.',
            },
        ],
        'c4': [],
        'c5': [
            {
                'insertAfterIndex': 2,
                'span': 'sm:col-span-2',
                'bgClass': 'bg-selva text-coco',
                'tag': 'Saberes & Sabores · MinCultura / ACUA',
                'tagClass': 'text-platano',
                'quote': '“Cuando se cocina y se canta las cosas saben mejor.”',
            },
            {
                'insertAfterIndex': 5,
                'span': 'sm:col-span-2',
                'bgClass': 'bg-marea text-coco',
                'tag': 'Sabor Pacífico · Grupo Fogones y Comunidades',
                'tagClass': 'text-platano',
                'quote': '“… la cocina no solamente es comer, la cocina es cultura y arte… la buena comida alimenta hasta el alma.”',
            },
            {
                'insertAfterIndex': 7,
                'span': 'sm:col-span-2',
                'bgClass': 'bg-platano text-carbon',
                'tag': 'Ley 2158 de 2021 · Patrimonio del Pacífico',
                'tagClass': 'text-selva',
                'quote': 'El viche o biche y sus derivados se reconocen como patrimonio cultural inmaterial y saber colectivo de las comunidades negras del Pacífico.',
            },
        ],
    }

    for i in range(1, 6):
        ckey = f'c{i}'
        selected = grouped[ckey]
        payload = [
            {
                'id': r['sourceId'],
                'caption': r['visualDescription'],
                'originalName': r.get('displayTitle', r['curatedFileName']),
                'primaryCategory': r['primaryCategory'],
                'span': 'sm:col-span-2' if ((ckey == 'c3' and n == 14) or (ckey == 'c5' and n == 7)) else spans[n % len(spans)],
            }
            for n, r in enumerate(selected)
        ]
        pattern = rf'({ckey}: \{{.*?photos: )\[.*?\](,\s*cards: )\[.*?\](,\s*videos:)'
        text, count = re.subn(
            pattern,
            lambda m, p=payload, cards=CURATED_CARDS[ckey]: m[1] + json.dumps(p, ensure_ascii=False) + m[2] + json.dumps(cards, ensure_ascii=False) + m[3],
            text,
            count=1,
            flags=re.S,
        )
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
    text = text.replace('>05</span>\n          <span class="uppercase tracking-wider text-[10px]">Crónicas Temáticas</span>', '>04</span>\n          <span class="uppercase tracking-wider text-[10px]">Ejes Temáticos</span>')
    text = text.replace('>78</span>\n          <span class="uppercase tracking-wider text-[10px]">Postales de Taller</span>', f'>{total_photos}</span>\n          <span class="uppercase tracking-wider text-[10px]">Fotografías de Clase</span>')
    text = text.replace('>18</span>\n          <span class="uppercase tracking-wider text-[10px]">Memorias en Video</span>', f'>{total_videos}</span>\n          <span class="uppercase tracking-wider text-[10px]">Videos de Clase</span>')
    text = text.replace('Voces en el Glosario', 'Términos en el Glosario')
    text = text.replace('1 / 78', f'1 / {total_photos}')
    text = text.replace('78 FOTOS ÚNICAS + 18 VIDEOS', f'{total_photos} FOTOS CURADAS · {total_videos} VIDEOS')
    text = text.replace('Crónica viva de las Cocinas del Pacífico Colombiano', 'Crónica y bitácora de las Cocinas del Pacífico Colombiano')
    text = text.replace(
        'Un recorrido sensorial y gastronómico en cinco capítulos: de la piedra de moler y el perfume de la azotea hasta el coco recién estrujado, el pulso del manglar y la memoria viva del litoral.',
        'Un recorrido por las prácticas de clase: de la piedra de moler y las hierbas de azotea hasta el coco rallado a mano, los frutos del mar, el trabajo en brigada y los registros en video.',
    )
    text = text.replace('Explorar la Crónica', 'Explorar la Revista')
    text = text.replace('>Carta Editorial</span>', '>Presentación</span>')
    text = text.replace(
        'Cocinar el Pacífico es aprender a escuchar el territorio con las manos',
        'Aprender el Pacífico desde el fogón y la mesa compartida',
    )

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
        <a href="#cronica-1" class="hover:text-achiote transition-colors">I. Taller Sensorial</a>
        <a href="#cronica-2" class="hover:text-selva transition-colors">II. Azotea</a>
        <a href="#cronica-3" class="hover:text-marea transition-colors">III. Fogón, Mar &amp; Mesa</a>
        <a href="#cronica-5" class="hover:text-achiote transition-colors">IV. Brigada &amp; Cultura</a>
        <a href="#videos-eje" class="hover:text-marea transition-colors">Videos</a>
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
      <a href="#editorial" class="block py-2.5 px-3 rounded-xl hover:bg-arena text-marea">Presentación y Mapa de Lectura</a>
      <a href="#cronica-1" class="block py-2.5 px-3 rounded-xl hover:bg-arena text-carbon">I · Taller Sensorial</a>
      <a href="#cronica-2" class="block py-2.5 px-3 rounded-xl hover:bg-arena text-selva">II · Azotea</a>
      <a href="#cronica-3" class="block py-2.5 px-3 rounded-xl hover:bg-arena text-marea">III · Fogón, Mar &amp; Mesa</a>
      <a href="#cronica-5" class="block py-2.5 px-3 rounded-xl hover:bg-arena text-achiote">IV · Brigada &amp; Cultura</a>
      <a href="#videos-eje" class="block py-2.5 px-3 rounded-xl hover:bg-arena text-carbon">Videos</a>
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
        'Organizamos esta bitácora en cuatro ejes temáticos y una sección audiovisual agrupada por preparación, integrando las fotografías de clase, los fragmentos de cocina y las voces recogidas durante el semestre.',
    )
    text = text.replace('Cinco Crónicas del Litoral', 'Cuatro Ejes y Archivo Audiovisual')
    text = text.replace('Selecciona cualquier capítulo para sumergirte en sus crónicas, mosaicos fotográficos y memorias en video.', 'Selecciona un eje para recorrer las fotografías de clase o ve directamente a la sección de videos por preparación.')

    # Actualizar las 5 tarjetas del Mapa de Lectura con colores semánticos por tema
    c1_n, c2_n, c3_n, c5_n = len(grouped['c1']), len(grouped['c2']), len(grouped['c3']), len(grouped['c5'])
    old_cards_grid = '''        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-4">
          <!-- Tarjeta I -->
          <a href="#cronica-1" class="group rounded-3xl p-6 bg-selva text-coco shadow-md hover:-translate-y-1.5 hover:shadow-xl transition-all flex flex-col justify-between min-h-[210px]">
            <div class="flex items-center justify-between">
              <span class="font-editorial text-3xl font-black text-platano">I</span>
              <span class="text-[10px] font-bold uppercase tracking-widest px-2.5 py-1 rounded-full bg-coco/15 text-coco">18 fotos · 4 videos</span>
            </div>
            <div class="mt-6">
              <h4 class="font-editorial font-bold text-xl leading-snug group-hover:text-platano transition-colors">Territorio, Saberes y Herramientas</h4>
              <p class="text-xs text-coco/75 mt-2">Piedra de moler, maíz, plátano, fufú y Juan Valerio.</p>
            </div>
          </a>

          <!-- Tarjeta II -->
          <a href="#cronica-2" class="group rounded-3xl p-6 bg-achiote text-coco shadow-md hover:-translate-y-1.5 hover:shadow-xl transition-all flex flex-col justify-between min-h-[210px]">
            <div class="flex items-center justify-between">
              <span class="font-editorial text-3xl font-black text-platano">II</span>
              <span class="text-[10px] font-bold uppercase tracking-widest px-2.5 py-1 rounded-full bg-coco/15 text-coco">15 fotos · 3 videos</span>
            </div>
            <div class="mt-6">
              <h4 class="font-editorial font-bold text-xl leading-snug group-hover:text-platano transition-colors">Hierbas de Azotea y Selva</h4>
              <p class="text-xs text-coco/85 mt-2">Chillangua, chirarán, poleo, pipilongo y refrito solar.</p>
            </div>
          </a>

          <!-- Tarjeta III -->
          <a href="#cronica-3" class="group rounded-3xl p-6 bg-platano text-carbon shadow-md hover:-translate-y-1.5 hover:shadow-xl transition-all flex flex-col justify-between min-h-[210px]">
            <div class="flex items-center justify-between">
              <span class="font-editorial text-3xl font-black text-selva">III</span>
              <span class="text-[10px] font-bold uppercase tracking-widest px-2.5 py-1 rounded-full bg-carbon/10 text-carbon">15 fotos · 4 videos</span>
            </div>
            <div class="mt-6">
              <h4 class="font-editorial font-bold text-xl leading-snug group-hover:text-achiote transition-colors">Coco, Tubérculos y Fogón</h4>
              <p class="text-xs text-carbon/80 mt-2">Leche de coco artesanal, encocados, tapao y amasijos.</p>
            </div>
          </a>

          <!-- Tarjeta IV -->
          <a href="#cronica-4" class="group rounded-3xl p-6 bg-marea text-coco shadow-md hover:-translate-y-1.5 hover:shadow-xl transition-all flex flex-col justify-between min-h-[210px]">
            <div class="flex items-center justify-between">
              <span class="font-editorial text-3xl font-black text-platano">IV</span>
              <span class="text-[10px] font-bold uppercase tracking-widest px-2.5 py-1 rounded-full bg-coco/15 text-coco">15 fotos · 4 videos</span>
            </div>
            <div class="mt-6">
              <h4 class="font-editorial font-bold text-xl leading-snug group-hover:text-platano transition-colors">Mar, Río y Manglar</h4>
              <p class="text-xs text-coco/80 mt-2">Piangüeras, bocana, cangrejos, jaiba y biodiversidad.</p>
            </div>
          </a>

          <!-- Tarjeta V -->
          <a href="#cronica-5" class="group rounded-3xl p-6 bg-chontaduro text-coco shadow-md hover:-translate-y-1.5 hover:shadow-xl transition-all flex flex-col justify-between min-h-[210px]">
            <div class="flex items-center justify-between">
              <span class="font-editorial text-3xl font-black text-coco">V</span>
              <span class="text-[10px] font-bold uppercase tracking-widest px-2.5 py-1 rounded-full bg-carbon/20 text-coco">15 fotos · 3 videos</span>
            </div>
            <div class="mt-6">
              <h4 class="font-editorial font-bold text-xl leading-snug group-hover:text-carbon transition-colors">Bebidas y Cultura Viva</h4>
              <p class="text-xs text-coco/90 mt-2">Viche, cantos de cocina, San Pacho y pueblos originarios.</p>
            </div>
          </a>
        </div>'''
    new_cards_grid = f'''        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-4">
          <!-- Tarjeta I: Amarillo Plátano / Maíz / Fibras -->
          <a href="#cronica-1" class="group rounded-3xl p-6 bg-platano text-carbon shadow-md hover:-translate-y-1.5 hover:shadow-xl transition-all flex flex-col justify-between min-h-[210px]">
            <div class="flex items-center justify-between">
              <span class="font-editorial text-3xl font-black text-selva">I</span>
              <span class="text-[10px] font-bold uppercase tracking-widest px-2.5 py-1 rounded-full bg-carbon/10 text-carbon">{c1_n} fotos</span>
            </div>
            <div class="mt-6">
              <h4 class="font-editorial font-bold text-xl leading-snug group-hover:text-selva transition-colors">Taller Sensorial</h4>
              <p class="text-xs text-carbon/85 mt-2">Piedra de moler, utensilios tradicionales, maíz, bijao y despensa del litoral.</p>
            </div>
          </a>

          <!-- Tarjeta II: Verde Selva / Hierbas de Azotea -->
          <a href="#cronica-2" class="group rounded-3xl p-6 bg-selva text-coco shadow-md hover:-translate-y-1.5 hover:shadow-xl transition-all flex flex-col justify-between min-h-[210px]">
            <div class="flex items-center justify-between">
              <span class="font-editorial text-3xl font-black text-platano">II</span>
              <span class="text-[10px] font-bold uppercase tracking-widest px-2.5 py-1 rounded-full bg-coco/15 text-coco">{c2_n} fotos</span>
            </div>
            <div class="mt-6">
              <h4 class="font-editorial font-bold text-xl leading-snug group-hover:text-platano transition-colors">Azotea</h4>
              <p class="text-xs text-coco/85 mt-2">Chillangua, chirarán, poleo, pipilongo y refrito con achiote.</p>
            </div>
          </a>

          <!-- Tarjeta III: Azul Marea / Fogón, Mar y Mesa -->
          <a href="#cronica-3" class="group rounded-3xl p-6 bg-marea text-coco shadow-md hover:-translate-y-1.5 hover:shadow-xl transition-all flex flex-col justify-between min-h-[210px]">
            <div class="flex items-center justify-between">
              <span class="font-editorial text-3xl font-black text-platano">III</span>
              <span class="text-[10px] font-bold uppercase tracking-widest px-2.5 py-1 rounded-full bg-coco/15 text-coco">{c3_n} fotos</span>
            </div>
            <div class="mt-6">
              <h4 class="font-editorial font-bold text-xl leading-snug group-hover:text-platano transition-colors">Fogón, Mar &amp; Mesa</h4>
              <p class="text-xs text-coco/85 mt-2">Leche de coco artesanal, encocados, mariscos, arroces y amasijos.</p>
            </div>
          </a>

          <!-- Tarjeta IV: Achiote / Terracota / Brigada y Cultura Viva -->
          <a href="#cronica-5" class="group rounded-3xl p-6 bg-achiote text-coco shadow-md hover:-translate-y-1.5 hover:shadow-xl transition-all flex flex-col justify-between min-h-[210px]">
            <div class="flex items-center justify-between">
              <span class="font-editorial text-3xl font-black text-platano">IV</span>
              <span class="text-[10px] font-bold uppercase tracking-widest px-2.5 py-1 rounded-full bg-coco/15 text-coco">{c5_n} fotos</span>
            </div>
            <div class="mt-6">
              <h4 class="font-editorial font-bold text-xl leading-snug group-hover:text-platano transition-colors">Brigada &amp; Cultura</h4>
              <p class="text-xs text-coco/85 mt-2">Trabajo en equipo, libros de consulta, guasá y tradición oral.</p>
            </div>
          </a>

          <!-- Tarjeta AV: Carbón Editorial / Videos -->
          <a href="#videos-eje" class="group rounded-3xl p-6 bg-carbon text-coco shadow-md hover:-translate-y-1.5 hover:shadow-xl transition-all flex flex-col justify-between min-h-[210px]">
            <div class="flex items-center justify-between">
              <span class="font-editorial text-2xl font-black text-platano">AV</span>
              <span class="text-[10px] font-bold uppercase tracking-widest px-2.5 py-1 rounded-full bg-platano text-carbon">{total_videos} videos</span>
            </div>
            <div class="mt-6">
              <h4 class="font-editorial font-bold text-xl leading-snug group-hover:text-platano transition-colors">Videos</h4>
              <p class="text-xs text-coco/85 mt-2">Momentos de taller sensorial, maíz, refrito, arroz con coco y fufú.</p>
            </div>
          </a>
        </div>'''
    assert old_cards_grid in text
    text = text.replace(old_cards_grid, new_cards_grid, 1)

    # Actualizar encabezados de Ejes I-IV sincronizados con sus colores semánticos
    text = text.replace(
        '<span class="px-4 py-1.5 rounded-full bg-selva text-platano text-xs font-bold uppercase tracking-widest">Crónica I</span>',
        '<span class="px-4 py-1.5 rounded-full bg-platano text-carbon text-xs font-bold uppercase tracking-widest">Eje I</span>',
    )
    text = text.replace(
        'Antes de la electricidad y el acero inoxidable, el pulso del Pacífico se talló en piedra, madera y manos pacientes.',
        'Antes de encender los fogones, el taller sensorial nos acercó al peso de la piedra, la madera, las fibras y los sabores base del litoral.',
    )
    text = text.replace(
        '<span class="px-4 py-1.5 rounded-full bg-achiote text-coco text-xs font-bold uppercase tracking-widest">Crónica II</span>',
        '<span class="px-4 py-1.5 rounded-full bg-selva text-platano text-xs font-bold uppercase tracking-widest">Eje II</span>',
    )
    text = text.replace(
        '<h2 class="font-editorial font-black text-4xl sm:text-6xl text-achiote leading-[1.04]">\n          Hierbas de Azotea y Aromas de la Selva\n        </h2>',
        '<h2 class="font-editorial font-black text-4xl sm:text-6xl text-selva leading-[1.04]">\n          Hierbas de Azotea y Aromas de la Selva\n        </h2>',
    )
    text = text.replace(
        'En el Pacífico, la sazón se aprende primero con la nariz y se cultiva a un paso de la cocina, elevada sobre la humedad de la tierra.',
        'En el Pacífico, la sazón empieza en las huertas elevadas a un paso de la cocina y se construye en el refrito.',
    )
    text = text.replace('el aula entera cambió de temperatura y paisaje.', 'el aula se llenó de aromas del litoral.')
    text = text.replace('el abrazo solar del', 'el color cálido del')
    text = text.replace(
        '<span class="px-4 py-1.5 rounded-full bg-platano text-carbon text-xs font-bold uppercase tracking-widest">Crónica III</span>',
        '<span class="px-4 py-1.5 rounded-full bg-marea text-platano text-xs font-bold uppercase tracking-widest">Eje III</span>',
    )
    text = text.replace('Alquimia del Fogón · Guisos y Raíces', 'Cocina en Práctica · Coco, Mar y Tubérculos')
    text = text.replace(
        '<h2 class="font-editorial font-black text-4xl sm:text-6xl text-carbon leading-[1.04]">\n          Coco, Tubérculos y Fogón\n        </h2>',
        '<h2 class="font-editorial font-black text-4xl sm:text-6xl text-marea leading-[1.04]">\n          Fogón, Mar y Mesa del Pacífico\n        </h2>',
    )
    text = text.replace(
        'El tiempo en las ollas del Pacífico no se mide en cronómetros: se escucha hasta que el coco se vuelve seda y los tubérculos abrazan el caldo.',
        'Leche de coco extraída a mano, fuegos lentos y cocciones donde el marisco, los arroces y los amasijos toman su punto.',
    )
    text = text.replace('Pocas técnicas revelan tanto cariño como rallar y estrujar el coco a mano para separar sus dos vidas:', 'Pocas técnicas dicen tanto de la cocina del Pacífico como rallar y estrujar el coco a mano para separar sus dos extracciones:')
    text = text.replace('monumentos del sabor', 'platos emblemáticos')
    text = text.replace('las raíces generosas', 'los tubérculos tradicionales')
    old_c3_col2 = '''            A su alrededor florece también la tradición horneada de los
            <button type="button" class="glossary-link" onclick="openGlossary('amasijos')">amasijos del Pacífico</button>,
            recordándonos que la cocina costera es tan rica en texturas crocantes y masas tibias como en caldos profundos.'''
    new_c3_col2 = '''            Con ellos dialogan los frutos de la <button type="button" class="glossary-link" onclick="openGlossary('bocana')">bocana</button>, la <button type="button" class="glossary-link" onclick="openGlossary('pesca_artesanal')">pesca artesanal</button> y la <button type="button" class="glossary-link" onclick="openGlossary('pesca_manglar')">pesca de manglar</button> —cangrejo azul, <button type="button" class="glossary-link" onclick="openGlossary('jaiba')">jaiba</button>, <button type="button" class="glossary-link" onclick="openGlossary('camaron_titi')">camarón tití</button> y <button type="button" class="glossary-link" onclick="openGlossary('piangua')">piangua</button>—, junto a la tradición horneada y frita de los <button type="button" class="glossary-link" onclick="openGlossary('amasijos')">amasijos del Pacífico</button>, que completan la mesa del litoral.'''
    assert old_c3_col2 in text
    text = text.replace(old_c3_col2, new_c3_col2, 1)

    text = text.replace("chapterTitle: 'Crónica I · Territorio, Saberes y Herramientas Ancestrales'", "chapterTitle: 'Eje I · Taller Sensorial, Saberes y Herramientas'")
    text = text.replace("chapterTitle: 'Crónica II · Hierbas de Azotea y Aromas de la Selva'", "chapterTitle: 'Eje II · Hierbas de Azotea y Aromas de la Selva'")
    text = text.replace("chapterTitle: 'Crónica III · Coco, Tubérculos y Fogón'", "chapterTitle: 'Eje III · Fogón, Mar y Mesa del Pacífico'")
    text = text.replace("chapterTitle: 'Crónica V · Bebidas, Cultura Viva e Identidad'", "chapterTitle: 'Eje IV · Bitácora de Brigada y Cultura Viva'")

    text = text.replace('<article id="cronica-4" class="', '<article id="cronica-4" aria-hidden="true" class="hidden ')
    text = text.replace("['c1', 'c2', 'c3', 'c4', 'c5'].forEach(buildChronicle);", "['c1', 'c2', 'c3', 'c5'].forEach(buildChronicle);")

    MARIMBA_DIVIDER = '''  <!-- Separador Marimba -->
  <div class="py-6 bg-coco" aria-hidden="true">
    <div class="marimba-divider">
      <span class="marimba-bar w-2 h-5"></span>
      <span class="marimba-bar w-2 h-9"></span>
      <span class="marimba-bar w-2 h-14"></span>
      <span class="marimba-bar w-2 h-9"></span>
      <span class="marimba-bar w-2 h-5"></span>
    </div>
  </div>

  '''
    text = text.replace('<article id="cronica-5"', MARIMBA_DIVIDER + '<article id="cronica-5"', 1)

    text = text.replace('>Crónica V</span>', '>Eje IV</span>')
    text = text.replace('<!-- Cabecera de Crónica V -->', '<!-- Cabecera de Eje IV -->')
    text = text.replace('<!-- Texto Editorial de Crónica V -->', '<!-- Texto Editorial de Eje IV -->')
    text = text.replace('Espiritualidad, Fiesta y Ética Culinaria', 'Bitácora de Brigada, Cultura Viva y Ética Culinaria')
    text = text.replace(
        '<h2 class="font-editorial font-black text-4xl sm:text-6xl text-marea leading-[1.04]">\n          Bebidas, Cultura Viva e Identidad\n        </h2>',
        '<h2 class="font-editorial font-black text-4xl sm:text-6xl text-marea leading-[1.04]">\n          Bitácora de Brigada y Cultura Viva\n        </h2>',
    )
    text = text.replace(
        'En el Pacífico se cocina cantando, se destila memoria y se defiende la vida a través de la soberanía alimentaria.',
        'Trabajo en equipo, tradición oral, cantos vinculados al oficio y lecturas que contextualizan cada práctica en clase.',
    )
    text = text.replace('sazonan la memoria', 'acompañan las jornadas')
    text = text.replace('transformarlo en masa viva.', 'transformarlo en masa homogénea.')
    text = text.replace('escuchamos al plátano verde y al maduro contar historias sin fronteras.', 'trabajamos el plátano verde y el maduro en preparaciones que conectan a todo el litoral.')
    text = text.replace('para regalar color limpio y aroma terroso sin amargor.', 'para aportar color limpio y aroma terroso sin amargor.')
    text = text.replace(
        'Crónica de las Cocinas del Pacífico. Un tributo a las portadoras de tradición, a los ecosistemas de selva y manglar, y a cada aprendizaje vivido frente al fogón universitario.',
        'Crónica y bitácora de las Cocinas del Pacífico: saberes tradicionales, ecosistemas del litoral y aprendizaje frente al fogón universitario.',
    )

    # Cambio #5: Quitar por completo las franjas de Memorias en Movimiento dentro de las crónicas e insertar sección propia antes del Glosario
    text = re.sub(
        r'\s*<!-- Franja Memorias en Movimiento.*?<div id="videos-c\d"[^>]*></div>\s*</div>',
        '',
        text,
        flags=re.S,
    )
    text = text.replace('  <!-- ===================================================================== -->\n  <!-- 6. GLOSARIO INTERACTIVO', build_videos_section(videos) + '\n  <!-- ===================================================================== -->\n  <!-- 6. GLOSARIO INTERACTIVO', 1)

    # Insertar sección #referencias antes del footer
    text = text.replace('  <!-- ===================================================================== -->\n  <!-- 7. CONTRAPORTADA EDITORIAL', build_references_section() + '\n  <!-- ===================================================================== -->\n  <!-- 7. CONTRAPORTADA EDITORIAL', 1)

    # Cambio #6: Footer -> Aida Arteaga y David González + Fotografía Estudiantes + enlace a #referencias
    text = text.replace(
        '<p class="font-editorial font-bold text-xl text-coco mt-1">Aida Arteaga</p>',
        '<p class="font-editorial font-bold text-xl text-coco mt-1">Aida Arteaga y David González</p>'
        '\n              <span class="text-[10px] font-bold uppercase tracking-widest text-platano block mt-3">Fotografía y Registro</span>'
        '\n              <p class="text-xs text-coco/85 mt-0.5">Estudiantes de Cocinas del Pacífico 2026-2</p>',
    )
    text = text.replace(
        '↑ Volver a la Portada\n            </a>',
        '↑ Volver a la Portada\n            </a>\n'
        '            <a href="#referencias"\n'
        '              class="inline-flex items-center gap-2 px-5 py-2.5 rounded-full bg-coco/10 hover:bg-selva text-coco border border-coco/20 font-semibold text-xs uppercase tracking-wider transition-colors">\n'
        '              ↑ Referencias y Fuentes\n'
        '            </a>',
    )

    # Quitar enlaces de "Abrir en Drive" en Lightbox y tarjetas
    text = re.sub(r'\s*<a id="lb-drive-btn".*?</a>', '', text, flags=re.S)
    text = text.replace("document.getElementById('lb-drive-btn').href = driveView(item.id);", '')
    text = re.sub(r'\s*<a href="\$\{driveView\([^)]+\)\}"[^>]*>\s*Abrir en Drive ↗\s*</a>', '', text, flags=re.S)

    # Quitar botones de Guardar PDF (header y footer) y su listener
    text = re.sub(r'\s*<button id="print-pdf-btn".*?</button>', '', text, flags=re.S)
    text = re.sub(r'\s*<button type="button" onclick="window\.print\(\)".*?</button>', '', text, flags=re.S)
    text = text.replace("document.getElementById('print-pdf-btn').addEventListener('click', () => window.print());", '')

    # Limpieza de textos técnicos/avisos
    text = text.replace('img.parentElement.querySelector(', 'img.parentElement?.querySelector(')
    text = text.replace('Algunas fotografías se muestran en modo reserva. Asegúrate de que la carpeta compartida en Google Drive esté configurada como <em>"Cualquier persona con el enlace · Lector"</em>.', 'Algunas vistas previas no están disponibles temporalmente. Comprueba tu conexión a Internet o recarga la página.')
    text = text.replace('Activa el acceso público en Google Drive o ábrela directamente desde el enlace.', 'Vista previa no disponible temporalmente: comprueba tu conexión a Internet.')

    # Atributos de rendimiento en imágenes (cover y lightbox) y metadatos SEO / OpenGraph / Favicon
    text = text.replace(
        'id="cover-hero-img"',
        'id="cover-hero-img"\n        fetchpriority="high"\n        decoding="async"',
        1,
    )
    text = text.replace(
        'class="max-h-[70vh] w-auto object-contain rounded-xl"',
        'decoding="async"\n          class="max-h-[70vh] w-auto object-contain rounded-xl"',
        1,
    )
    seo_meta = (
        '  <meta name="author" content="Aida Arteaga, David González, Estudiantes de Cocinas del Pacífico 2026-2" />\n'
        '  <meta name="theme-color" content="#0F4C3A" />\n'
        '  <meta property="og:title" content="MAREA &amp; AZOTEA · Crónica y bitácora de las Cocinas del Pacífico Colombiano" />\n'
        '  <meta property="og:description" content="Revista digital editorial de la cátedra Cocinas del Pacífico · Gastronomía y Artes Culinarias · Pontificia Universidad Javeriana Cali." />\n'
        '  <meta property="og:type" content="article" />\n'
        '  <meta property="og:locale" content="es_CO" />\n'
        '  <link rel="icon" type="image/svg+xml" href="data:image/svg+xml,%3Csvg xmlns=\'http://www.w3.org/2000/svg\' viewBox=\'0 0 32 32\'%3E%3Ccircle cx=\'16\' cy=\'16\' r=\'16\' fill=\'%230F4C3A\'/%3E%3Cpath d=\'M5 20C8.5 17 12.5 17 16 20C19.5 23 23.5 23 27 20\' stroke=\'%23E9B44C\' stroke-width=\'2.4\' stroke-linecap=\'round\' fill=\'none\'/%3E%3Cpath d=\'M16 15.5C16 10.5 19.5 6.5 24.5 6.5C24.5 11.5 21 15.5 16 15.5Z\' fill=\'%23E9B44C\'/%3E%3C/svg%3E" />'
    )
    text = text.replace(
        '<meta name="description" content="Revista digital editorial de la cátedra Cocinas del Pacífico · Gastronomía y Artes Culinarias · Pontificia Universidad Javeriana Cali." />',
        '<meta name="description" content="Revista digital editorial de la cátedra Cocinas del Pacífico · Gastronomía y Artes Culinarias · Pontificia Universidad Javeriana Cali." />\n' + seo_meta,
        1,
    )

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
