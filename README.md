# Marea & Azotea — revista de Cocinas del Pacífico

Edición estática de cinco ejes temáticos. Conserva la identidad editorial, la paleta selva/marea/achiote/plátano/coco y las fuentes Playfair Display, Plus Jakarta Sans y Space Mono. Sin framework, backend, Tailwind de ejecución ni dependencias nuevas.

## Abrir la revista

Abrir `index.html` directamente funciona; también se puede servir el repositorio:

```sh
python -m http.server 8080 --bind 127.0.0.1
```

Visitar <http://127.0.0.1:8080>. `index.html` y `assets/` deben viajar juntos al publicar en un alojamiento estático como GitHub Pages. Las fuentes de Google y las miniaturas de Drive necesitan Internet; el contenido, los estilos, los filtros y el visor son locales. Los enlaces al catálogo abren los metadatos de auditoría, **no** otra selección pública de imágenes.

## Alcance editorial

Solo se publican fotos cuyo `reviewStatus` es `verified` en [el catálogo temático](audit/thematic-catalog.json). En este checkpoint son **58 registros**, distribuidos según su categoría principal:

| Eje | Registros publicados |
| --- | ---: |
| Territorio, Saberes y Herramientas Ancestrales | 29 |
| Hierbas de Azotea y Aromas de la Selva | 15 |
| Frutos del Mar, Río y Manglar | 9 |
| Coco, Tubérculos y Fogón | 5 |
| Bebidas, Cultura Viva e Identidad | 0 |

`verified` significa sujeto visible y encaje en un eje amplio; no es certificación de recetas, especies, procedencias o identidades. Cada pie y alt reproduce `visualDescription` exactamente, y cada foto conserva su nombre original y enlace por ID. La portada utiliza `IMG_1898.HEIC`, ID `1jMeLokjKWlpVlkg_X67NqsVLP9nFM-QV`, del eje Territorio.

No se deduplican registros por nombre, parecido ni hash. **58 es el número de IDs de la selección**, no de escenas diferentes ni de todas las fotos del archivo. Se muestra solo una apertura por eje con imágenes disponibles y una galería completa, evitando dos rejillas de 58 tarjetas. El eje sin fotos tiene un estado vacío explícito.

Se excluyen de la revista 91 fotos `provisional`, 32 `needs-human` y 31 MOV `uninspected-video`. Los 212 registros siguen accesibles en el catálogo completo, que no se modificó. Se retiraron `Personalizar`, cargas locales y glosario botánico/recetario no respaldado: no hay persistencia ni promesa de guardado. Imprimir/PDF abre la impresión del navegador y prepara **toda** la selección, independientemente del filtro activo; el PDF no es una revista editable. La disponibilidad de imágenes depende de la red y de Drive; el fallback no atribuye todos los errores a permisos.

## Actualizar y comprobar

La fuente del markup es `tools/build_magazine.py`; **regenerar `index.html` después de editar la plantilla o tras una revisión autorizada del catálogo**:

```sh
python tools/build_magazine.py
python -m unittest discover -s tests -v
node tests/magazine.test.cjs
node tests/magazine-functional.cjs
node tests/magazine-real-smoke.cjs
```

No es necesario ejecutar el generador para ver la página. No renombra archivos de Drive ni descarga imágenes. CSS y comportamiento están en `assets/magazine.css` y `assets/magazine.js`.

Las pruebas de navegador usan Playwright y Chrome ya instalados en este equipo. Por defecto buscan `C:/Users/D/node_modules/playwright` y `C:/Program Files/Google/Chrome/Application/chrome.exe`. En otro equipo se pueden especificar `PLAYWRIGHT_PATH` (ruta del módulo instalado) y `CHROME_PATH`. No se instala nada automáticamente. `MAGAZINE_URL` permite ejecutar el smoke real contra un servidor estático en lugar de `file:`.

- `magazine.test.cjs`: contrato DOM mínimo usado para RED antes de implementar los cinco ejes.
- `magazine-functional.cjs`: imágenes fixture explícitamente simuladas, DOM/JS/CSS reales. Contrasta cada ID/pie/alt/nombre/enlace, seis filtros, navegación en 1440/390/360, visor y foco, móvil, fallback con solicitudes abortadas e impresión. Genera `print-layout-MOCK.pdf`; **no** es evidencia de carga fotográfica real.
- `magazine-real-smoke.cjs`: red Drive real sin sustituir imágenes; exige al menos cinco IDs distintos con dimensiones naturales válidas y la imagen ampliada. Genera capturas desktop/móvil y JSON de respuestas, fallos y errores JS. No afirma haber probado las 58 cargas, reproducción de videos ni otros navegadores.

Los artefactos privados se escriben fuera del repo, por defecto en `C:/Users/D/AppData/Local/hermes/profiles/null/cache/scratch/marea-magazine-qa/`. Se puede cambiar con `ARTIFACT_DIR`. No commitear capturas ni PDFs con fotografías/personas.

## Auditoría histórica frente a edición actual

- [Taxonomía y límites de verified](audit/TAXONOMY.md).
- [Relectura de seis correcciones](audit/THEMATIC-CORRECTIONS-RECHECK.md).
- [Catálogo temático CSV](audit/thematic-catalog.csv) y [JSON](audit/thematic-catalog.json): 212 IDs.
- `audit/page-references.json`, `inventory.json`, `summary.json`, `media-catalog.csv` y `thumbnail-checks.json` son el **snapshot histórico** de la página anterior (47 fotos + 3 videos); no se sobrescribieron para hacer coincidir la edición actual.

`tools/audit_media.py` reconoce el manifiesto de publicación actual y conserva el parser del HTML anterior. Los tests distinguen los 50 registros históricos de los 58 actuales. Si se decide repetir el inventario público de Drive:

```sh
python tools/audit_media.py
```

Ahora escribe en `audit/current/`, separado del snapshot histórico. Ese comando hace lectura de red y comprueba miniaturas; **no** valida semántica ni sustituye los tests de navegador. `python tools/thematic_media.py validate` requiere la evidencia privada `../visual-evidence` ya existente; un clon remoto sin ella no reproduce esa validación completa. No ejecutar `build` del catálogo para cambiar estados sin revisión.

## Entrega para revisión

La página y sus assets se entregan juntos en la rama `audit/thematic-draft` del fork [Dacroxx/marea-y-azotea](https://github.com/Dacroxx/marea-y-azotea/tree/audit/thematic-draft). Para verla, descargar el ZIP de esa rama, extraerlo y abrir `index.html`; GitHub muestra código, no una vista ejecutada de la revista. También se puede usar el servidor local indicado arriba.

Revisión frontend independiente: aprobada con límites, sin bloqueos críticos. Evidencia y límites en [FRONTEND-REVIEW.md](audit/FRONTEND-REVIEW.md). No hay merge a dev/main ni despliegue autorizado; el sitio original continúa sin cambios. No se tocó el WIP del clon de Documents ni se cambiaron permisos/originales de Drive.
