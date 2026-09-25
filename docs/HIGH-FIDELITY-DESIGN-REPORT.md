# YOYI'R · Dirección de arte de alta fidelidad

**PÁGINAS:** 33: las 30 páginas solicitadas más 2027, 2028 y sin fecha para resolver los accesos del inicio.
**PDF:** `output/YOYIR-Premium-High-Fidelity-Prototype.pdf`. 540 × 960 pt, vertical. 551 enlaces internos reales.

**LAYOUT FAMILIES:** 24 familias diferenciadas.

| Página | Diseño | Familia |
| ---: | --- | --- |
| 01 | PORTADA | cover |
| 02 | INICIO | dashboard |
| 03 | MENÚ | directory |
| 04 | 2026 | annual |
| 05 | ENERO 2026 | calendar |
| 06 | FEBRERO 2028 | calendar |
| 07 | MARZO | divider |
| 08 | MARZO 2026 | calendar |
| 09 | PLAN DEL MES | roadmap |
| 10 | MI SEMANA | split-page |
| 11 | MIÉRCOLES | timeline |
| 12 | OBJETIVOS | editorial-divider |
| 13 | MI META SMART | goal-map |
| 14 | VIDA | editorial-divider |
| 15 | MI VIDA | collage |
| 16 | PRODUCTIVIDAD | editorial-divider |
| 17 | MENOS RUIDO, MÁS FOCO | matrix |
| 18 | BIENESTAR | editorial-divider |
| 19 | MI SEMANA DE BIENESTAR | tracker |
| 20 | VOLVER A MÍ | journal |
| 21 | FINANZAS | editorial-divider |
| 22 | PRESUPUESTO MENSUAL | table |
| 23 | ESTUDIO | editorial-divider |
| 24 | PLAN DE ESTUDIO | study-plan |
| 25 | UN LUGAR PARA CADA COSA | checklist |
| 26 | IDEAS QUE MERECEN QUEDARSE | dot-grid |
| 27 | PEQUEÑOS EXTRAS | resource-board |
| 28 | STICKERS FUNCIONALES | sticker-sheet |
| 29 | STICKERS DE VIDA | illustration-sheet |
| 30 | TU TIEMPO, TU RITMO | freeform |
| 31 | 2027 | annual |
| 32 | 2028 | annual |
| 33 | UN NUEVO COMIENZO | undated |

**COLORES:** LAVANDA `#CBB9E5`, BLUSH `#E9BBCB`, CORAL `#EFAFA3`, PEACH `#F4C8A7`, YELLOW `#F3DFA0`, SAGE `#B9CEAD`, MINT `#BDE0CF`, SKY `#B6D8EA`, PERIWINKLE `#BDC6EC`, SAND `#DCCBB7`.

**COMPONENTES:** DIGITAL_PLANNER_SHELL, papel interior, borde de hojas, sombra de papel, margen de encuadernación, cinco pestañas superiores, pestañas laterales mensuales/de sección, estado activo, menú, cinta washi, nota adhesiva, clip vectorial, renglones, checklist, mini calendarios, timeline, escala de ánimo, gotas, barra segmentada, matriz, collage y stickers troquelados.

**ICONOS:** agenda, auriculares, avion, botella, camara, cartera, casa, check, clip, comida, corazon, estrella, flecha, gota, hoja, lapiz, libro, luna, maleta, pastel, planta, regalo, reloj, sobre, sol, taza, zapatilla. Todos dibujados con vectores propios; sin emojis, imágenes descargadas ni clipart externo.

**STICKERS VISIBLES:** 58 instancias: 29 en la hoja funcional, 20 en la hoja de vida y el resto integrado en dashboards/páginas. Son arte vectorial real. Las hojas no simulan una función de inserción al tocarlas.

**TRACKERS:** agua con 8 gotas; ánimo/energía con escalas; hábitos con puntos; sueño con línea temporal por día; ahorro y progreso con barras segmentadas; movimiento con icono y registro. Los indicadores se marcan usando la aplicación de anotación, sin cálculos ni automatización.

**CALENDARIOS VALIDADOS:** 40: 36 mini calendarios anuales, enero 2026, febrero 2028, marzo 2026 y mini marzo de estudio. Fechas calculadas con calendar/datetime y verificadas sobre el texto realmente dibujado. Enero 2026 empieza en jueves; febrero 2028 incluye el martes 29. Sin números de día 32–35.

**NAVEGACIÓN:** destinos PDF /Fit y /FitR. El mes con página desarrollada abre esa página; el resto abre su mini calendario del mismo año. Los cinco accesos SMART apuntan a sus áreas reales. Los accesos semana/día muestran las páginas de ejemplo 16–22/03/2026 y 18/03/2026. No existen páginas fechadas completas fuera de este prototipo.

**PLACEHOLDERS:** 0 textos de relleno; no aparece “ESPACIO PARA ESCRIBIR”. Los renglones y campos en blanco son áreas de anotación intencionales, no contenido pendiente.

**ERRORES AUTOMÁTICOS:** 0. PDFs leídos por PyMuPDF y pypdf estricto; se renderizan todas las páginas; se comprueban límites de textos/trazos, enlaces no superpuestos, destinos, fechas dibujadas, alcance de todas las páginas desde portada y ausencia de JavaScript/enlaces externos.

**OBJETIVOS TÁCTILES:** mínimo 64 × 64 pt (42,7 × 42,7 píxeles al ajustar a 360 px de ancho). Revisar tamaño físico y comodidad en la app de teléfono/tablet elegida; no se declara compatibilidad probada con aplicaciones específicas. Los calendarios anuales requieren ampliar para leer/anotar.

**ARCHIVOS PNG GENERADOS:** 11 previews a 1620 × 2880 px, más 3 hojas de contacto de todas las páginas.

- `output/premium-preview-images/01-portada.png`
- `output/premium-preview-images/02-inicio.png`
- `output/premium-preview-images/05-enero.png`
- `output/premium-preview-images/10-semana.png`
- `output/premium-preview-images/11-dia.png`
- `output/premium-preview-images/15-mi-vida.png`
- `output/premium-preview-images/19-tracker.png`
- `output/premium-preview-images/22-presupuesto.png`
- `output/premium-preview-images/24-plan-estudio.png`
- `output/premium-preview-images/28-funcionales.png`
- `output/premium-preview-images/29-stickers-vida.png`

**PRESERVACIÓN:** se verificó SHA-256 de todos los PDFs preexistentes antes y después; no se modificó ni regeneró el master ni el preview V2.

**CÓDIGO:** `src/premium/` separa arte vectorial, shell, composiciones y build/validación. Generar únicamente este archivo con `python -m src.premium.build`.

**REVISIÓN MANUAL:** revisar previews y probar navegación, /FitR, tamaño de pestañas, escritura y guardado en teléfono/tablet. La aprobación estética corresponde a la usuaria; los checks automáticos no certifican una valoración visual.

**ESTADO:** se entrega solo este prototipo y sus previews. No se inicia otra fase ni se aplica el diseño al master.
