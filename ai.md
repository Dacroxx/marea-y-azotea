# Continuidad para modelos y colaboradores — Marea & Azotea

## Estado vigente — implementación local de la revista

**Esta sección actualiza y prevalece sobre los pendientes del handoff histórico que sigue.** David autorizó adaptar el index real a los cinco ejes, usando solo fotos `verified`, sin esperar a resolver todas las propuestas del catálogo. La aceptación de esta entrega es una revista revisable sobre esa selección, no la clasificación definitiva de los 212 medios ni un cierre de tareas.

- Implementación entregada para revisión en la rama `audit/thematic-draft` del fork, junto con `assets/`, tests y documentación. Base anterior `f752169e9ccf3cadb96141d42aa1830a0e35a18f`; obtener SHA vigente con `git rev-parse HEAD` o GitHub, no confundirlo con la base de auditoría. No merge a dev/main ni deploy. Clon aislado local: `kanban/boards/david-inc/workspaces/t_ff5bf98a/repo`. No se tocó el WIP de `C:/Users/D/Documents/marea-y-azotea`.
- **`index.html` ya está implementado**, no es una maqueta documental. Cinco H2 exactos, navegación desktop/móvil, portada verified, carta editorial prudente, una apertura por eje, galería completa con seis filtros y conteos, estado vacío del eje Bebidas, visor `<dialog>` con flechas/Esc/cierre y restitución de foco, fallback neutral y enlaces Drive. Mantiene marca, fuentes y paleta editorial; CSS y JS locales, sin framework ni instalación.
- Selección: **58 IDs de fotos verified**, por categoría principal: Territorio 29, Hierbas 15, Mar 9, Coco/Fogón 5, Bebidas/Identidad 0. No deduplicación: los nombres repetidos no se confunden con IDs idénticos. Puede haber escenas repetidas. Cada descripción/alt es exactamente la del catálogo; nombres originales visibles y links por ID. Portada: `1jMeLokjKWlpVlkg_X67NqsVLP9nFM-QV`, `IMG_1898.HEIC`, Territorio.
- Se mantienen **fuera de la revista** 91 provisional, 32 needs-human y 31 MOV uninspected-video. Catálogo completo enlazado como metadatos de auditoría; ni su JSON/CSV ni el inventario/evidencias se modificaron. `verified` no es certificación de recetas, especies, historias o identidad ni revisión exhaustiva por terceros.
- Se retiraron el editor `Personalizar`, cargas de archivos y el glosario anterior de recetas/especies no sustentadas. No hay almacenamiento ni promesa de guardar cambios. Imprimir/PDF prepara la selección completa (aunque exista filtro activo) y usa impresión del navegador; no guarda una revista editable. Ctrl+P depende también del tiempo de carga de la red; revisar la vista previa antes de guardar.
- Fuente del markup: `tools/build_magazine.py`; ejecutar `python tools/build_magazine.py` después de cambiar plantilla o selección autorizada. `assets/magazine.css` y `.js` son locales; los medios se solicitan por URL de miniatura de Drive y las fuentes a Google. Funciona por `file:` y servidor estático. Ver comandos y límites en README.

### Verificación ejecutada

