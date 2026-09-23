# Digital Planner · Prueba técnica

Planner PDF sin fecha, con diseño pastel, pensado para probar navegación y anotación en teléfono y tablet.

## Archivos

- [Descargar el PDF](digital-planner-test.pdf): 8 páginas verticales, 450 × 720 puntos y 86 enlaces internos.
- [Vista previa](planner-preview.png).
- [Informe de validación](validation-report.json).
- `generate_planner.py`: genera el PDF, comprueba los enlaces y renderiza todas las páginas.

Incluye portada, índice, mes, semana, día, objetivos, finanzas y notas. La escritura y el dibujo se realizan con las herramientas de la aplicación de anotación. No contiene formularios, cálculos automáticos, JavaScript ni dependencias de navegador.

## Probar en teléfono y tablet

1. Descargar el PDF original e importarlo en una aplicación de anotación PDF.
2. Tocar OPEN PLANNER y recorrer las secciones, las pestañas superiores y los botones inferiores.
3. Usar el modo de navegación o lectura si la aplicación lo requiere para activar enlaces.
4. Escribir, dibujar y resaltar; comprobar legibilidad, tamaño táctil y comodidad al ampliar.
5. Guardar, cerrar y volver a abrir para comprobar que se conservan las anotaciones.
6. Si se exporta una copia, comprobar que conserva también la navegación.

Los destinos de los 86 enlaces y el renderizado de las 8 páginas se verificaron mediante PyMuPDF y pypdf. La compatibilidad con aplicaciones específicas queda pendiente de pruebas reales en dispositivos.

## Regenerar

Requiere Python y las fuentes Calibri, Calibri Bold y Georgia instaladas en `C:/Windows/Fonts`, tal como se utilizan en el script.

```shell
python -m pip install -r requirements.txt
python generate_planner.py
```

El script escribe el PDF, la vista previa y el informe en su misma carpeta. El PDF final no requiere Python ni esas fuentes instaladas en el dispositivo: las fuentes están incrustadas.
