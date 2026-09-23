# YOYI'R · Arquitectura de Fase 1

Esta fase se añade al proyecto previo. `generate_planner.py` y sus salidas originales no se modifican.

```text
src/
  config.py              dimensiones, tipografías e inventario editorial
  themes.py              seis paletas inmutables
  components.py          texto, botones, tablas, cajas y pestañas
  navigation.py          registro de destinos e intención de cada enlace
  templates.py           áreas de anotación y plantillas reutilizables
  planner/
    dates.py             calendarios, semanas y transiciones
    blueprint.py         arquitectura fechada completa como datos
    manifest.py          selección explícita de las 60 páginas de fase 1
  layouts/
    planner.py           composición de páginas
    covers.py            arte vectorial original y catálogo de portadas
  stickers.py            exportador PNG RGBA y catálogo de activos
  notebooks.py           seis tipos, diez secciones y plantillas
  validation.py          comprobaciones sobre los archivos serializados
  build.py               generación, informes y paquete descargable
assets/                  política de recursos; no fuentes ni arte de terceros
output/                  PDFs reales, PNG, previews, mapas y validaciones
docs/                    arquitectura, pruebas manuales e informe de construcción
tests/                   regresiones de fechas y arquitectura
```

## Regenerar

Desde la raíz, con Python 3.12 y las dependencias existentes:

```shell
python -m pip install -r requirements.txt
python -m src.build
python -m unittest discover -s tests -v
```

Las fuentes Calibri, Calibri Bold y Georgia se leen de `C:/Windows/Fonts`. Para un equipo con otro directorio, definir `YOYIR_FONT_DIR` con los archivos `calibri.ttf`, `calibrib.ttf` y `georgia.ttf` debidamente licenciados. No se redistribuyen esos archivos. Los subconjuntos usados se incrustan en el PDF; el dispositivo receptor no necesita instalarlos.

El mismo generador acepta `--theme lavender|blush|sage|sky|sand|neutral` y `--output carpeta`. El argumento cambia las páginas de trabajo; las seis demostraciones conservan intencionalmente sus seis paletas. El informe de construcción describe la última ejecución. Ejecutar sin argumentos para restaurar las salidas canónicas antes de publicar.

## Datos y navegación

- `calendar-2026-2028.json`: los 1096 días, columnas de calendario, lunes de cada semana y días anteriores/siguientes.
- `publishing-blueprint.json`: IDs de todas las páginas futuras anuales, mensuales, semanales y diarias. No genera cientos de páginas PDF. Cada año conserva sus pestañas, incluso en semanas que cruzan el límite anual.
- `master-manifest.json` y `notebook-manifest.json`: orden físico publicado de las páginas.
- `*-navigation.json`: cada enlace registra origen, destino, etiqueta y rectángulo. Los destinos se validan contra las anotaciones reales, no solo contra el catálogo.
- Los destinos globales usan `/Fit`. Los meses compactos usan `/FitR` para ampliar el rectángulo del mes correcto; enero 2026 tiene su dashboard completo. Ningún enlace abandona el PDF.
- La portada conduce a todas las páginas mediante un grafo comprobado. Las áreas de escritura no son controles. Las listas editoriales futuras son texto plano, sin botones falsos.

## Reutilización y límites

Las portadas son ilustraciones vectoriales generadas con geometría propia. Hay 12 composiciones iniciales y 150 registros de catálogo; los restantes están reservados, no dibujados. El catálogo de stickers reserva 1680 IDs. Ampliar la biblioteca requiere diseñar nuevos elementos, no contar recolores o reservas como activos terminados.

Los seis tipos de notebook se configuran desde `notebook_pages(style=...)`. Esta fase publica el tipo LINED con una página de notas de proyecto adicional en cada sección. Las secciones se personalizan escribiendo sus títulos; la pestaña numérica es estable.

No hay cambio dinámico de temas, cálculo financiero, almacenamiento de datos, integraciones ni lógica ejecutable en los PDFs. Insertar PNG, sustituir portadas o duplicar páginas depende de la app. Los enlaces de una copia de página podrían continuar apuntando al original.

La validación automática complementa la revisión visual; no sustituye las pruebas en teléfono y tablet. Fase 2 requiere aprobación y no se ejecuta por defecto.