- **TDD RED:** `node tests/magazine.test.cjs` falló contra el index original: cinco H2 esperados frente a lista vacía. **GREEN:** pasa tras la implementación. El parser de auditoría tuvo su propio RED (`0 != 58`) y GREEN al reconocer el manifiesto actual. Un defecto de fondo transparente de carga en galería también se reprodujo con assert de estilo y se corrigió.
- `python -m unittest discover -s tests -v`: **17 tests OK**. Se conservan conteos del snapshot histórico (50 refs = 47 fotos + 3 MOV), se prueba aparte el manifiesto actual de 58 fotos y sigue probado el parser legacy. `python tools/thematic_media.py validate`: 212 IDs, cobertura exacta, taxonomía, extensiones, nombres propuestos únicos y paridad CSV/JSON, con la evidencia privada existente.
- `node tests/magazine-functional.cjs`: **9 grupos de comprobaciones OK** en Chrome real con transporte de imágenes fixture explícito: todos los IDs/pies/alt/nombres/enlaces; filtros 58/29/15/9/5/0; nav en 1440/390/360 sin desborde; visor con teclado/foco y en móvil; print media con 58 tarjetas; botón impresión y fallback al abortar Drive. Sin excepciones JS. PDF fixture generado; lectura de texto posterior comprobó las descripciones de los 58 registros presentes, sin faltantes, en 23 páginas. Eso valida texto/layout, no carga fotográfica real del PDF.
- `node tests/magazine-real-smoke.cjs`: **OK con red Drive real**, al menos cinco IDs distintos cargados con dimensiones naturales válidas y la foto ampliada; sin excepciones JS ni solicitudes fallidas en esa ejecución. No equivale a comprobar la carga de las 58 fotos. Los 302 de Drive redirigen normalmente; el éxito se decide por imagen decodificada, no solo por status HTTP. La primera ejecución detectó que contar elementos repetidos no garantizaba cinco IDs distintos; se endureció la espera por ID y se volvió a ejecutar.
- Se inspeccionaron capturas reales de portada desktop/móvil, galería y visor. Detector Impeccable ejecutado una vez: aviso de Plus Jakarta Sans aceptado por identidad explícita; aviso de imagen vacía del visor corregido inicializando su src con la portada verified (no placeholder). Sin actualización de skill ni paquetes.
- Evidencia privada: `C:/Users/D/AppData/Local/hermes/profiles/null/cache/scratch/marea-magazine-qa/`: `browser-mock-results.json`, `browser-real-results.json`, `pdf-text-results.json`, `real-cover-1440.png`, `real-cover-390.png`, `real-cover-360.png`, `real-territorio-1440.png`, `real-gallery-1440.png`, `real-lightbox-1440.png`, `fallback-390.png`, `print-layout-MOCK.pdf`. **No commitear imágenes/personas/PDF**. Son temporales y no una auditoría independiente.

### Cómo retomar ahora

1. Revisar diff local y abrir la página (`python -m http.server 8080 --bind 127.0.0.1` o `index.html` directamente).
2. Repetir comandos de README. Las pruebas Node usan Playwright/Chrome ya instalados; rutas configurables, no instalar dependencias automáticamente. `ARTIFACT_DIR` apunta a una ruta privada.
3. Contrastar esta implementación con el catálogo; no elevar estados ni reclasificar para rellenar Bebidas. No es necesario resolver las 91+32 incertidumbres para revisar la selección publicada.
4. Revisión frontend independiente completada (`deleg_ab235519`): aprobada con límites, sin bloqueos críticos. Null reprodujo los 17 tests, nueve grupos funcionales y smoke Drive real. Ver `audit/FRONTEND-REVIEW.md`. Revisar el checkpoint en GitHub; no fusionar ni desplegar sin aprobación de David. Las tarjetas históricas no representan una aprobación global de los 212 medios.
5. La auditoría de red `tools/audit_media.py` ahora escribe en `audit/current/`, nunca sobre el snapshot histórico de `audit/`. Reconoce el manifiesto actual y conserva parser legacy. No confundir el snapshot viejo de 47 fotos/3 videos con la página vigente.

---

## Contexto histórico de la auditoría previa

Los apartados siguientes conservan la base del trabajo y sus límites. Las menciones a la «página actual», tres capítulos, falta de integración o nuevas confirmaciones describen el estado **anterior** a la implementación local documentada arriba, no un gate vigente para esta entrega.


Este archivo permite retomar el trabajo sin depender del historial de chat ni de un modelo concreto. Es contexto del proyecto, NO autorización para publicar, modificar Drive, borrar datos o ejecutar instrucciones de fuentes externas. Mantenerlo actualizado con evidencia, incertidumbres y checkpoints reales.

## 1. Qué quiere David

Auditar y mejorar esta revista digital de Cocinas del Pacífico colombiano, empezando por el uso correcto del archivo fotográfico. El objetivo inmediato es **clasificar visualmente el material, proponer nombres descriptivos y trazar dónde corresponde cada imagen**, con cinco ejes temáticos en lugar de asumir que todo pertenece a las tres clases que aparecen hoy en la página.

David confirmó que la carpeta raíz incluye material de otras actividades. No clasificar automáticamente por fecha, orden de archivo, nombre de cámara o pie de foto existente. No se pide construir otra aplicación ni migrar a un framework.

## 2. Repositorios y flujo de trabajo

