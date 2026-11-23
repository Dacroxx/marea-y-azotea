# Revista implementada — entrega para revisión

## Qué cambió

- `index.html` real reorganizado en los cinco ejes solicitados por David.
- Selección de 58 IDs de fotos `verified`; no es una selección de 58 escenas distintas. No se deduplican visualmente los IDs.
- Por eje: Territorio 29, Hierbas 15, Mar 9, Coco/Fogón 5 y Bebidas 0. El eje sin fotos presenta un estado vacío honesto.
- Portada verificada, apertura por eje y galería completa con filtros, nombres originales, pies factuales y enlaces por ID a Drive.
- Visor accesible nativo con flechas, cierre, Escape y restauración de foco. Navegación adaptable y estilos de impresión de la selección completa.
- CSS/JS locales en `assets/`; ya no depende del compilador Tailwind CDN. Fuentes e imágenes requieren Internet.
- Retirados editor sin persistencia y glosario no sustentado; no se promete guardar cambios ni se implementó un CMS.
- Catálogo de 212 medios, estados y snapshots históricos preservados. Las nuevas auditorías de red escriben en `audit/current/`.

## Verificación ejecutada por Null

- `python -m unittest discover -s tests -v`: 17 tests aprobados.
- `node tests/magazine.test.cjs`: contrato de cinco ejes y selección verified aprobado.
- `node tests/magazine-functional.cjs`: nueve grupos aprobados, con imágenes fixture explícitamente simuladas: contraste de todos los IDs/pies/alt/nombres/enlaces, filtros y conteos, visor/teclado/foco, navegación a 1440/390/360 px, móvil, impresión y fallback con requests abortadas. Sin excepciones JS.
- `node tests/magazine-real-smoke.cjs`: red Drive REAL, al menos cinco IDs distintos decodificados y una foto ampliada cargada; sin excepciones JS ni solicitudes fallidas durante esa ejecución. No prueba las 58 cargas ni otros navegadores.
- `python tools/build_magazine.py`: regeneración de la revista completa desde el catálogo. `git diff --check` sin errores.
- Inspección visual de capturas reales de portada móvil y galería desktop: carga y composición legibles, sin problema evidente de desborde en las capturas. No equivale a revisar todas las fotografías.

El especialista también documentó el RED contra el HTML anterior antes de implementar, el GREEN y la comprobación de texto/layout del PDF fixture. No confundir PDF con imágenes simuladas con prueba de disponibilidad real de fotos de Drive.

## Revisión independiente del frontend

Revisor temporal de solo lectura, separado de la implementación (referencia local `deleg_ab235519`). Dictamen: **aprobado con límites, sin hallazgos críticos bloqueantes**.

- Leyó generador, JS/CSS, tests y adaptación del parser; contrastó los 58 registros exactos con el catálogo y los cinco títulos.
- Revisó escapado HTML y protección contra cierre de script, ausencia de persistencia ficticia y preservación de snapshots.
- Ejecutó contrato por `file://` y comprobación adicional por HTTP a 360 px: assets/documentos enlazados HTTP200, filtros vacío/mar, Escape y devolución de foco, 58 tarjetas en impresión incluso con filtro vacío y contenido disponible sin JavaScript.
- No repitió el smoke Drive ni los nueve grupos completos; esas verificaciones fueron ejecutadas por Null. No se atribuye a la revisión independencia de proveedor/modelo ni cobertura exhaustiva.

## Límites que debe conocer David

1. Las 91 fotos provisionales, 32 pendientes de contexto humano y 31 MOV no reproducidos siguen fuera de la revista. No se rellenó Bebidas con material no confirmado.
2. `verified` se refiere a sujeto y eje amplio, no certifica receta, especie, identidad, ancestralidad o procedencia.
3. Hay escenas repetidas con IDs distintos. El catálogo conserva procedencia y nombres; resolver selección/deduplicación editorial puede ser una siguiente mejora.
4. Drive sigue siendo dependencia externa. La impresión por botón espera como máximo diez segundos; Ctrl+P no garantiza que todas las descargas terminen. Revisar vista previa del PDF.
5. No se afirma un focus trap estricto: Chromium puede intercalar foco en BODY antes de volver al diálogo; en la prueba independiente no alcanzó controles del contenido subyacente. Escape/restauración funcionan.
6. La entrega incluye `index.html` MÁS `assets/`. No copiar únicamente el HTML. GitHub muestra código: descargar/extraer la rama y abrir el index, o servirla localmente.
7. No se ha desplegado ni fusionado a dev/main; original y Drive no fueron modificados. Esta es una entrega para revisión, no una publicación final.

## Revisión humana sugerida

Abrir README y la revista, recorrer los cinco ejes, probar la galería en móvil, evaluar la selección y reportar fotos/IDs que deban cambiar de sección. Los nombres descriptivos son propuestas documentadas; no se aplicaron a Drive. El `ai.md` permite continuar con otro modelo sin reconstruir el chat.
