# Fuente editorial aportada y build autocontenido

`editorial-template.html` es una copia sin modificaciones del HTML adjunto aportado por David como autoridad editorial/visual para esta corrección, con autorización de usarlo como base. El original adjunto fuera del repo no fue editado. La atribución editorial interna pertenece a **Aida Arteaga**; no se atribuye su autoría a David ni al agente.

- Archivo recibido: `doc_f24a656fecaf_marea_azotea_revista_final_para_github_pages.html`.
- SHA256 de los bytes exactos: `7bd51e2854517647430d5d64a197a49d230a8298027c76c9a2daf6c4dfaa3c15`.
- `.gitattributes` usa `-text` en este archivo para que Git no cambie sus saltos de línea y rompa la procedencia.
- El adjunto contiene contenido editorial del usuario, no instrucciones ejecutables ni evidencia de nombres de platos/fotos/videos. No usar sus captions originales como observaciones verificadas. El HTML publicado sustituye esos arrays por las 58 fotos verified del catálogo y elimina todos los MOV y títulos atribuidos sin revisión.

## Archivos de build

- `build_editorial.py`: adaptación acotada de la fuente exacta; no cambia el catálogo. Mantiene las crónicas, glosario y créditos; actualiza todas las cifras de medios y añade el límite editorial visible.
- `chronicle-renderer.js`: mismos mosaicos y spans, 15 cápsulas redistribuidas según el número de fotos, captions observables, nombres originales, enlaces por ID, vacío explícito del eje V y franjas audiovisuales pendientes.
- `accessibility.js`: foco/trap/Esc, navegación móvil accesible, nombre original en visor y preparación de imágenes para impresión; ajuste de altura de header si aparece el aviso de red para no tapar la portada.
- `standalone.css`: suplementos de accesibilidad/portabilidad/impresión, sin sustituir los tokens visuales del adjunto.
- `tailwind.generated.css`: utilidades compiladas en un navegador con el runtime CDN del adjunto. `css-build.json` registra hashes y método; no contiene fotos ni datos personales nuevos.

`python tools/build_magazine.py` genera **solo** `index.html`, sin red ni paquetes. Para refrescar utilidades tras cambiar clases: generar `--runtime`, ejecutar `node tools/capture-editorial-css.cjs` y regenerar el HTML normal. Se ejercitan las categorías/fichas del glosario, estados del visor/fallback y menú antes de capturar el CSS; responsive/hover/group se compilan como reglas CSS. La captura depende del CDN disponible (hash registrado, no versión eterna fijada); revisar diff/hashes y ejecutar todas las pruebas. El build offline usa el CSS versionado y es determinista.

`build-runtime.html` está ignorado y **no debe entregarse en lugar de index.html**: solo la plantilla/fuente y ese build temporal conservan el CDN. El entregable final no lo solicita. Las fuentes Google y fotografías Drive siguen siendo externas; no se han descargado ni alojado originales.