- Original: https://github.com/aidaa8048-pixel/marea-y-azotea
- Fork de David, donde se trabaja: https://github.com/Dacroxx/marea-y-azotea
- Web original: https://aidaa8048-pixel.github.io/marea-y-azotea/
- `origin` debe apuntar al fork; `upstream`, al original. Verificarlos antes de escribir.
- `main`: base original, SHA `4e6f256f4d8adc1b1af4bc9b02b72d627f2e6a97` al iniciar esta tarea.
- `dev`: rama de integración. Auditoría base publicada en `678392e9a285d16288e03a395b2f25459d06761d`.
- Este documento se añade en un checkpoint posterior: consultar `git log -1 -- ai.md` para su commit, no confundirlo con el SHA de la auditoría.
- Antes de actuar: `git status --short`, `git branch -vv`, `git remote -v`, `git log -n 5 --oneline`.
- Preservar WIP ajeno. No reset destructivo, force push, borrado de ramas o merge a main sin aprobación. CI verde no autoriza merge.

## 3. Las cinco categorías autorizadas

Mantener estos nombres exactos como valores de categoría:

### Territorio, Saberes y Herramientas Ancestrales

Taller sensorial, la piedra de moler, el maíz, el plátano y preparaciones de base como los bolones o el Juan Valerio.

### Hierbas de Azotea y Aromas de la Selva

El universo aromático del Pacífico: chillangua, chirarán, poleo, pipilongo y refritos.

### Frutos del Mar, Río y Manglar

Pesca artesanal, pesca de manglar, piangua, jaiba, cangrejos, camarones y pescados de río y de mar.

### Coco, Tubérculos y Fogón

Leche de coco, encocados, tapao, atollados, pusandao, arroz clavado, yuca, ñame, papa china (achín) y amasijos.

### Bebidas, Cultura Viva e Identidad

Viche/biche, tradición oral, cantos de cocina, festividades (San Pacho, Petronio Álvarez) y cosmovisión de comunidades afrodescendientes e indígenas (Emberá y Wounaan).

### Criterios de asignación

- Una categoría principal por archivo, según el sujeto o proceso dominante, y categorías secundarias para cruces justificados.
- Ejemplo conceptual: un encocado de pescado puede cruzar Frutos del Mar y Coco/Fogón; no afirmar que una foto muestra encocado solo porque tiene pescado y salsa.
- Si no hay evidencia suficiente, categoría principal nula y estado pendiente. Eso NO crea una sexta categoría temática.
- Describir lo observable; no inventar plato, ingrediente, especie, fecha, evento, procedencia, identidad étnica ni historia de la clase.
- La carpeta de origen ayuda como contexto, pero no reemplaza mirar la imagen.

## 4. Fuente del archivo y hechos verificados

Carpeta de Drive autorizada para lectura:
https://drive.google.com/drive/folders/1Fqf4PVjly0UXCLWEN4zByLekWpJAmOPk?usp=sharing

Snapshot de auditoría: `audit/summary.json` (incluye fecha de comprobación). Visibles públicamente:

- 212 medios con IDs únicos: 181 fotos (149 HEIC y 32 JPG) y 31 MOV.
- Raíz: 149 medios.
- `cocinas del pacifico/clase 31 agosto`: 26 medios.
- `cocinas del pacifico/taller sensorial`: 37 medios.
- `cocinas del pacifico/clase cangrejos`: sin archivos públicamente visibles.
- Cuatro subcarpetas visibles en total; no confundir carpetas con medios.

La página actual utiliza 47 fotos y 3 videos. Los 50 IDs existen y sus nombres coinciden exactamente con Drive. En Taller Sensorial hay 13 fotos no referenciadas por la página; podrían ser omisiones o una selección editorial. Consultar `audit/REPORT.md` para sus nombres.

La auditoría por carpetas anterior es una **base histórica**, no la clasificación temática final. En particular, los valores antiguos `sensorial`, `agosto` y `pending-review` de `audit/media-catalog.csv` no son los cinco ejes nuevos.

## 5. Diagnóstico: qué está probado y qué no

