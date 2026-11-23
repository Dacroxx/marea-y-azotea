# Restauración de la referencia editorial — verificación local

## Diagnóstico y alcance

El parent descargó y abrió el ZIP exacto de la entrega anterior desde GitHub: Chrome aplicó `assets/magazine.css`, fondos computados no blancos y cero errores JavaScript. **No se reprodujo una rotura general de estilos del ZIP completo.** No se atribuye el problema a permisos, navegador o usuario. La entrega sí había reducido en exceso la identidad del HTML que David aportó después. Esta corrección usa ese adjunto como base exacta y hace que abrir **solo el HTML** no dependa de assets vecinos.

Se conservan portada full-bleed, foto/SVG, superposición tipográfica, paleta, tres tipografías editoriales, carta/firma y créditos de Aida Arteaga, cinco crónicas extensas, separadores, mosaicos con spans, 15 cápsulas, cinco espacios audiovisuales, glosario de 44 voces con filtros/buscador/fichas y footer. No se presenta el texto aportado como evidencia fotográfica, transcripción verificada o revisión científica; una nota visible distingue los ámbitos.

Solo aparecen 58 IDs de fotos verified por categoría principal: 29 Territorio, 15 Hierbas, 5 Coco/Fogón, 9 Mar, 0 Bebidas (orden visual del adjunto). Cada pie y alt conserva exactamente `visualDescription`, nombre original y enlace por ID. La portada verified es `IMG_1898.HEIC`. Se mantienen fuera 91 provisional, 32 needs-human y 31 MOV no inspeccionados. No hay iframes/videos publicados ni títulos de escenas inventadas; todos los contadores audiovisuales indican cero. El eje V conserva voz y tarjetas con vacío fotográfico explícito.

## Pruebas y hallazgos

- **RED antes de implementación:** `node tests/editorial-standalone.cjs` contra `f8e3ab1` falló con 0 mosaicos frente a 5. **GREEN:** cinco mosaicos, 44 entradas y 58 fotos; cuatro columnas desktop incluso sin red.
- **HTML aislado:** la prueba funcional crea un directorio vacío, copia solo `index.html`, bloquea todo HTTP(S) y usa Chrome real, sin fixtures. Revisa selección completa, captions/alt/nombres/enlaces exactos, 15 cápsulas, vacío del quinto eje, 44 fichas abiertas/cerradas con foco, filtros de categorías, búsqueda y escape de HTML introducido en el buscador, enlaces inline, visor/Esc/flechas/trap/retorno de foco, menú y cinco anclas.
- **1440/390/360:** columnas 4/1/1, fondos y tamaños monumentales presentes, sin desborde horizontal. Offline conserva SVG y fallback neutral; no atribuye automáticamente los fallos a permisos. CSS y JavaScript inline, ninguna petición a assets relativos ni al CDN.
- **Comparación contra el adjunto real:** igualdad computada de 14 componentes × 12 propiedades × tres anchuras (colores, fuentes, tamaños, pesos, display, columnas, gaps, padding horizontal y radios). Se preservan además 33 nodos de texto editorial seleccionados de carta/crónicas/footer. No es una afirmación de pixel-perfect de toda la página: cambian las fotos, los conteos y la altura de mosaicos según la selección; las notas de alcance y accesibilidad se añaden explícitamente.
- **Inspección visual real:** portada desktop mantiene la composición de referencia con otra foto verified; móvil conserva masthead, jerarquía, botones y ritmos. Mosaico real presenta spans grandes/pequeños y cápsulas de color intercaladas, con pies observables y nombres. Offline conserva la composición aunque no pueda mostrar fotos/fuentes de red.
- **Impresión:** se generan PDF offline y se verifica en media print que las 58 fichas están visibles, todos los reveals tienen opacidad 1 y controles ocultos. No es evidencia de fotos cargadas. La prueba reprodujo opacidad temporal 0 debido a transiciones al entrar en print; se corrigió desactivando transiciones en impresión.
- **Race real de errores de imagen:** al navegar deprisa por el visor con red bloqueada, un `onerror` tardío accedía al padre de una imagen ya retirada. Se reprodujo y se corrigió con acceso opcional; la prueba funcional pasa sin excepciones.
- **Drive real:** smoke sin sustitución de imágenes, cinco IDs distintos con dimensiones naturales válidas y foto ampliada cargada; cero excepciones JS y cero solicitudes fallidas en esa ejecución. No certifica las 58 imágenes, los MOV ni otros navegadores.
- **Auditoría:** los 17 tests Python existentes pasan, conservando catálogo de 212 registros, paridad, evidencia privada disponible, parser legacy y snapshot histórico. No se reclasificó ni sobrescribió la auditoría para acomodar el diseño.

## Reproducibilidad y límites

El adjunto exacto está en `source/editorial-template.html`, SHA256 `7bd51e2854517647430d5d64a197a49d230a8298027c76c9a2daf6c4dfaa3c15`. El generador reconstruye offline `index.html` a partir de esa base, catálogo y CSS/utilidades versionados. El refresco opcional de CSS usa Playwright/Chrome ya instalados y Tailwind en un navegador de build, sin instalar ni ejecutar paquetes externos en shell. El entregable final no usa ese runtime. Ver `source/README.md` y README raíz.

Evidencia privada (fuera de Git): `C:/Users/D/AppData/Local/hermes/profiles/null/cache/scratch/marea-editorial-qa/`, con JSON de pruebas, comparación computada, capturas referencia/resultado 1440/390/360, mosaicos, visor y PDF offline. No commitear capturas de personas ni PDFs. `audit/FRONTEND-REVIEW.md` es histórico y no aprueba esta nueva entrega.

Estado: **cambios locales para revisión parent**; este implementador no hace commit, push, PR, merge ni deploy. No se tocó el clon Documents con WIP, el adjunto original fuera del repo ni otros perfiles. La clasificación global de los 212 medios y la revisión de afirmaciones editoriales siguen abiertas.
