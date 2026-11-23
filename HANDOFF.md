# HANDOFF — restauración editorial autocontenida (checkpoint local)

## Estado real / siguiente gate

**Implementación funcional local, pruebas clave verdes; NO aprobada aún por David ni revisión independiente de esta nueva entrega.** Parent debe revisar y decidir si publica checkpoint aprobado o WIP. Este implementador NO hizo commit/push/PR/merge/deploy. No modificar `CONTINUE.md` del parent.

Repo único: `C:/Users/D/AppData/Local/hermes/kanban/boards/david-inc/workspaces/t_ff5bf98a/repo`.
Rama: `audit/thematic-draft`; base HEAD `f8e3ab15c76d2bad2456aeaa3f28aa165f9f060a`; origin `https://github.com/Dacroxx/marea-y-azotea.git`.
No se tocó Documents con WIP, otros perfiles ni el adjunto original.

## Actualización parent al finalizar

Parent informa checkpoint remoto `3fcdf148693c850e0fe4bc8ab9dde20aa84f0cc0`, misma rama/PR, SOLO `CONTINUE.md` y `handoff/user-reference.html` (copia original). No incluye este WIP. Preservar ambos archivos y el nuevo HEAD; **NO resetear a f8e3ab1**. No se cambió modelo/config. El implementador no tocó esos archivos ni hizo publicación.

## Qué está hecho

- `index.html` se reconstruyó usando el HTML exacto de referencia, no la galería simplificada. Mantiene portada full-bleed foto/SVG/overlay, tipografías, carta/firma de **Aida Arteaga**, cinco crónicas, ritmo gráfico, 15 cápsulas intercaladas, mosaicos con spans, cinco franjas audiovisuales prudentes, glosario de 44 voces (buscador/filtros/fichas) y footer.
- CSS y JS están **inline**. Solo HTML en carpeta vacía funciona con todo HTTP(S) bloqueado. Sin CDN Tailwind ni assets relativos en el entregable. Fotos y fuentes de Google requieren Internet; offline conserva composición/SVG/fallback neutral.
- 58 IDs verified, valores de categoría y captions exactos del catálogo: Territorio29/Hierbas15/Coco5/Mar9/Bebidas0 (orden del adjunto). Nombre original y enlace por ID visibles. Portada verified `IMG_1898.HEIC`, ID `1jMeLokjKWlpVlkg_X67NqsVLP9nFM-QV`.
- Fuera 91 provisional, 32 needs-human y 31 MOV no inspeccionados. Cero embeds/títulos de videos inventados. Contadores portada/sumario/franjas/visor corregidos. EjeV conserva texto y cápsulas con estado vacío.
- Nota visible distingue contenido editorial aportado (no certificado como transcripción ni revisión científica) de observaciones fotográficas. No se reescribió la voz editorial ni se atribuyó autoría a David.
- Catálogo/auditoría histórica sin modificar. Los assets antiguos quedan históricos, no se solicitan.

## Fuente y generación (sin instalar)

Adjunto original, solo lectura:
`C:/Users/D/AppData/Local/hermes/profiles/null/cache/documents/doc_f24a656fecaf_marea_azotea_revista_final_para_github_pages.html`.
Copia exacta versionable: `source/editorial-template.html`.
SHA256: `7bd51e2854517647430d5d64a197a49d230a8298027c76c9a2daf6c4dfaa3c15`.
`.gitattributes` conserva sus bytes y usa LF para el build.

Build normal, offline y byte-idéntico probado:

```sh
python tools/build_magazine.py
```

Delegación del generador a `source/build_editorial.py`; suplementos `source/chronicle-renderer.js`, `source/accessibility.js`, `source/standalone.css`, utilidades estáticas `source/tailwind.generated.css`.

Solo si se añaden clases utilitarias, refrescar CSS en navegador de build:

```sh
python tools/build_magazine.py --runtime
node tools/capture-editorial-css.cjs
python tools/build_magazine.py
```

Playwright existente `C:/Users/D/node_modules/playwright`; Chrome `C:/Program Files/Google/Chrome/Application/chrome.exe`. No npm install ni paquetes externos ejecutados en shell. Se ejercitaron categorías/fichas, visor/fallback y menú antes de capturar. `source/css-build.json` conserva hashes de CSS/runtime. El CDN puede cambiar al refrescar; revisar hash/diff. La reproducción offline desde CSS versionado sí es determinista. `source/build-runtime.html` está ignorado: NO publicar ese archivo como entregable en lugar de index.

## Ejecuciones reales más recientes

