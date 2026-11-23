# Autocontrol previo a revisión

## Subsanación acotada tras revisión independiente

Fuente: informe de solo lectura de deleg_f32395bd, conservado íntegro en audit/THEMATIC-INDEPENDENT-REVIEW.md. La muestra independiente cubrió 31 IDs (28 fotos y 3 miniaturas MOV), no los 212. Dictamen original: cambios requeridos; NO aprobación global. En esta reanudación se abrieron realmente con vision_analyze las seis miniaturas por ID y se contrastaron las correcciones; esto es autocontrol del implementador, no segunda revisión independiente.

- 1ZLqcN5pVMJqFhShFm3URppR7cQMMD53R (número 71): molino manual metálico con granos claros/amarillentos en tolva. Se corrigieron descripción y prefijo a molino-metalico-granos-claros; primaria pasa del eje 4 al 1, conservando provisional/medium y sin acreditar ancestralidad ni ingrediente.
- 1TjpiB96VVCi8Hz8PHamIOX0ih8k2YKQd y 1Xyx9QkNFauXQsVG9_5T_W2pZy4qOJHxS (26 y 158): tallos y hojas verdes sobre piedra; se elimina la afirmación de vainas y se usa tallos-hojas-sobre-piedra. Eje 1/provisional/low intacto.
- 1Go3kmI7JbNLSFuw32ZQGUKMZH6uUFrRA y 1i5R9Z88aIrSZs1ADTfp3aF4uyPtxvH6f (57 y 125): pasta clara en mortero metálico, bol de vegetales blancos/verdes. Se corrige color, manteniendo eje 2/verified/high para sujeto amplio, no autenticidad cultural.
- 1C7r_LcmfzuioltWf5e2YMyeg54j0-S8Y (4): prefijo neutral mezcla-amarilla-fragmentos-sarten; no confirma hierbas. Eje 2/provisional/medium intacto.

Se corrigieron TSV fuente; 125 y 158 heredan de 57 y 26 mediante coincidencias visuales previamente documentadas, con evidencia individual preservada. Se regeneraron JSON de observaciones, CSV/JSON de catálogo, resumen e informe. Sufijos de ID y extensiones originales preservados. Sin nuevas descargas ni reproducción de MOV, sin push, Drive o web. No se modificó el clon compartido.

Verificación de subsanación: build y validate OK; 14 pruebas originales OK (incluida reconstrucción offline byte-idéntica), y ejecución final de 15 pruebas OK al añadir test_independent_review_six_corrections para los seis IDs. Conteos generados: 212 IDs, 181 fotos/31 MOV; ejes 1=73, 2=19, 3=11, 4=38, 5=8 y null=63. Estados sin cambio: 58 verified, 91 provisional, 32 needs-human, 31 uninspected-video. La integración sigue pendiente de gate de revisión, no se declara aprobación global. El bloque de continuidad inferior permanece válido en cobertura/estados; debe acompañarse de esta subsanación y de su revisión posterior al actualizar ai.md.

Tarea t_ff5bf98a. Se reutilizó la inspección visual completa documentada por el intento 11 y conservada en los TSV y thematic-visual-matches.json, conforme a la indicación expresa de Null de no repetir la descarga ni inspección completa. En la reanudación se generaron y validaron todos los entregables. No se afirma una segunda inspección completa independiente.

## Contraste visual sustantivo en esta reanudación

Se abrieron con vision_analyze las hojas locales sheet-01.jpg y sheet-03.jpg y se contrastaron con las anotaciones del catálogo. Evidencia local en ../visual-evidence/map.json; no se adjuntan imágenes.

