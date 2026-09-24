"""
ADAPTADOR VISUAL PREMIUM

Traduce componentes visuales premium (del prototipo V2)
al sistema Drawing existente del Master.

Permite generar todas las páginas con estética premium sin reconstruir
los generadores de fechas, navegación y contenido existentes.
"""

from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics

# Paleta premium multicolor coordinada
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

# Mapa de colores por categoría
CATEGORY_COLORS = {
    'objetivos': ['#CDBCE8', '#B9C5EA'],  # lavanda + periwinkle
    'vida': ['#E7B8C8', '#F4C6A6'],  # blush + melocotón
    'productividad': ['#B8D7E8', '#B9C5EA'],  # azul + periwinkle
    'bienestar': ['#B9CBAE', '#BFE0D0'],  # salvia + menta
    'autocuidado': ['#E7B8C8', '#DCCBB6', '#F4C6A6'],  # blush + arena + melocotón
    'finanzas': ['#B9CBAE', '#F3DFA5', '#BFE0D0'],  # salvia + amarillo + menta
    'estudio': ['#B9C5EA', '#B8D7E8', '#F3DFA5'],  # periwinkle + azul + amarillo
    'organizacion': ['#EFAFA2', '#DCCBB6'],  # coral + arena
    'notas': ['#DCCBB6', '#CDBCE8'],  # arena + lavanda
    'extras': ['#BFE0D0', '#CDBCE8', '#E7B8C8']  # menta + lavanda + blush
}