- Las 47 URLs de miniaturas respondieron con imagen válida por HTTP.
- En una prueba real de Chrome headless sobre la web original cargaron la portada, las primeras ocho fotos sensoriales y 40 imágenes de la galería en el recorrido efectuado, sin excepciones JS ni solicitudes fallidas. La galería tiene 47 tarjetas; las restantes no se declararon rotas porque existe carga diferida.
- Por tanto, **no se reprodujo una rotura general de enlaces o permisos**. No reemplazar enlaces especulativamente ni afirmar que el problema de David ya se corrigió.
- Correspondencia editorial pendiente: un ID correcto no valida el pie. Por ejemplo, el texto de `IMG_1881.HEIC` habla de transformación en masas, algo no demostrado claramente por la captura examinada.
- La precisión del resto de los pies y el comportamiento en otros dispositivos requieren revisión.
- No se ha verificado la reproducción/audio de los videos.
- `Personalizar` modifica el DOM y usa URLs de objeto locales; no existe guardado persistente implementado. No presentar esos cambios como guardados en GitHub o Drive. El botón PDF invoca impresión del navegador, no guarda la revista editable.

## 6. Estado de la clasificación al escribir este handoff

La auditoría base está en `dev`. Esta rama `audit/thematic-draft` conserva el catálogo temático como **BORRADOR para auditoría, no aprobado globalmente y no incorporado a la web**. No fusionarla automáticamente a dev/main.

El especialista examinó las 181 fotos y miniaturas de los 31 MOV y generó catálogo/observaciones. Una revisión temporal independiente de 31 IDs encontró seis correcciones; fueron aplicadas por el especialista y Null abrió de nuevo las seis miniaturas y contrastó sus registros corregidos. Documentos: `audit/THEMATIC-INDEPENDENT-REVIEW.md` y `audit/THEMATIC-CORRECTIONS-RECHECK.md`. Esto NO equivale a revisión independiente exhaustiva. Una miniatura de MOV no equivale a ver el video.

Verificación posterior a las correcciones ejecutada por Null: 15 tests OK y validación de 212 IDs, cobertura exacta, taxonomía, extensiones, nombres únicos y paridad CSV/JSON. Hay 58 fotos verified, 91 provisional, 32 needs-human y 31 MOV uninspected-video. El gate automático de Kanban rechaza incluso solicitar revisión porque interpreta las incertidumbres como falta de clasificación completa. No falsear certezas, repetir intentos idénticos ni desactivar gates. Hace falta acordar la aceptación de una primera entrega provisional o resolver dudas con David antes del cierre formal; no se necesita repetir descarga ni reconstruir desde cero.

Coordinación existente, solo si se trabaja dentro de la instalación Hermes de David:

- Tablero: `david-inc` (usar argumento explícito).
- `t_ff5bf98a`: clasificación visual por `david-specialist`; debe pasar a revisión de `david-reviewer`.
- `t_b76dc508`: integración por Null; depende de que termine la clasificación revisada. No crear tareas duplicadas.
- Workspace local de clasificación: bajo el directorio de datos local de Hermes, `kanban/boards/david-inc/workspaces/t_ff5bf98a/`.
- Clon aislado: `repo/`; evidencia local: `visual-evidence/` con 212 miniaturas, 14 hojas y `map.json`, según checkpoint del especialista.
- En el clon aislado existen `tools/thematic_media.py`, `tests/test_thematic.py`, `audit/thematic-observations.tsv`, lotes `-02`, `-03`, `-04` y `audit/thematic-visual-matches.json`.
- El script anuncia comandos `python tools/thematic_media.py prepare | build | validate`; revisar su versión y entradas. `prepare` requiere Pillow y descarga miniaturas; `build`/`validate` también usan el mapa de evidencia local, no asumir que un clon remoto sin `visual-evidence` reproduce todas las pruebas.
- Esta rama conserva catálogo, observaciones, scripts, pruebas e informes textuales. Las miniaturas/hojas siguen privadas y locales. Un modelo remoto puede leer las descripciones pero debe recuperar miniaturas autorizadas para una nueva verificación visual; no afirmar haber visto imágenes solo por leer el JSON.

**Advertencia de concurrencia:** en el clon local compartido hay WIP previo en `index.html`, `docs/` y `tests/media.test.cjs`. No es parte del checkpoint de auditoría validado. No descartarlo, no atribuirlo a un arreglo probado y no mezclarlo en commits de catálogo. El especialista trabaja en un clon aislado; continuar con esa separación.

## 7. Entregable y aceptación de la clasificación

Archivos presentes como candidato de auditoría (no aprobación global):

