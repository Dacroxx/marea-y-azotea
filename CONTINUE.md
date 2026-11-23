# CONTINUAR AQUÍ — Gemini, DeepSeek u otro modelo

## Checkpoint más reciente: restauración implementada, para revisión

Esta actualización prevalece sobre la descripción del trabajo activo que sigue. El implementador terminó; no queda un subagente editando este clon. Se restauró el diseño del HTML aportado, con CSS/JS inline, 58 IDs verified, 15 cápsulas y 44 voces. Null ejecutó personalmente 21 tests Python, contrato standalone, ocho grupos funcionales offline y smoke Drive real (cinco IDs distintos + visor), todos aprobados, y miró capturas de portada móvil y mosaico desktop. No se ha realizado una revisión independiente completa de esta nueva restauración ni una aprobación de David.

La implementación y las fuentes reproducibles se conservan en esta rama como candidato revisable, NO como página simplificada anterior. Consultar HEAD de la rama/PR para SHA exacto y HANDOFF.md para detalles. Pendiente no bloqueante para preservar el avance: confirmar posible solapamiento temporal del aviso de red con el encabezado al cambiar viewport; está registrado, no certificado resuelto. No iniciar otra reconstrucción ni clasificación. Siguiente acción: abrir el index autocontenido y revisar con David o un modelo sucesor, luego corregir puntualmente. No se ha cambiado de modelo, fusionado ni desplegado.

## Encargo vigente (prioridad sobre el handoff histórico)

David quiere terminar la revista **Marea & Azotea** y dejar los cambios revisables en SU fork, no solo documentos. La primera implementación fue rechazada porque simplificó demasiado la revista. El ZIP se mostró plano en su entorno.

**Autoridad visual y editorial:** `handoff/user-reference.html`, copia exacta del HTML que David adjuntó. Mantener portada, composición, colores, Playfair/Fraunces/Plus Jakarta, cinco crónicas, mosaicos, tarjetas intercaladas, glosario de 44 voces y créditos/voz del archivo. NO sustituir por una galería genérica. El texto editorial aportado no prueba lo que contiene cada foto; pies y asignaciones proceden del catálogo auditado.

Referencia SHA256: `7bd51e2854517647430d5d64a197a49d230a8298027c76c9a2daf6c4dfaa3c15` (verificar contra copia adjunta antes de editarla). Conservar original sin modificar; usar plantilla de trabajo separada.

## Dónde trabajar y revisar

- Fork de David: https://github.com/Dacroxx/marea-y-azotea
- Rama: `audit/thematic-draft`.
- PR existente hacia `dev`: https://github.com/Dacroxx/marea-y-azotea/pull/1 . Actualizar este PR; no crear otro por reflejo.
- Último checkpoint de implementación ANTERIOR a la restauración editorial: `f8e3ab15c76d2bad2456aeaa3f28aa165f9f060a`. No presentarlo como la versión corregida aprobada.
- La rama contiene la auditoría y `ai.md`; este archivo aporta el contexto nuevo que faltaba.
- No fusionar main/dev, desplegar, tocar original, mover/renombrar medios o cambiar permisos de Drive sin aprobación adicional.

## Qué se está corrigiendo ahora

1. Restaurar la estructura del HTML enviado por David, no reinterpretarla.
2. Incorporar exclusivamente los 58 registros `photo` con `reviewStatus=verified` de `audit/thematic-catalog.json`, por categoría principal exacta, con nombre original y `visualDescription` factual. No copiar captions literarios del adjunto si no describen la imagen.
3. Dejar fuera 91 fotos provisionales, 32 que requieren contexto humano y 31 MOV sin reproducir. No inventar categorías, videos, transcripciones, eventos ni especies para llenar espacios.
4. Distribución publicada por ID: Territorio29, Hierbas15, Mar9, Coco/Fogón5, Bebidas0. Conservar la crónica de Bebidas con un estado visual honesto sin fotos verificadas, no borrar la sección.
5. Actualizar conteos originales 78 fotos/18 videos del adjunto para no presentar material que se excluyó. Los 58 IDs pueden contener escenas repetidas; no afirmar 58 escenas únicas.
6. Entregar **index.html AUTOCONTENIDO**, CSS y comportamiento inline. Fuentes y fotos pueden necesitar Internet, pero abrir solo el HTML en un directorio vacío no debe perder diseño ni controles. No depender de `assets/` ni del compilador Tailwind CDN en la entrega final.
7. Mantener/validar navegación, glosario, mosaicos, visor/Esc/foco, móvil, impresión y fallback neutral. No atribuir todo error de imagen a permisos.

## Diagnóstico que no se debe inventar