- Hoja 01, celdas 1–3: bocados dorados con cobertura blanca; no permite certificar coco o preparación específica. Se conserva eje 4 provisional.
- Hoja 01, celda 4: mezcla amarilla húmeda, fragmentos verdes/rojizos en sartén. No certifica hierbas específicas ni refrito. Eje 2 y secundario 4 son propuesta provisional, no verified.
- Hoja 01, celdas 5–6: caparazón, patas y pinzas de crustáceo sostenido. Eje 3 verified es defendible para sujeto amplio; no certifica especie ni lugar de captura.
- Hoja 01, celdas 7–11: platos con granos y preparaciones amarillas, arroz blanco y láminas amarillas. Se conserva clasificación provisional y no se atribuye leche de coco.
- Hoja 01, celdas 12–13: piezas alargadas en salsa amarilla/anaranjada, compatibles con pescado pero no concluyentes en la hoja. Se conserva «parecen pescado», provisional, sin identificar receta ni especie.
- Hoja 01, celda 14: grupo en cocina sin sujeto temático concluyente. Null y needs-human son apropiados.
- Hoja 01, celdas 15–16: recipientes, utensilios, hojas y objetos sobre mesa. Encaje amplio en herramientas; no prueba ancestralidad ni actividad concreta.
- Hoja 03, celda 1 (número 33): hojas, mazorca seca y pequeños objetos/recipiente. La referencia amplia a maíz/herramientas es visible, no demuestra uso ritual ni especie botánica de las hojas.
- Hoja 03, celdas 2 y 6: frutos rojos en cesta; no se asigna especie. La composición mixta de celda 2 sigue provisional; el acercamiento de celda 6 sin vínculo suficiente queda null.
- Hoja 03, celda 3: cesta y utensilios alargados sobre mesa, con manos trabajando al fondo. No se atribuye receta.
- Hoja 03, celdas 4–5 y 8–12: mortero de apariencia de madera con mano, recipientes oscuros y fondo de cocina. El sujeto herramienta justifica eje 1 amplio; no acredita procedencia ancestral.
- Hoja 03, celda 7: recipiente oscuro a contraluz y grupo al fondo. Detalle insuficiente, por eso la asignación sigue provisional.
- Hoja 03, celdas 13–14: hojas/tallos en cesta, sin especie verificable. Eje amplio de hierbas, no identidad botánica.
- Hoja 03, celdas 15–16: tejido geométrico amarillo y oscuro. Se conservó provisional/medium tanto en los TSV fuente como en sus coincidencias visuales 180–181; no se infiere etnia, ancestralidad ni procedencia.

No se observó contradicción que justificara elevar confianza. Los casos débiles siguen como propuestas explícitas o sin categoría. Esta comprobación no convierte la opinión del mismo agente en evidencia independiente. El revisor debe contrastar las hojas restantes y cuestionar el encaje de utensilios genéricos, hierbas y cultura viva; la taxonomía amplia no autentica atribuciones culturales.

## Bloque propuesto de actualización para ai.md (no aplicado)

Clasificación local generada sobre base 678392e: audit/thematic-catalog.csv y .json cubren 212 IDs únicos (181 fotos, 31 MOV). Estados: 58 verified de sujeto/eje amplio, 91 provisional, 32 needs-human y 31 uninspected-video. Los MOV no se reprodujeron. Taxonomía, preguntas por IDs, observaciones y evidencia trazable acompañan el catálogo. Pasan 14 pruebas, incluida reconstrucción offline byte-idéntica y hashes locales. No se modificó Drive, web ni remotos. Revisión sustantiva david-reviewer es el siguiente gate antes de integración. Preservar ai.md publicado por Null en origin/dev afacda1d3ffda6c9463552a5b13890fcb8a1e317; ese cambio remoto es comunicado por Null, no fue descargado/verificado en este clon y no invalida la base local. Imágenes y hojas exclusivamente locales.

## Pruebas realmente ejecutadas

`python -m unittest discover -s tests -p 'test*.py' -v`: 14 pruebas OK. Incluyen reconstrucción offline byte-idéntica de CSV/JSON/observaciones/resumen/informe, cobertura exacta de 212 IDs, 181 fotos y 31 vídeos, hashes de miniaturas locales, mapa hoja/celda, extensiones, nombres únicos y paridad CSV/JSON. Las pruebas negativas rechazan categoría desconocida, evidencia alterada, ID faltante y extensión alterada.

`git diff --exit-code`: OK, archivos previos versionados intactos. HEAD base 678392e9a285d16288e03a395b2f25459d06761d. Entregables nuevos sin commit, sin push ni cambios remotos. Ningún MOV reproducido; las miniaturas no validan contenido temporal/audio. No se aplicó ningún nombre propuesto a Drive ni se modificó la web.
