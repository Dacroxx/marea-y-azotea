# Marea & Azotea — revista de Cocinas del Pacífico

## Abrir: solo hace falta `index.html`

Descargar el ZIP de la rama `audit/thematic-draft` del fork [Dacroxx/marea-y-azotea](https://github.com/Dacroxx/marea-y-azotea/tree/audit/thematic-draft), extraerlo y abrir `index.html`. **También se puede copiar únicamente ese HTML a otra carpeta vacía y abrirlo:** contiene todos los estilos y JavaScript, sin `assets/`, Tailwind CDN ni paquetes de ejecución. GitHub muestra código, no ejecuta la revista en su visor de archivos. No se ha autorizado merge ni deploy.

Las fotos de Drive y las fuentes de Google necesitan Internet. Si la red, el servicio o el acceso fallan, se conserva el diseño con fuentes de respaldo y un estado neutral; la portada conserva su SVG. No se alojan originales ni se cambian permisos de Drive. Alternativa opcional:

```sh
python -m http.server 8080 --bind 127.0.0.1
```

Abrir <http://127.0.0.1:8080>. No es necesario ejecutar un build para leer la página.

## La referencia aprobada, no una galería de reemplazo

La base editorial y visual es el HTML aportado por David, preservado exactamente en `source/editorial-template.html`: portada full-bleed con fotografía/SVG y superposición tipográfica; Playfair Display, Fraunces y Plus Jakarta Sans; carta, firma y créditos originales de **Aida Arteaga**; cinco crónicas extensas; mosaicos con spans y 15 cápsulas intercaladas; separadores, cinco espacios audiovisuales, glosario de 44 voces con buscador/filtros/fichas y footer.

Se distingue **contenido editorial aportado** de **evidencia fotográfica**. Las crónicas, citas, recetas, identificaciones botánicas y voces del glosario no han sido verificadas como transcripciones ni revisión científica. Se conserva su voz con una nota de alcance visible, sin convertirla en prueba de lo que aparece en cada foto. La entrega estilística simplificada anterior fue rechazada. El parent abrió el ZIP completo anterior: CSS aplicado y cero errores JS; el fallo general de estilos **no se reprodujo**. Esta corrección restaura la identidad autorizada y elimina, además, la fragilidad de separar el HTML de sus assets; no atribuye una causa al equipo de David.

## Selección fotográfica: 58 IDs verified

| Categoría principal exacta (orden visual de la referencia) | IDs publicados |
| --- | ---: |
| Territorio, Saberes y Herramientas Ancestrales | 29 |
| Hierbas de Azotea y Aromas de la Selva | 15 |
| Coco, Tubérculos y Fogón | 5 |
| Frutos del Mar, Río y Manglar | 9 |
| Bebidas, Cultura Viva e Identidad | 0 |

Cada pie/alt reproduce `visualDescription` exactamente y muestra el nombre original y un enlace por ID. El visor conserva esa trazabilidad. La portada usa `IMG_1898.HEIC`, `1jMeLokjKWlpVlkg_X67NqsVLP9nFM-QV`, verificado en Territorio. `verified` significa sujeto visible y encaje temático amplio, no certificación de receta, especie, procedencia o identidad. No se deduplican escenas por nombre o parecido.

No se publican 91 fotos `provisional`, 32 `needs-human` ni los 31 MOV `uninspected-video`. No se inventan títulos audiovisuales ni se incrustan videos sin revisar. Las franjas mantienen su espacio editorial como archivo pendiente, con cero videos publicados. El quinto eje conserva crónica, cápsulas y glosario, con estado visual vacío explícito. Los conteos de portada, sumario, franjas y visor reflejan la selección real. El catálogo de 212 registros y la auditoría histórica no se reclasificaron para encajar el diseño.

## Regeneración reproducible, sin instalar paquetes

```sh
python tools/build_magazine.py
```

El generador usa la fuente editorial exacta, el catálogo, los suplementos de `source/` y el CSS estático versionado `source/tailwind.generated.css`; regenera `index.html` **sin red**. No escribe en el catálogo ni descarga fotos. Los viejos `assets/magazine.css` y `.js` se conservan como archivos históricos, pero el HTML ya no los solicita.

Si se añaden clases Tailwind a las fuentes, actualizar el CSS en Chrome con las herramientas **ya instaladas** (sin npm install):

```sh
python tools/build_magazine.py --runtime
node tools/capture-editorial-css.cjs
python tools/build_magazine.py
```

Solo esa regeneración opcional de utilidades necesita el CDN en un navegador de build. El script ejercita fichas/categorías del glosario, visor, fallback y menú; captura las reglas de las clases presentes, incluidas variantes responsive/hover. El HTML temporal `source/build-runtime.html` está ignorado y no es el entregable. Se guardan hashes de CSS y runtime en `source/css-build.json`. El CDN no está fijado para siempre: una versión futura puede producir otro CSS; revisar el hash/diff y repetir las pruebas de referencia. El build offline a partir de CSS versionado sí es determinista. La procedencia y checksum exactos del adjunto están en `source/README.md`.

## Pruebas reales

```sh
python -m unittest discover -s tests -v
node tests/magazine.test.cjs
node tests/magazine-functional.cjs
node tests/editorial-reference.cjs
node tests/magazine-real-smoke.cjs
```

Las pruebas de navegador usan Playwright/Chrome existentes. Valores por defecto: `C:/Users/D/node_modules/playwright`, `C:/Program Files/Google/Chrome/Application/chrome.exe`; se pueden especificar `PLAYWRIGHT_PATH` y `CHROME_PATH`. `MAGAZINE_URL` permite hacer smoke contra un servidor en lugar de file.

- `magazine.test.cjs` → contrato de la referencia: su RED real dio 0 mosaicos frente a 5 sobre `f8e3ab1`; ahora pasa.
- `magazine-functional.cjs` → HTML copiado a un directorio vacío, **todo HTTP(S) bloqueado**, sin imágenes fixture. Verifica 58 IDs/pies/alt/nombres/links, categorías 29/15/5/9/0, 15 cápsulas, 44 fichas, buscador/filtros e inyección escapada, enlaces de glosario, navegación, menú, visor/teclado/Esc/foco, fallbacks neutrales, impresión y ausencia de requests a assets/CDN. Pantallas 1440, 390 y 360; PDF con medios no disponibles, no evidencia de fotografías cargadas.
- `editorial-reference.cjs` → compara estilos computados de 14 componentes y 12 propiedades contra el adjunto original en tres anchuras; comprueba también 33 nodos editoriales originales sin reescritura. Es una prueba de red para compilar la referencia, no dependencia del entregable.
- `magazine-real-smoke.cjs` → Drive real, sin fixtures: exige cinco IDs distintos con dimensiones naturales válidas y la foto ampliada. No certifica las 58 cargas ni videos/otros navegadores.
- Tests Python mantienen el contrato del catálogo y el snapshot legacy (47 fotos + 3 videos) separado del manifiesto actual de 58.

Capturas y PDFs privados se escriben fuera del repo en `C:/Users/D/AppData/Local/hermes/profiles/null/cache/scratch/marea-editorial-qa/`, configurable por `ARTIFACT_DIR`. **No commitear fotografías/personas ni PDFs.** Ver resultados y límites de esta corrección en [audit/EDITORIAL-RESTORATION.md](audit/EDITORIAL-RESTORATION.md). El informe `audit/FRONTEND-REVIEW.md` corresponde al diseño anterior, no a una aprobación independiente de este nuevo HTML.

## Auditoría conservada

[TAXONOMY.md](audit/TAXONOMY.md), [catálogo JSON](audit/thematic-catalog.json), [CSV](audit/thematic-catalog.csv) y [correcciones](audit/THEMATIC-CORRECTIONS-RECHECK.md) conservan la revisión existente. `tools/audit_media.py` reconoce el manifiesto actual y mantiene el parser legacy; una nueva auditoría de red escribe en `audit/current/`, no sobre el snapshot histórico. No equivale a revisar semántica. `python tools/thematic_media.py validate` necesita la evidencia privada `../visual-evidence`; un clon remoto sin ella no reproduce esa validación completa.