class PremiumAdapter:
    """
    Adaptador que permite usar componentes visuales premium con la clase Drawing existente.

    Internamente traduce llamadas de estilo premium a operaciones de Drawing.
    """

    def __init__(self, drawing):
        """
        Inicializar adaptador con una instancia de Drawing existente.

        Args:
            drawing: Instancia de src.components.Drawing
        """
        self.d = drawing
        self.c = drawing.c
        self.t = drawing.t
        self.nav = drawing.nav
        self.page = drawing.page
        self.HEIGHT = drawing.c._pagesize[1]
        self.WIDTH = drawing.c._pagesize[0]

    def shell(self, page_num, total_pages, year=None, month=None):
        """
        Dibujar el shell premium de planner/cuaderno.
        Incluye: fondo crema, anillas, margen de encuadernación, número de página.
        """
        # Fondo exterior crema
        self.d.box(0, 0, self.WIDTH, self.HEIGHT, '#ECE8EF', radius=0)

        # Capas de papel (efecto 3D suave de cuaderno)
        self.d.box(33, 79, 439, 864, '#DCD6DD', radius=17)
        self.d.box(29, 72, 437, 866, '#E9E3DE', radius=15)
        self.d.box(25, 65, 435, 867, '#FFFCF7', radius=13)
        self.d.box(25, 66, 22, 865, '#F0EBE6', radius=12)

        # Línea de encuadernación (borde izquierdo de anillas)
        self.d.line(46, 82, 46, 914, '#DAD1C9', .8)

        # Anillas (pequeños círculos en el margen)
        for yy in range(117, 866, 94):
            self.c.setFillColor(HexColor('#D1C8C4'))
            self.c.circle(35, self.HEIGHT - yy, 3)
            self.d.line(19, yy-2, 36, yy-2, '#BBB2B0', 2)
            self.d.line(19, yy, 36, yy, '#FFFFFF', 1)

        # Número de página en esquina inferior
        self.d.text(f"{page_num:04d} / {total_pages:04d}", 60, 945, 8, color='#78707A')

    def premium_title(self, title, subtitle='', color_key='lavanda', size=28):
        """
        Título premium con línea de acento.

        Args:
            title: Título principal
            subtitle: Subtítulo (kicker)
            color_key: Clave en PREMIUM_COLORS
            size: Tamaño de fuente
        """
        color = PREMIUM_COLORS.get(color_key, '#CDBCE8')

        if subtitle:
            self.d.text(subtitle, 60, 125, 10, 'Bold', color='#6D6670')

        actual_size = size if len(title) < 23 else size - 4
        self.d.text(title, 58, 163, actual_size, 'Editorial')

        # Línea de acento
        self.d.line(60, 180, 136, 180, color)

    def premium_tabs_top(self, page_id, year=None, month=None):
        """
        Pestañas superiores: INICIO, AÑO, MES, SEM, DÍA
        Mostrar solo las relevantes según el tipo de página.
        """
        if year is None:
            year = 2026

        tabs = [
            ('INICIO', 'home', 0),
            ('AÑO', f'year-{year}', 7),
            ('MES', f'month-{year}-{month:02d}' if month else f'month-{year}-01', 3),
            ('SEM', 'week', 5),
            ('DÍA', 'day', 1)
        ]

        colors = ['#CBB9E5', '#DCCBB6', '#B8D7E8', '#BFE0D0', '#F4C6A6']

        for i, (label, target, color_idx) in enumerate(tabs):
            x = 48 + i * 86
            is_active = page_id == target

            # Box con borde redondeado
            color = [PREMIUM_COLORS['lavanda'], PREMIUM_COLORS['arena'],
                    PREMIUM_COLORS['azul'], PREMIUM_COLORS['menta'], PREMIUM_COLORS['melocoton']][color_idx]

            y = 19 if is_active else 25
            self.d.button(label, target, x, y, 80, 64 if is_active else 59)

            if is_active:
                # Línea indicadora de estado activo
                self.d.line(x+12, y+8, x+68, y+8, '#39353F')

    def premium_tabs_lateral(self, page_id, tab_type='month', year=None):
        """
        Pestañas laterales: meses (ENE-DIC) o colecciones (METAS, VIDA, etc.)
        """
        if tab_type == 'month':
            months = ['ENE', 'FEB', 'MAR', 'ABR', 'MAY', 'JUN',
                     'JUL', 'AGO', 'SEP', 'OCT', 'NOV', 'DIC']
            colors = ['#CDBCE8', '#E9BBCB', '#EFAFA2', '#F4C6A6', '#F3DFA0', '#B9CEAD',
                     '#BFE0D0', '#B6D8EA', '#BDC6EC', '#DCCBB7', '#CBB9E5', '#E7B8C8']

            for i, (label, color) in enumerate(zip(months, colors)):
                month_num = i + 1
                is_active = False  # Detectar desde page_id si corresponde
                target = f'month-{year}-{month_num:02d}' if year else 'month'

                x = 460 if is_active else 464
                y = 96 + i * 68
                width = 72 if is_active else 68
                height = 64

                self.d.button(label, target, x, y, width, height)

        elif tab_type == 'collection':
            collections = [
                ('METAS', 'objetivos', 0),
                ('VIDA', 'vida', 3),
                ('BIENESTAR', 'bienestar', 5),
                ('FINANZAS', 'finanzas', 4),
                ('NOTAS', 'notas', 7),
                ('EXTRAS', 'extras', 1)
            ]

            for i, (label, key, color_idx) in enumerate(collections):
                is_active = page_id == key
                color = list(PREMIUM_COLORS.values())[color_idx]

                x = 460 if is_active else 464
                y = 160 + i * 112

                self.d.button(label, key, x, y, 68 if is_active else 64, 92)

    def premium_buttons_bottom(self, prev_id, next_id, menu_id='menu'):
        """
        Botones inferiores: MENÚ, ANTERIOR, SIGUIENTE
        Táctil-friendly para tablet y teléfono.
        """
        self.d.button('MENÚ', menu_id, 58, 862, 112, 70)
        self.d.button('ANTERIOR', prev_id, 184, 862, 122, 70)
        self.d.button('SIGUIENTE', next_id, 320, 862, 122, 70)

    def premium_section_divider(self, title, subtitle, color_key='lavanda', icon_name=None):
        """
        Divisor de sección editorial (ej: MARZO, OBJETIVOS, VIDA)
        """
        color = PREMIUM_COLORS.get(color_key, '#CDBCE8')

        # Fondo decorativo con forma orgánica
        self.d.box(85, 189, 330, 318, color, radius=160)

        # Círculo decorativo adicional
        self.c.setFillColor(HexColor(['#EFAFA2', '#F4C6A6', '#B9CEAD'][
            hash(color_key) % 3]))
        self.c.circle(330, self.HEIGHT - 288, 64)

        # Título principal
        self.d.text(title, 250, 548, 52, 'Editorial', center=True)
        self.d.text(subtitle, 250, 587, 24, color=color)

        # Subtítulo/frase
        self.d.text('Este mes quiero…', 77, 657, 21, 'Editorial')
        self.d.line(78, 692, 344, 692)

    def premium_checkbox_list(self, x, y, items, color_key='lavanda', num_items=3):
        """
        Lista de checkboxes con estilo premium.
        """
        color = PREMIUM_COLORS.get(color_key, '#CDBCE8')
        gap = 30

        for i in range(num_items):
            # Checkbox pequeño
            self.d.box(x, y + i*gap, 11, 11, '#FFFCF7', stroke=True, radius=2)
            # Línea para escribir
            self.d.line(x+21, y+11+i*gap, x+200, y+11+i*gap)

    def premium_progress_bar(self, x, y, width=160, segments=8, color_key='salvia'):
        """
        Barra de progreso segmentada.
        """
        color = PREMIUM_COLORS.get(color_key, '#B9CBAE')

        self.d.box(x, y, width, 17, '#FFFCF7', stroke=True, radius=8)

        for i in range(1, segments):
            self.d.line(x + i*width/segments, y+2, x + i*width/segments, y+15, color)

        self.d.text('0', x, y+34, 10)
        self.d.text('100%', x+width, y+34, 10, center=True)

    def premium_tracker_dots(self, x, y, cols=7, rows=4, gap=20, color_key='lavanda'):
        """
        Grid de puntos para trackers (hábitos, ánimo, etc.)
        """
        for row in range(rows):
            for col in range(cols):
                xx = x + col * gap
                yy = y + row * gap
                self.c.setStrokeColor(HexColor('#A49C9C'))
                self.c.setLineWidth(.65)
                self.c.circle(xx, self.HEIGHT - yy, 3.2)

    def premium_sticky_note(self, x, y, width, height, color_key='blush'):
        """
        Nota adhesiva (sticky note) con washi tape.
        """
        color = PREMIUM_COLORS.get(color_key, '#E7B8C8')

        # Sombra
        self.d.box(x+3, y+4, width, height, '#E7E0D6', radius=2)
        # Nota principal
        self.d.box(x, y, width, height, color, radius=2)

        # Washi tape (decorativo)
        tape_color = PREMIUM_COLORS.get('melocoton', '#F4C6A6')
        self._draw_washi_tape(x + width/2 - 28, y - 8, 56, tape_color)

    def _draw_washi_tape(self, x, y, w, color):
        """Dibujar washi tape decorativo (línea punteada)."""
        self.c.setStrokeColor(HexColor(color))
        self.c.setLineWidth(3)
        for i in range(8, int(w)-4, 12):
            self.d.line(x+i, y+3, x+i-3, y+14, color, .6)

    def premium_icon(self, name, x, y, size=44, color_key='tinta'):
        """
        Dibujar icono lineal vectorial (premium).
        """
        color = PREMIUM_COLORS.get(color_key, '#39353F')

        self.c.saveState()
        self.c.translate(x, self.HEIGHT - y - size)
        self.c.scale(size/48, size/48)
        self.c.setStrokeColor(HexColor(color))
        self.c.setFillColor(HexColor('#FFFCF7'))
        self.c.setLineWidth(1.65)
        self.c.setLineCap(1)
        self.c.setLineJoin(1)

        # Invocar dibujante de iconos (simplificado)
        self._draw_icon_shape(name, self.c)

        self.c.restoreState()

    def _draw_icon_shape(self, name, canvas):
        """Formas básicas de iconos (subset del prototipo)."""
        def line(x1, y1, x2, y2):
            canvas.line(x1, y1, x2, y2)
        def rect(x, y, w, h, r=3):
            canvas.roundRect(x, y, w, h, r, stroke=1, fill=0)
        def circ(x, y, r):
            canvas.circle(x, y, r, stroke=1, fill=0)

        if name == 'checkmark':
            canvas.polyline([8, 23, 19, 12, 40, 37])
        elif name == 'clock':
            circ(24, 24, 18)
            line(24, 24, 24, 37)
            line(24, 24, 34, 20)
        elif name == 'star':
            import math
            points = [(24+(18 if i%2==0 else 8)*math.sin(i*math.pi/5),
                      24+(18 if i%2==0 else 8)*math.cos(i*math.pi/5)) for i in range(10)]
            path = canvas.beginPath()
            path.moveTo(*points[0])
            for p in points[1:]:
                path.lineTo(*p)
            path.close()
            canvas.drawPath(path, stroke=1)
        elif name == 'heart':
            path = canvas.beginPath()
            path.moveTo(24, 8)
            path.curveTo(-8, 29, 13, 51, 24, 34)
            path.curveTo(35, 51, 56, 29, 24, 8)
            canvas.drawPath(path, stroke=1)
        # Agregar más iconos según sea necesario

    def premium_collection_entry(self, label, target, index, total_in_row=2):
        """
        Entrada de colección en grid editorial (tarjeta con color).
        """
        pass  # Simplificado para esta fase

# Funciones de conveniencia para uso directo

def create_adapter(drawing):
    """Crear instancia de adaptador premium."""
    return PremiumAdapter(drawing)

def apply_premium_shell(drawing, page_num, total_pages, year=None, month=None):
    """Aplicar shell premium a una página."""
    adapter = create_adapter(drawing)
    adapter.shell(page_num, total_pages, year, month)

def apply_premium_title(drawing, title, subtitle='', color='lavanda'):
    """Aplicar título premium."""
    adapter = create_adapter(drawing)
    adapter.premium_title(title, subtitle, color)
