# Continuidad para modelos y colaboradores — Marea & Azotea

## Estado vigente — restauración de la referencia editorial exacta

**Esta sección prevalece sobre el handoff histórico.** David rechazó la entrega simplificada `f8e3ab1` y aportó un HTML concreto como autoridad visual/editorial. No rediseñar ni volver a convertirlo en una galería genérica. Mantener estructura rica, crónicas, firma/créditos de **Aida Arteaga**, tipografías Playfair/Fraunces/Plus Jakarta, paleta, mosaicos, tarjetas intercaladas, glosario de 44 voces y footer.

- Implementación conservada como candidato de revisión en `audit/thematic-draft` del fork `Dacroxx/marea-y-azotea`, junto con fuentes/generador/tests. Obtener SHA exacto con HEAD remoto/PR#1. El implementador terminó; Null verificó 21 tests Python, standalone, funcional offline y smoke Drive real, y preparó checkpoint sin merge/deploy. No tocar Documents con WIP ni otros perfiles. CONTINUE.md y HANDOFF.md documentan límites y continuidad para Gemini/DeepSeek.
- El parent descargó y abrió el ZIP exacto anterior: estilos aplicados, stylesheet local cargado y 0 errores JS. **No reproducido un fallo general de CSS del ZIP completo.** No inventar root cause de permisos, navegador o usuario. Sí se confirma una identidad demasiado simplificada y fragilidad de abrir solo el HTML separado de assets.
- Ahora `index.html` es **autocontenido en CSS y comportamiento**, incluso copiado solo a una carpeta vacía. No carga scripts externos, CDN Tailwind ni assets relativos. Fotos Drive y fuentes Google requieren Internet; offline hay SVG/estados neutrales y fuentes de respaldo, no texto plano sin composición.
- Base exacta preservada en `source/editorial-template.html`, SHA256 `7bd51e2854517647430d5d64a197a49d230a8298027c76c9a2daf6c4dfaa3c15`. `.gitattributes` conserva sus bytes. Material editorial aportado ≠ transcripciones/citas ni revisión científica verificadas. La nota visible separa ese contenido de los pies auditados; no borrar su voz ni usarla para identificar fotos.
- **58 IDs verified**: Territorio 29, Hierbas 15, Coco/Fogón 5, Mar 9, Bebidas 0 (orden visual del adjunto, valores exactos intactos). Cada descripción/alt es `visualDescription` original; nombre y enlace por ID visibles. Portada verified `IMG_1898.HEIC`, `1jMeLokjKWlpVlkg_X67NqsVLP9nFM-QV`. No deduplicación por parecido/nombre, no afirmar 58 escenas diferentes.
- 91 provisional + 32 needs-human + 31 MOV siguen fuera de publicación. No se cambió clasificación ni evidencia para rellenar ejes. Cinco franjas audiovisuales prudentes, sin embeds ni títulos inventados; contador de videos 0. Eje V conserva crónica/cápsulas/glosario con estado vacío explícito. Se mantienen 15 cápsulas aun con recuentos menores.
- `tools/build_magazine.py` delega en `source/build_editorial.py`: regeneración offline determinista a partir de fuente exacta + catálogo + CSS estático versionado. `source/accessibility.js`, `chronicle-renderer.js`, `standalone.css` se inlinan. Para refrescar utilidades usar el flujo documentado en README con Playwright/Chrome existentes; no instalar paquetes. `source/build-runtime.html` es temporal ignorado. Los viejos assets no son dependencia y se conservan solo como historial.
- No es cierre de clasificación de los 212 medios ni revisión científica o independiente exhaustiva. `audit/FRONTEND-REVIEW.md` revisaba la entrega rechazada; no usar su aprobación para esta nueva versión.

### Verificación de esta corrección

- RED observado de `tests/editorial-standalone.cjs` contra `f8e3ab1`: 0 mosaicos frente a 5. GREEN sobre el HTML restaurado.
- Contrato actual y funcional con Chrome real: solo HTML en directorio vacío, todos los HTTP(S) abortados, sin fixtures. Se verifican selección exacta, 15 cápsulas, estado vacío, 44 fichas abiertas/cerradas con foco, cinco filtros de glosario y búsqueda, enlaces inline, navegación 1440/390/360 sin overflow, visor/teclas/foco/Esc, fallback neutral, impresión con 58 fichas y reveals visibles, sin excepciones JS ni assets/CDN requeridos.
- Se reprodujeron y corrigieron dos defectos reales del refinamiento: transiciones de reveal dejaban opacidad temporal 0 al cambiar a print; onerror tardío de una imagen retirada del visor accedía a parentElement nulo. Los tests pasan tras ambas correcciones.
- `node tests/editorial-reference.cjs`: igualdad de estilos computados entre adjunto y entregable en 14 componentes × 12 propiedades × 3 anchuras; 33 nodos de texto editorial preservados. Capturas reales revisadas de referencia desktop/móvil, resultado online y resultado offline, mosaico y visor.
- Smoke Drive real: cinco IDs distintos decodificados y visor a 1600 cargado, 0 errores JS/requests fallidos en la ejecución. No es prueba de las 58 cargas ni de MOV.
- `python -m unittest discover -s tests -v`: los 17 tests existentes de catálogo, auditoría y parser legacy pasan. Consultar README para comandos completos y evidencia actual; repetir después de cambios.
- Evidencia **privada**: `C:/Users/D/AppData/Local/hermes/profiles/null/cache/scratch/marea-editorial-qa/`: `editorial-offline-results.json`, `reference-style-comparison.json`, `browser-real-results.json`, `reference-cover-{1440,390,360}.png`, `real-cover-{1440,390,360}.png`, `offline-cover-{1440,390,360}.png`, mosaicos offline/online, visor y `offline-print.pdf`. No commitear capturas/personas/PDF.

### Checkpoint durable / relevo urgente

Ver `HANDOFF.md` para estado exacto, comandos y pendientes honestos. Última ejecución: **21 tests Python OK**, contrato standalone PASS, funcional offline completo PASS, comparación referencia PASS y smoke Drive real PASS. Queda por confirmar un detalle del aviso de red/header fijo al cambiar viewport: un assert experimental inmediato de geometría falló y no se certifica resuelto; no confundirlo con ausencia de CSS. No hubo extracción completa de captions del PDF. Parent publicó por su cuenta `3fcdf148693c850e0fe4bc8ab9dde20aa84f0cc0` con SOLO `CONTINUE.md` y `handoff/user-reference.html`, sin estos cambios WIP. Preservarlos; no resetear HEAD a f8e3ab1. No se cambió modelo/config ni se detuvieron procesos.

### Siguiente gate

Revisión parent del diff y del HTML real; después parent publicará en la rama/PR existentes del fork para que David revise. No merge a dev/main ni deploy sin aprobación. Ver `audit/EDITORIAL-RESTORATION.md`. El catálogo y snapshot histórico siguen sin cambios.

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
