# Auditoría inicial del archivo fotográfico

## Alcance y base

Base inspeccionada: `4e6f256f4d8adc1b1af4bc9b02b72d627f2e6a97` del original. `index.html` no modificado.

Fuente autorizada: carpeta pública `1Fqf4PVjly0UXCLWEN4zByLekWpJAmOPk` y sus subcarpetas. Fecha exacta de la captura: `summary.json`. Los resultados describen la visibilidad pública, no prueban la inexistencia de archivos restringidos.

## Inventario verificado

212 archivos multimedia visibles con ID único: 149 HEIC, 32 JPG y 31 MOV. Además, cuatro subcarpetas visibles.

Por ubicación:

- Raíz `Fotitos importantes`: 149 archivos, sin clasificación por clase en el origen.
- `clase 31 agosto`: 26 archivos; la página utiliza los 26 (24 fotos y 2 videos).
- `taller sensorial`: 37 archivos; la página utiliza 24 (23 fotos y 1 video).
- `clase cangrejos`: sin archivos visibles públicamente.

La página referencia 50 archivos distintos: 47 fotos y 3 videos. Sus 50 IDs existen en el inventario y los nombres originales coinciden exactamente. 162 archivos visibles no están referenciados por la página; esto NO significa que sean 162 escenas nuevas, pues hay nombres repetidos con IDs diferentes.

## Clasificación trazable, no inventada

El CSV conserva ID y nombre original, carpeta de origen, propuesta de categoría y fundamento:

- 63 archivos tienen categoría respaldada por su subcarpeta de origen.
- 48 archivos de la raíz tienen el mismo nombre (sin distinguir mayúsculas) que archivos de la página. Se marca la categoría solo como **candidata por nombre**; no se asegura duplicidad de contenido.
- 101 archivos de la raíz quedan en `pending-review`. No hay evidencia de carpeta/nombre que permita ubicarlos automáticamente.

El campo `proposedName` añade la categoría al nombre original; NO intenta inventar el plato, ingrediente ni técnica que aparece. Nada ha sido renombrado en Drive.

## Fotos omitidas en Taller Sensorial

La subcarpeta contiene estas 13 fotos adicionales, no incluidas en los arrays de la página:

`IMG_1882.HEIC`, `IMG_1883.HEIC`, `IMG_1884.HEIC`, `IMG_1885.HEIC`, `IMG_1886.HEIC`, `IMG_1891.HEIC`, `IMG_1892.HEIC`, `IMG_1893.HEIC`, `IMG_1901.HEIC`, `IMG_1907.HEIC`, `IMG_1908.HEIC`, `IMG_1909.HEIC`, `IMG_1910.HEIC`.

No se insertaron automáticamente: puede tratarse de una selección editorial intencionada.

## Carga de las imágenes

Las 47 URLs de miniatura respondieron HTTP 200 con contenido de imagen. No se ha demostrado una rotura general de los enlaces ni una falta general de permisos.

Prueba adicional en Chrome headless, contexto nuevo, sobre la web publicada original:

- Portada cargada, ancho natural de 1600 píxeles.
- Primeras ocho imágenes de Taller Sensorial cargadas, ancho natural de 1200 píxeles.
- Galería generada con 47 tarjetas; 40 imágenes cargadas en la posición recorrida, ninguna imagen terminada con error. Las otras siete no se contabilizan como fallos: existe carga diferida.
- Sin excepciones JavaScript ni solicitudes fallidas durante este recorrido.
- Aviso de permisos de Drive oculto.

Evidencia estructurada: `browser-baseline.json`. Capturas locales excluidas del repositorio público para no volver a publicar imágenes de personas. Este recorrido no prueba todos los navegadores, móviles, videos ni todas las imágenes desplazándose hasta el final.

## Correspondencia editorial

La existencia de un ID/nombre correcto NO valida el pie de foto. La inspección visual de una captura encontró un ejemplo que requiere revisión: `IMG_1881.HEIC` dice «Transformación del grano y el plátano en masas suaves llenas de aroma», pero la imagen visible muestra una mano y materiales sobre una mesa, no documenta claramente ese proceso. La precisión de todos los pies continúa pendiente; no convertir textos existentes en evidencia de lo que ocurrió.

## Decisión pendiente

Confirmar si los archivos sueltos de la raíz pertenecen exclusivamente a las tres clases de la revista. Después, revisar miniaturas/contactos para nombrar descriptivamente y asignar solo lo que pueda verificarse. Los ambiguos necesitan confirmación de David.

Antes de modificar la carga, precisar el síntoma que experimenta David (imagen que no aparece, imagen incorrecta, pie incorrecto o material ausente). No sustituir enlaces que actualmente cargan por una solución especulativa.

No se ha desplegado, cambiado la revista, copiado originales a GitHub ni alterado Drive.