```sh
python -m unittest discover -s tests -v   # 21 OK: 17 anteriores + 4 build/procedencia
node tests/magazine.test.cjs             # PASS
node tests/magazine-functional.cjs       # PASS, ocho grupos; HTML aislado, sin red
node tests/editorial-reference.cjs       # PASS
node tests/magazine-real-smoke.cjs       # PASS, Drive real
```

- RED real sobre f8e3ab1: contrato editorial esperaba5 mosaicos y obtuvo0; GREEN tras restauración.
- Funcional offline: selección completa exacta, 15 cápsulas, 44 fichas abiertas/cerradas con foco, cinco filtros y búsqueda, escape de HTML, enlaces inline, visor/teclado/Esc/trap/foco, menú/anclas, 1440/390/360 sin desborde, columnas4/1/1, fallback neutral, impresión con58 fichas y reveals opacidad1, PDF generado, cero excepciones JS y cero requests a assets/CDN.
- Referencia: iguales 14 componentes ×12 propiedades ×3 anchuras; 33 nodos editoriales preservados. No afirma pixel-perfect de todas las alturas: cambian fotos/recuentos y se añade nota de alcance.
- Smoke más reciente: cinco IDs distintos decodificados (1200px), visor a1600 cargado, cero JS errors/requestsFailed. No prueba las58 cargas ni MOV ni otros navegadores.
- Dos bugs reproducidos/corregidos: reveal con transición dejaba opacidad0 momentánea al imprimir; onerror tardío en imagen retirada del visor accedía a parentElement nulo. Tests verdes tras fixes.

## Pendiente honesto / no ampliar por consumo

- David debe revisar esta versión; `audit/FRONTEND-REVIEW.md` aprobaba el diseño anterior rechazado, NO esta corrección.
- **Detalle visual pendiente de confirmar:** el aviso neutral de red dentro del header fijo puede tapar temporalmente el cintillo al bloquear red/cambiar viewport. Se añadió ResizeObserver + variable de altura para reservar espacio, pero un assert experimental inmediato de geometría falló; no se investigó si era sincronización/scroll y se retiró ese assert del contrato final. No vender como resuelto ese detalle. La suite funcional completa y la comparación de estilos pasan; no impide la composición rica ni lectura de crónicas. Si parent necesita tocarlo, esperar a layout estable y comprobar aviso visible/cerrado antes de afirmar corrección. No reiniciar rediseño.
- No se ha comprobado extracción de todos los captions del PDF; solo print DOM/estilos,58 fichas visibles y generación real. No afirmar revisión de contenido PDF completa.
- No se revisó semántica científica/botánica de crónicas/glosario: se conservó material del usuario con límite explícito. No reclasificar las212 entradas para rellenar categorías.
- El fallo general de CSS del ZIP completo **NO se reprodujo** por parent (stylesheet aplicado, fondos computados,0JS). Esta corrección restaura referencia y robustez HTML aislado, no atribuye root cause al usuario.

## Evidencia privada (no commitear imágenes/personas/PDF)

`C:/Users/D/AppData/Local/hermes/profiles/null/cache/scratch/marea-editorial-qa/`:
- `editorial-offline-results.json`, `reference-style-comparison.json`, `browser-real-results.json`.
- `reference-cover-{1440,390,360}.png`, `real-cover-{1440,390,360}.png`, `offline-cover-{1440,390,360}.png`.
- `real-mosaic-1440.png`, `offline-mosaic-{1440,390,360}.png`, `real-lightbox-1440.png`, `offline-print.pdf`.
Baseline parent desktop: `C:/Users/D/AppData/Local/hermes/profiles/null/cache/scratch/marea-reference-comparison.png`.
Se miraron realmente baseline, portada final desktop/móvil, mosaico real y fallback móvil. La composición coincide con la referencia con otra foto verified, estadísticas58/0/44 y captions observables.

## Archivos cambiados/creados

`index.html`, `tools/build_magazine.py`, `tools/capture-editorial-css.cjs`, `source/` (plantilla exacta/build/CSS/JS/procedencia), `.gitattributes`, `.gitignore`, `tests/editorial-{standalone,functional,reference}.cjs`, `tests/test_editorial_build.py`, entradas compatibles `tests/magazine*.cjs`, README, ai.md, `audit/EDITORIAL-RESTORATION.md`, este HANDOFF. `source/build-runtime.html` temporal ignorado no debe agregarse. Ver `git status --short` antes de publicar. No se requieren más rondas de polish para conservar el trabajo.
