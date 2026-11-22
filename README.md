# Marea & Azotea — fork de trabajo

Revista web de Cocinas del Pacífico. Fork de [aidaa8048-pixel/marea-y-azotea](https://github.com/aidaa8048-pixel/marea-y-azotea).

## Flujo

- `main`: copia inicial del original, sin cambios de la auditoría.
- `dev`: inventario, auditoría y futuros cambios verificables.
- No se configura despliegue ni se modifica el repositorio original.
- No se renombran, mueven ni alteran permisos de los archivos de Drive.

## Archivo fotográfico

- [Diagnóstico y límites](audit/REPORT.md).
- [Catálogo CSV](audit/media-catalog.csv): nombre original, ID, carpeta, categoría propuesta y evidencia; puede abrirse en Excel.
- [Inventario JSON](audit/inventory.json).
- [Archivos utilizados por la página](audit/page-references.json).
- [Pruebas HTTP de miniaturas](audit/thumbnail-checks.json).
- [Prueba en navegador](audit/browser-baseline.json).

Los nombres propuestos NO se han aplicado a los archivos originales. Coincidir por nombre no prueba que dos archivos tengan el mismo contenido. `pending-review` es deliberado: no asignar material a una clase sin evidencia.

## Reproducir la auditoría

Python 3, sin instalar dependencias:

```sh
python tools/audit_media.py
python -m unittest discover -s tests -v
```

El primer comando hace solicitudes de solo lectura a la carpeta pública autorizada y actualiza los JSON/CSV de `audit/`. No descarga originales. La prueba en navegador es evidencia separada y no se reproduce con ese comando.

Para ver la revista localmente, servir este directorio con un servidor estático, por ejemplo `python -m http.server 8080 --bind 127.0.0.1`. La página necesita Internet para Tailwind, fuentes y medios de Google Drive.