Null descargó y extrajo el ZIP exacto de GitHub del checkpoint anterior: contenía index.html, assets/magazine.css y assets/magazine.js. Al abrirlo por file:// en Chrome los estilos se aplicaron (fondo coco, portada marea, sin errores JS). **El fallo de estilos de David no se reprodujo con la carpeta completa.** Sí se confirmó una diferencia grande de diseño frente al adjunto. Por eso se restaura su base y se elimina la fragilidad de assets separados. No culpar al navegador/usuario ni declarar una causa no probada.

## Estado local al preparar este relevo

Había un implementador temporal ACTIVO (`deleg_e1c3a53c`, subagente `sa-0-2063df22`) sobre un clon aislado. Se le pidió priorizar terminar o dejar checkpoint honesto por límite de uso. NO lanzar otro editor simultáneamente sobre el mismo clon.

Clon local: `C:/Users/D/AppData/Local/hermes/kanban/boards/david-inc/workspaces/t_ff5bf98a/repo`.

Al consultar git status había cambios locales en index, README, ai.md, generador y pruebas; además source/, tools/capture-editorial-css.cjs, tests/editorial-{reference,functional,standalone}.cjs y audit/EDITORIAL-RESTORATION.md. **Su existencia no demuestra que estén completos ni que sus pruebas pasen.** Leer el HANDOFF.md que deje el implementador y resultados reales antes de afirmar finalización. No sobrescribir sus cambios. No tocar `C:/Users/D/Documents/marea-y-azotea`: tiene WIP ajeno de un intento previo.

Si no se dispone de ese filesystem, comprobar la cabeza remota del PR: puede haberse publicado un checkpoint posterior a este documento. Si la restauración aún no está en remoto, partir de la referencia adjunta y del catálogo, no fingir haber recuperado cambios locales no disponibles.

## Verificación mínima antes de publicar la corrección

- Test RED frente al diseño anterior, GREEN al restaurar referencia.
- Copiar ÚNICAMENTE el index final a un directorio vacío, bloquear peticiones CSS/JS externas y comprobar estilos reales (fondos, tamaños, columnas, mosaicos); los fallbacks de imagen offline son esperables. No basta buscar nombres de clases en el código.
- Mirar capturas de referencia y resultado a 1440px y móvil390/360. Verificar parecido estructural, no solo que no se caiga.
- Fotos por ID y pie exacto del catálogo; glosario44; navegación, visor, teclado, menú y estados vacíos.
- Smoke con Drive real, imágenes decodificadas y visor. Separar evidencia mock/offline/real; no afirmar comprobar todas si solo se prueba una muestra.
- Validaciones Python/auditoría histórica preservadas. Revisar comandos actuales en README; no dejar scripts que regeneren la página simplificada anterior.
- Verificar diff, incluir todos los archivos necesarios, commit y push a la rama del fork. Leer de vuelta HEAD, index y PR por GitHub API antes de afirmar que David ya puede revisarlo.
- Actualizar ai.md, README y estado de relevo con lo realmente ejecutado y los límites, sin promesas.

## Herramientas locales ya disponibles

Node/Python, Pillow, Playwright `C:/Users/D/node_modules/playwright`, Chrome `C:/Program Files/Google/Chrome/Application/chrome.exe`. No instalar dependencias automáticamente. Hay un intento de capturar CSS Tailwind compilado de la referencia para integrarlo inline; leer su script antes de usarlo y verificar cobertura de clases dinámicas. El HTML de referencia tiene Tailwind CDN: conservarlo como fuente no significa dejar esa dependencia en la entrega final.

Drive autorizado para lectura: https://drive.google.com/drive/folders/1Fqf4PVjly0UXCLWEN4zByLekWpJAmOPk?usp=sharing . Inventario público212medios con ID. Nunca renombrar originales por los nombres propuestos sin permiso.

## Coordinación existente, si se usa Hermes

Tablero `david-inc`; no crear tarjetas ni grafos duplicados. `t_b76dc508` reúne implementación/integración; `t_ff5bf98a` conserva clasificación. El gate anterior bloqueó pasar a revisión por incertidumbres de fotos aunque David aceptó entrega provisional y después autorizó página solo con verified. No desactivar gates ni gastar reintentos idénticos: distinguir alcance de la página58verified del cierre semántico total212. Dejar checkpoint y PR revisable es más útil que más burocracia.

## Primer mensaje sugerido para el modelo sucesor

«Lee CONTINUE.md y ai.md del fork Dacroxx/marea-y-azotea, rama audit/thematic-draft, y la referencia handoff/user-reference.html. Retoma la restauración editorial, no la página simplificada. Comprueba si el implementador anterior sigue activo y qué cambios reales hay. Termina un index autocontenido fiel a la referencia, con solo fotos verified y pruebas reales. Actualiza el mismo PR#1 y reporta SHA, cómo abrirlo y límites. No despliegues ni toques main/Drive.»