- `audit/thematic-catalog.csv` y `.json` para TODOS los IDs del inventario.
- `audit/TAXONOMY.md`: ejes y criterios de desempate.
- `audit/THEMATIC-REPORT.md`: conteos calculados, límites y dudas concretas por ID.
- Scripts y pruebas reproducibles; observaciones trazables a miniatura/hoja/celda.

Campos mínimos por medio:

`sourceId`, `originalName`, `sourceFolder`, `mediaType`, `primaryCategory`, `secondaryCategories`, `visualDescription`, `proposedFilename`, `evidence`, `confidence`, `reviewStatus`.

Reglas:

- Conservar nombre original e ID; nombre descriptivo solo propuesto, extensión original y sufijo estable de ID para evitar colisiones.
- Estados: `verified`, `provisional`, `needs-human`, `uninspected-video`, `out-of-scope`. No elevar certeza para completar casillas.
- Igual nombre no demuestra duplicado. Igual hash de miniatura demuestra miniatura idéntica, no necesariamente original idéntico. No borrar duplicados.
- Verificar cobertura contra los 212 IDs de la base; si Drive cambia, registrar diferencia, no alterar silenciosamente la base.
- Verificar categorías válidas, nombres propuestos únicos, evidencia por fila y consistencia de CSV/JSON/reporte.
- Revisar semántica y muestra visual, no aprobar solo porque pasan tests.

## 8. Herramientas y reproducción

Proyecto actual: un único `index.html` con HTML/CSS/JS, Tailwind por CDN y fuentes de Google. No hay backend, gestor de medios ni instalación de dependencias del proyecto necesaria para abrirlo.

Auditoría base, Python estándar:

```sh
python tools/audit_media.py
python -m unittest discover -s tests -v
```

La primera orden lee Drive y regenera el snapshot: conservar resultados históricos si se necesita comparar cambios. En el checkpoint base pasaron cuatro pruebas; volver a ejecutar para el estado que se entregue.

Servidor local opcional:

```sh
python -m http.server 8080 --bind 127.0.0.1
```

Miniaturas públicas: `https://drive.google.com/thumbnail?id=ID&sz=w640` (o w1200). Drive devuelve JPEG incluso para muchos originales HEIC. Es posible descargar miniaturas para revisar sin bajar originales. Las hojas de contacto deben permitir leer el nombre/ID y observar detalles; ampliar imágenes ambiguas.

Pitfall de inventario: el HTML normal de Drive mostró solo las primeras 50 entradas de la raíz. La auditoría usó `embeddedfolderview?id=FOLDER_ID` recursivamente y obtuvo 150 entradas raíz, incluida una carpeta. No declarar totales a partir de aquella primera página truncada. Los resultados siguen limitados a visibilidad pública.

Pillow y Playwright estaban ya disponibles en el entorno local que hizo la revisión; no asumir que lo están en otro equipo. La herramienta de navegador inicial agotó tiempo; la comprobación efectiva se realizó con Playwright y Chrome instalados. No inventar resultados si una herramienta falla.

## 9. Límites y próximos pasos

1. Leer el catálogo borrador y los dos informes de revisión; no rehacer lo ya guardado.
2. Resolver con David las dudas semánticas y la aceptación de una entrega provisional, sin forzar clasificación. El bloqueo actual es del cierre formal, no pérdida de archivos ni falta de pruebas.
3. Presentar a David dudas específicas con imágenes/IDs, no pedirle repetir toda la clasificación.
4. Integrar catálogo, documentación y pruebas verificados en `dev`; comunicar SHA exacto y alcance.
5. Acordar la adaptación de secciones/galería de la web a los cinco ejes y precisar el síntoma de fotos que David observa antes de corregirlo.

No se autorizó renombrar/mover originales en Drive, alterar permisos, instalar dependencias, publicar originales o personas en nuevos artefactos públicos, modificar el repo original, desplegar ni fusionar a `main`. Las hojas/miniaturas permanecen locales; el catálogo de metadatos y este contexto sí pertenecen al fork. Nunca guardar credenciales ni conversaciones completas aquí.

## 10. Cómo mantener este archivo

Al terminar una etapa, actualizar únicamente el estado real: rama/SHA, rutas entregadas, pruebas ejecutadas con resultado, decisiones de David, dudas y siguiente paso. Separar siempre hechos observados, propuestas y pendientes. Un modelo nuevo debe poder continuar sin reconstruir la conversación y sin confundir una intención con algo realizado.
