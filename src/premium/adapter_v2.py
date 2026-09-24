"""
ADAPTADOR VISUAL PREMIUM V2

Versión corregida que usa SOLO la API de Drawing (src.components.Drawing)
Sin intentar mezclar con Art (premium/art.py).

Propósito: Aplicar estética premium a generadores existentes.
"""

from reportlab.lib.colors import HexColor

# Paleta premium
PREMIUM_COLORS = {
    'lavanda': '#CDBCE8',
    'lila': '#B9A4D8',
    'blush': '#E7B8C8',
    'rosa': '#F3D5DF',
    'coral': '#EFAFA2',
    'melocoton': '#F4C6A6',
    'amarillo': '#F3DFA5',
    'salvia': '#B9CBAE',
    'menta': '#BFE0D0',
    'azul': '#B8D7E8',
    'periwinkle': '#B9C5EA',
    'arena': '#DCCBB6',
    'crema': '#FAF7F2',
    'tinta': '#39353F'
}

class PremiumAdapterV2:
    """Adaptador premium usando API de Drawing."""

    def __init__(self, drawing):
        self.d = drawing
        self.c = drawing.c
        self.t = drawing.t
        self.nav = drawing.nav
        self.page = drawing.page

    def shell_background(self):
        """Dibujar fondo premium (capas de papel)."""
        # Fondo exterior
        self.d.box(0, 0, 540, 960, '#ECE8EF', stroke=False, radius=0)

        # Capas de papel (efecto suave)
        self.d.box(33, 79, 439, 864, '#DCD6DD', stroke=False, radius=17)
        self.d.box(29, 72, 437, 866, '#E9E3DE', stroke=False, radius=15)
        self.d.box(25, 65, 435, 867, '#FFFCF7', stroke=False, radius=13)
        self.d.box(25, 66, 22, 865, '#F0EBE6', stroke=False, radius=12)

    def shell_binding(self):
        """Dibujar línea de encuadernación y anillas."""
        # Línea de binding
        self.d.line(46, 82, 46, 914, '#DAD1C9')

        # Anillas
        for yy in range(117, 866, 94):
            self.c.setFillColor(HexColor('#D1C8C4'))
            self.c.circle(35, self.c._pagesize[1] - yy, 3)

    def page_number(self, current, total):
        """Número de página en esquina inferior."""
        self.d.text(f'{current:04d}/{total:04d}', 60, 945, 8, color='#78707A')

    def premium_title(self, title, subtitle='', color_key='lavanda'):
        """Título con línea decorativa."""
        color = PREMIUM_COLORS.get(color_key, '#CDBCE8')

        if subtitle:
            self.d.text(subtitle, 60, 125, 10, 'Bold', color='#6D6670')

        size = 27 if len(title) < 23 else 23
        self.d.text(title, 58, 163, size, 'Editorial')

        # Línea decorativa
        self.d.line(60, 180, 136, 180, color)

    def month_divider(self, title, year_text, color_key='blush'):
        """Divisor de mes premium."""
        color = PREMIUM_COLORS.get(color_key, '#CDBCE8')

        # Forma decorativa (usando box redondeado)
        self.d.box(85, 189, 330, 318, color, stroke=False, radius=160)

        # Títulos
        self.d.text(title, 250, 548, 52, 'Editorial', center=True)
        self.d.text(year_text, 250, 587, 24, center=True)

        # Línea con frase
        self.d.text('Este mes quiero...', 77, 657, 21, 'Editorial')
        self.d.line(78, 692, 344, 692)

    def section_entry(self, label, x, y, width, height, color_key='lavanda'):
        """Entrada de sección (tarjeta con color)."""
        color = PREMIUM_COLORS.get(color_key, '#CDBCE8')
        self.d.box(x, y, width, height, color, stroke=False, radius=10)
        self.d.text(label, x + width/2, y + height/2 + 5, 13, 'Bold', center=True)

    def checklist_item(self, x, y, width=150, label=None):
        """Item de lista con checkbox."""
        # Checkbox
        self.d.box(x, y, 11, 11, self.t.paper, stroke=True, radius=2)
        # Línea
        self.d.line(x+21, y+11, x+width, y+11)
        if label:
            self.d.text(label, x+12, y+7, 11, 'Bold')

def create_adapter(drawing):
    """Factory para crear adaptador."""
    return PremiumAdapterV2(drawing)
