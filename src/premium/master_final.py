"""MASTER FINAL: PORTADA + DASHBOARD + MENÚ + AÑOS + RECURSOS MEJORADOS + OBJETIVOS + DATED CORE = 1424 páginas"""
import calendar
from datetime import date
import fitz
from reportlab.pdfgen import canvas
from ..config import OUTPUT
from ..components import register_fonts
from .art import W, H, COLORS
from .shell import digital_planner_shell
from .master_builder import dated_core_block, draw_block_page
from .dated import BlockArt
from .pages import cover, dashboard, menu, annual

def annual_core_block():
    """Generate PORTADA, DASHBOARD, MENÚ, YEAR OVERVIEWS, RECURSOS MEJORADOS, QUARTERS."""
    pages = []

    pages.append({'id': 'portada', 'kind': 'portada', 'year': 2026, 'month': 1, 'months': False})
    pages.append({'id': 'dashboard', 'kind': 'dashboard', 'year': 2026, 'month': 1, 'months': False})
    pages.append({'id': 'menu', 'kind': 'menu', 'year': 2026, 'month': 1, 'months': False})
    pages.append({'id': 'year-selector', 'kind': 'year-selector', 'year': 2026, 'month': 1, 'months': False})

    for year in (2026, 2027, 2028):
        pages.append({'id': f'year-{year}', 'kind': 'annual', 'year': year, 'month': 1, 'months': False, 'plan_anual': f'res-{year}-goals'})

        for resource in ['goals', 'dates', 'birthdays', 'projects', 'finance', 'personal', 'wellness', 'professional', 'vision', 'review']:
            pages.append({
                'id': f'res-{year}-{resource}',
                'kind': 'resource',
                'year': year,
                'resource': resource,
                'title': {
                    'goals': 'MIS OBJETIVOS DEL AÑO',
                    'dates': 'FECHAS IMPORTANTES',
                    'birthdays': 'CUMPLEAÑOS',
                    'projects': 'MIS PROYECTOS',
                    'finance': 'OBJETIVOS FINANCIEROS',
                    'personal': 'OBJETIVOS PERSONALES',
                    'wellness': 'OBJETIVOS DE BIENESTAR',
                    'professional': 'OBJETIVOS PROFESIONALES',
                    'vision': 'MI TABLERO DE VISIÓN',
                    'review': 'REVISIÓN ANUAL'
                }[resource],
                'year_return': f'year-{year}'
            })

        for quarter in (1, 2, 3, 4):
            months = ['ENERO·FEBRERO·MARZO', 'ABRIL·MAYO·JUNIO', 'JULIO·AGOSTO·SEPTIEMBRE', 'OCTUBRE·NOVIEMBRE·DICIEMBRE'][quarter - 1]
            pages.append({
                'id': f'q-{year}-{quarter}',
                'kind': 'quarter',
                'year': year,
                'quarter': quarter,
                'months': months,
                'year_return': f'year-{year}'
            })

    return pages

def objectives_collection():
    """Generate 12-page Objectives collection."""
    return [
        {'id': 'obj-div', 'kind': 'obj-divisor'},
        {'id': 'obj-vision', 'kind': 'obj-page', 'template': 'vision'},
        {'id': 'obj-overview', 'kind': 'obj-page', 'template': 'overview'},
        {'id': 'obj-smart', 'kind': 'obj-page', 'template': 'smart'},
        {'id': 'obj-plan', 'kind': 'obj-page', 'template': 'plan'},
        {'id': 'obj-action', 'kind': 'obj-page', 'template': 'action'},
        {'id': 'obj-milestones', 'kind': 'obj-page', 'template': 'milestones'},
        {'id': 'obj-progress', 'kind': 'obj-page', 'template': 'progress'},
        {'id': 'obj-obstacles', 'kind': 'obj-page', 'template': 'obstacles'},
        {'id': 'obj-checkin', 'kind': 'obj-page', 'template': 'checkin'},
        {'id': 'obj-victories', 'kind': 'obj-page', 'template': 'victories'},
        {'id': 'obj-review', 'kind': 'obj-page', 'template': 'review'},
    ]

def life_collection():
    """Generate 12-page VIDA collection."""
    return [
        {'id': 'life-div', 'kind': 'life-divisor'},
        {'id': 'life-overview', 'kind': 'life-page', 'template': 'overview'},
        {'id': 'life-board', 'kind': 'life-page', 'template': 'board'},
        {'id': 'life-dreams', 'kind': 'life-page', 'template': 'dreams'},
        {'id': 'life-adventures', 'kind': 'life-page', 'template': 'adventures'},
        {'id': 'life-places', 'kind': 'life-page', 'template': 'places'},
        {'id': 'life-learn', 'kind': 'life-page', 'template': 'learn'},
        {'id': 'life-favorites', 'kind': 'life-page', 'template': 'favorites'},
        {'id': 'life-happy', 'kind': 'life-page', 'template': 'happy'},
        {'id': 'life-memories', 'kind': 'life-page', 'template': 'memories'},
        {'id': 'life-year', 'kind': 'life-page', 'template': 'year'},
        {'id': 'life-capsule', 'kind': 'life-page', 'template': 'capsule'},
    ]

def productivity_collection():
    """Generate 12-page PRODUCTIVIDAD collection."""
    return [
        {'id': 'prod-div', 'kind': 'prod-divisor'},
        {'id': 'prod-focus', 'kind': 'prod-page', 'template': 'focus'},
        {'id': 'prod-matrix', 'kind': 'prod-page', 'template': 'matrix'},
        {'id': 'prod-braindump', 'kind': 'prod-page', 'template': 'braindump'},
        {'id': 'prod-task-plan', 'kind': 'prod-page', 'template': 'task_plan'},
        {'id': 'prod-project', 'kind': 'prod-page', 'template': 'project'},
        {'id': 'prod-board', 'kind': 'prod-page', 'template': 'board'},
        {'id': 'prod-focus-session', 'kind': 'prod-page', 'template': 'focus_session'},
        {'id': 'prod-time-block', 'kind': 'prod-page', 'template': 'time_block'},
        {'id': 'prod-recurring', 'kind': 'prod-page', 'template': 'recurring'},
        {'id': 'prod-waiting', 'kind': 'prod-page', 'template': 'waiting'},
        {'id': 'prod-review', 'kind': 'prod-page', 'template': 'review'},
    ]

def wellness_collection():
    """Generate 12-page BIENESTAR collection."""
    return [
        {'id': 'well-div', 'kind': 'well-divisor'},
        {'id': 'well-overview', 'kind': 'well-page', 'template': 'overview'},
        {'id': 'well-week', 'kind': 'well-page', 'template': 'week'},
        {'id': 'well-energy', 'kind': 'well-page', 'template': 'energy'},
        {'id': 'well-sleep', 'kind': 'well-page', 'template': 'sleep'},
        {'id': 'well-movement', 'kind': 'well-page', 'template': 'movement'},
        {'id': 'well-water', 'kind': 'well-page', 'template': 'water'},
        {'id': 'well-meals', 'kind': 'well-page', 'template': 'meals'},
        {'id': 'well-body-checkin', 'kind': 'well-page', 'template': 'body_checkin'},
        {'id': 'well-balance', 'kind': 'well-page', 'template': 'balance'},
        {'id': 'well-routines', 'kind': 'well-page', 'template': 'routines'},
        {'id': 'well-review', 'kind': 'well-page', 'template': 'review'},
    ]

def selfcare_collection():
    """Generate 12-page AUTOCUIDADO collection."""
    return [
        {'id': 'self-div', 'kind': 'self-divisor'},
        {'id': 'self-needs', 'kind': 'self-page', 'template': 'needs'},
        {'id': 'self-menu', 'kind': 'self-page', 'template': 'menu'},
        {'id': 'self-boundaries', 'kind': 'self-page', 'template': 'boundaries'},
        {'id': 'self-release', 'kind': 'self-page', 'template': 'release'},
        {'id': 'self-pause', 'kind': 'self-page', 'template': 'pause'},
        {'id': 'self-disconnect', 'kind': 'self-page', 'template': 'disconnect'},
        {'id': 'self-me-time', 'kind': 'self-page', 'template': 'me_time'},
        {'id': 'self-support', 'kind': 'self-page', 'template': 'support'},
        {'id': 'self-gestures', 'kind': 'self-page', 'template': 'gestures'},
        {'id': 'self-recharge', 'kind': 'self-page', 'template': 'recharge'},
        {'id': 'self-review', 'kind': 'self-page', 'template': 'review'},
    ]

def finance_collection():
    """Generate 12-page FINANZAS collection."""
    return [
        {'id': 'fin-div', 'kind': 'fin-divisor'},
        {'id': 'fin-overview', 'kind': 'fin-page', 'template': 'overview'},
        {'id': 'fin-budget', 'kind': 'fin-page', 'template': 'budget'},
        {'id': 'fin-expenses', 'kind': 'fin-page', 'template': 'expenses'},
        {'id': 'fin-bills', 'kind': 'fin-page', 'template': 'bills'},
        {'id': 'fin-subscriptions', 'kind': 'fin-page', 'template': 'subscriptions'},
        {'id': 'fin-savings', 'kind': 'fin-page', 'template': 'savings'},
        {'id': 'fin-funds', 'kind': 'fin-page', 'template': 'funds'},
        {'id': 'fin-debts', 'kind': 'fin-page', 'template': 'debts'},
        {'id': 'fin-purchases', 'kind': 'fin-page', 'template': 'purchases'},
        {'id': 'fin-calendar', 'kind': 'fin-page', 'template': 'calendar'},
        {'id': 'fin-review', 'kind': 'fin-page', 'template': 'review'},
    ]

def study_collection():
    """Generate 12-page ESTUDIO collection."""
    return [
        {'id': 'study-div', 'kind': 'study-divisor'},
        {'id': 'study-plan', 'kind': 'study-page', 'template': 'plan'},
        {'id': 'study-map', 'kind': 'study-page', 'template': 'map'},
        {'id': 'study-week', 'kind': 'study-page', 'template': 'week'},
        {'id': 'study-session', 'kind': 'study-page', 'template': 'session'},
        {'id': 'study-notes', 'kind': 'study-page', 'template': 'notes'},
        {'id': 'study-summary', 'kind': 'study-page', 'template': 'summary'},
        {'id': 'study-questions', 'kind': 'study-page', 'template': 'questions'},
        {'id': 'study-review', 'kind': 'study-page', 'template': 'review'},
        {'id': 'study-assessments', 'kind': 'study-page', 'template': 'assessments'},
        {'id': 'study-resources', 'kind': 'study-page', 'template': 'resources'},
        {'id': 'study-reflection', 'kind': 'study-page', 'template': 'reflection'},
    ]

def organization_collection():
    """Generate 12-page ORGANIZACIÓN collection."""
    return [
        {'id': 'org-div', 'kind': 'org-divisor'},
        {'id': 'org-pending', 'kind': 'org-page', 'template': 'pending'},
        {'id': 'org-home', 'kind': 'org-page', 'template': 'home'},
        {'id': 'org-maintenance', 'kind': 'org-page', 'template': 'maintenance'},
        {'id': 'org-shopping', 'kind': 'org-page', 'template': 'shopping'},
        {'id': 'org-inventory', 'kind': 'org-page', 'template': 'inventory'},
        {'id': 'org-errands', 'kind': 'org-page', 'template': 'errands'},
        {'id': 'org-documents', 'kind': 'org-page', 'template': 'documents'},
        {'id': 'org-repairs', 'kind': 'org-page', 'template': 'repairs'},
        {'id': 'org-declutter', 'kind': 'org-page', 'template': 'declutter'},
        {'id': 'org-packing', 'kind': 'org-page', 'template': 'packing'},
        {'id': 'org-reset', 'kind': 'org-page', 'template': 'reset'},
    ]

def notes_collection():
    """Generate 12-page NOTAS collection."""
    return [
        {'id': 'notes-div', 'kind': 'notes-divisor'},
        {'id': 'notes-lined', 'kind': 'notes-page', 'template': 'lined'},
        {'id': 'notes-dotted', 'kind': 'notes-page', 'template': 'dotted'},
        {'id': 'notes-grid', 'kind': 'notes-page', 'template': 'grid'},
        {'id': 'notes-blank', 'kind': 'notes-page', 'template': 'blank'},
        {'id': 'notes-idea', 'kind': 'notes-page', 'template': 'idea'},
        {'id': 'notes-quick', 'kind': 'notes-page', 'template': 'quick'},
        {'id': 'notes-mindmap', 'kind': 'notes-page', 'template': 'mindmap'},
        {'id': 'notes-compare', 'kind': 'notes-page', 'template': 'compare'},
        {'id': 'notes-meeting', 'kind': 'notes-page', 'template': 'meeting'},
        {'id': 'notes-capture', 'kind': 'notes-page', 'template': 'capture'},
        {'id': 'notes-mixed', 'kind': 'notes-page', 'template': 'mixed'},
    ]

def extras_collection():
    """Generate 12-page EXTRAS collection."""
    return [
        {'id': 'extras-div', 'kind': 'extras-divisor'},
        {'id': 'extras-functional', 'kind': 'extras-page', 'template': 'functional'},
        {'id': 'extras-life', 'kind': 'extras-page', 'template': 'life'},
        {'id': 'extras-labels', 'kind': 'extras-page', 'template': 'labels'},
        {'id': 'extras-checks', 'kind': 'extras-page', 'template': 'checks'},
        {'id': 'extras-numbers', 'kind': 'extras-page', 'template': 'numbers'},
        {'id': 'extras-months', 'kind': 'extras-page', 'template': 'months'},
        {'id': 'extras-weekdays', 'kind': 'extras-page', 'template': 'weekdays'},
        {'id': 'extras-mood', 'kind': 'extras-page', 'template': 'mood'},
        {'id': 'extras-decorative', 'kind': 'extras-page', 'template': 'decorative'},
        {'id': 'extras-paper', 'kind': 'extras-page', 'template': 'paper'},
        {'id': 'extras-free', 'kind': 'extras-page', 'template': 'free'},
    ]

def draw_resource_page(a, p):
    """Draw improved resource pages."""
    title = p['title']
    year = p['year']
    resource = p['resource']

    a.box(0, 0, W, H, '#ECE8EF', r=0)
    a.box(25, 65, 435, 867, '#F8F5F0', r=13)
    a.text(title, 60, 130, 18, 'Bold')
    a.text(f'{year}', 60, 155, 12)

    if resource == 'goals':
        a.text('OBJETIVO', 60, 280, 9, 'Bold')
        a.lines(60, 270, 380, 3, 45)
    elif resource == 'dates':
        a.text('FECHA', 60, 295, 9, 'Bold')
        a.text('EVENTO', 150, 295, 9, 'Bold')
        a.text('CATEGORÍA', 280, 295, 9, 'Bold')
        a.lines(60, 265, 380, 6, 35)
    elif resource == 'birthdays':
        a.text('NOMBRE', 60, 295, 9, 'Bold')
        a.text('FECHA', 200, 295, 9, 'Bold')
        a.text('REGALO', 300, 295, 9, 'Bold')
        a.lines(60, 265, 380, 6, 35)
    elif resource == 'projects':
        a.text('PROYECTO', 60, 295, 9, 'Bold')
        a.text('PRÓXIMO PASO', 240, 295, 9, 'Bold')
        a.text('FECHA', 380, 295, 9, 'Bold')
        a.lines(60, 265, 380, 5, 40)
    elif resource == 'finance':
        a.text('META', 60, 295, 9, 'Bold')
        a.text('OBJETIVO', 160, 295, 9, 'Bold')
        a.text('ACTUAL', 280, 295, 9, 'Bold')
        a.text('%', 360, 295, 9, 'Bold')
        a.lines(60, 265, 380, 5, 40)
    elif resource == 'personal':
        a.text('QUIERO', 60, 295, 9, 'Bold')
        a.text('POR QUÉ', 220, 295, 9, 'Bold')
        a.text('PRIMER PASO', 340, 295, 9, 'Bold')
        a.lines(60, 265, 380, 5, 40)
    elif resource == 'wellness':
        a.text('ÁREA', 60, 295, 9, 'Bold')
        a.text('MEJORAR', 160, 295, 9, 'Bold')
        a.text('ACCIÓN', 280, 295, 9, 'Bold')
        a.text('FRECUENCIA', 370, 295, 9, 'Bold')
        a.lines(60, 265, 380, 4, 45)
    elif resource == 'professional':
        a.text('OBJETIVO', 60, 295, 9, 'Bold')
        a.text('HABILIDAD', 200, 295, 9, 'Bold')
        a.text('FECHA', 330, 295, 9, 'Bold')
        a.lines(60, 265, 380, 5, 40)
    elif resource == 'vision':
        for i, label in enumerate(['VIVIR', 'CREAR', 'APRENDER', 'SENTIR', 'CONSEGUIR']):
            a.text(label, 60, 260 - i * 50, 10, 'Bold')
            a.lines(60, 240 - i * 50, 380, 1, 40)
    elif resource == 'review':
        for i, label in enumerate(['LOGRÉ', 'APRENDÍ', 'CAMBIÓ', 'MOMENTOS', 'ORGULLOSA', 'SUELTO', 'LLEVO', 'PALABRA']):
            a.text(label, 60, 320 - i * 40, 10, 'Bold')
            a.lines(60, 290 - i * 40, 380, 1, 35)

def draw_objectives_page(a, p):
    """Draw objectives collection pages."""
    a.box(0, 0, W, H, '#ECE8EF', r=0)
    a.box(25, 65, 435, 867, '#F8F5F0', r=13)

    if p['kind'] == 'obj-divisor':
        a.text('OBJETIVOS', 250, 400, 38, 'Editorial', center=True)
        a.text('Lo que quiero construir', 250, 450, 16, 'Editorial', center=True)
    else:
        template = p.get('template')
        titles = {
            'vision': ('Mi visión', 'UNA IDEA CON DIRECCIÓN'),
            'overview': ('Mis objetivos', 'RESUMEN POR ÁREA'),
            'smart': ('Objetivo SMART', 'ESPECÍFICA, MEDIBLE, ALCANZABLE'),
            'plan': ('De meta a plan', 'ESTRUCTURA CLARA'),
            'action': ('Plan de acción', 'PASOS CONCRETOS'),
            'milestones': ('Hitos', 'PUNTOS DE REFERENCIA'),
            'progress': ('Seguimiento', 'MONITOREO CONTINUO'),
            'obstacles': ('Obstáculos', 'ANTICIPAR Y RESOLVER'),
            'checkin': ('Check-in', 'REVISIÓN PERIÓDICA'),
            'victories': ('Pequeñas victorias', 'CELEBRAR AVANCES'),
            'review': ('Revisión', 'REFLEXIÓN FINAL'),
        }
        if template in titles:
            title, subtitle = titles[template]
            a.text(title, 60, 130, 18, 'Bold')
            a.text(subtitle, 60, 155, 12)
            a.lines(60, 280, 380, 6, 40)

def draw_life_page(a, p):
    """Draw VIDA collection pages."""
    a.box(0, 0, W, H, '#ECE8EF', r=0)
    a.box(25, 65, 435, 867, '#F8F5F0', r=13)

    if p['kind'] == 'life-divisor':
        a.text('VIDA', 250, 400, 38, 'Editorial', center=True)
        a.text('Lo que hace mi vida mía', 250, 450, 16, 'Editorial', center=True)
    else:
        template = p.get('template')
        titles = {
            'overview': ('Mi vida', 'VISIÓN PERSONAL'),
            'board': ('Mi tablero de vida', 'ÁREAS IMPORTANTES'),
            'dreams': ('Lista de sueños', 'COSAS QUE QUIERO VIVIR'),
            'adventures': ('Mis aventuras', 'EXPERIENCIAS Y VIAJES'),
            'places': ('Lugares que quiero conocer', 'DESTINOS'),
            'learn': ('Cosas que quiero aprender', 'INTERESES PERSONALES'),
            'favorites': ('Mis favoritos', 'LO QUE AMO'),
            'happy': ('Cosas que me hacen feliz', 'PEQUEÑOS PLACERES'),
            'memories': ('Recuerdos', 'MOMENTOS QUE GUARDAR'),
            'year': ('Mi año en momentos', 'MEMORIA PERSONAL'),
            'capsule': ('Cápsula del tiempo', 'PARA MI YO DEL FUTURO'),
        }
        if template in titles:
            title, subtitle = titles[template]
            a.text(title, 60, 130, 18, 'Bold')
            a.text(subtitle, 60, 155, 12)
            a.lines(60, 280, 380, 6, 40)

def draw_productivity_page(a, p):
    """Draw PRODUCTIVIDAD collection pages."""
    a.box(0, 0, W, H, '#ECE8EF', r=0)
    a.box(25, 65, 435, 867, '#F8F5F0', r=13)

    if p['kind'] == 'prod-divisor':
        a.text('PRODUCTIVIDAD', 250, 380, 34, 'Editorial', center=True)
        a.text('Hacer espacio para lo importante', 250, 450, 14, 'Editorial', center=True)
    else:
        template = p.get('template')
        titles = {
            'focus': ('Mi plan de foco', 'MENOS RUIDO, MÁS FOCO'),
            'matrix': ('Matriz de prioridades', 'QUÉ HACER'),
            'braindump': ('Sacar todo de mi cabeza', 'DESCARGAR PENDIENTES'),
            'task_plan': ('De pendiente a plan', 'HACERLO MANEJABLE'),
            'project': ('Plan de proyecto', 'DESGLOSADO Y DIRIGIDO'),
            'board': ('Tablero de tareas', 'POR HACER → HECHO'),
            'focus_session': ('Sesión de foco', 'UNA SESIÓN PRODUCTIVA'),
            'time_block': ('Bloques de tiempo', 'ORGANIZAR MI DÍA'),
            'recurring': ('Tareas repetitivas', 'LO QUE VUELVE UNA Y OTRA VEZ'),
            'waiting': ('En espera / Delegado', 'NO TODO DEPENDE DE MÍ'),
            'review': ('Revisión de productividad', 'LO QUE FUNCIONÓ'),
        }
        if template in titles:
            title, subtitle = titles[template]
            a.text(title, 60, 130, 18, 'Bold')
            a.text(subtitle, 60, 155, 12)
            a.lines(60, 280, 380, 6, 40)

def draw_wellness_page(a, p):
    """Draw BIENESTAR collection pages."""
    a.box(0, 0, W, H, '#ECE8EF', r=0)
    a.box(25, 65, 435, 867, '#F8F5F0', r=13)

    if p['kind'] == 'well-divisor':
        a.text('BIENESTAR', 250, 380, 34, 'Editorial', center=True)
        a.text('Escuchar mi propio ritmo', 250, 450, 14, 'Editorial', center=True)
    else:
        template = p.get('template')
        titles = {
            'overview': ('Mi bienestar', 'CÓMO ESTOY'),
            'week': ('Mi semana de bienestar', 'SEGUIMIENTO DIARIO'),
            'energy': ('Conocer mi energía', 'PATRONES PERSONALES'),
            'sleep': ('Mi descanso', 'SUEÑO Y RECUPERACIÓN'),
            'movement': ('Moverme a mi manera', 'ACTIVIDAD COTIDIANA'),
            'water': ('Mi agua', 'HIDRATACIÓN'),
            'meals': ('Mi semana en comidas', 'RITMO ALIMENTARIO'),
            'body_checkin': ('Escuchar mi cuerpo', 'CHECK-IN CORPORAL'),
            'balance': ('Equilibrio de mi semana', 'MIS ÁREAS'),
            'routines': ('Mis rutinas de bienestar', 'MAÑANA, DÍA, NOCHE'),
            'review': ('Lo que aprendí', 'REVISIÓN DE BIENESTAR'),
        }
        if template in titles:
            title, subtitle = titles[template]
            a.text(title, 60, 130, 18, 'Bold')
            a.text(subtitle, 60, 155, 12)
            a.lines(60, 280, 380, 6, 40)

def draw_selfcare_page(a, p):
    """Draw AUTOCUIDADO collection pages."""
    a.box(0, 0, W, H, '#ECE8EF', r=0)
    a.box(25, 65, 435, 867, '#F8F5F0', r=13)

    if p['kind'] == 'self-divisor':
        a.text('AUTOCUIDADO', 250, 380, 32, 'Editorial', center=True)
        a.text('Volver a mí', 250, 450, 14, 'Editorial', center=True)
    else:
        template = p.get('template')
        titles = {
            'needs': ('Volver a escucharme', 'QUÉ NECESITO HOY'),
            'menu': ('Mi menú de autocuidado', 'SEGÚN TIEMPO Y CONTEXTO'),
            'boundaries': ('Cuidar también es poner límites', 'MIS LÍMITES'),
            'release': ('No todo necesita quedarse conmigo', 'COSAS QUE PUEDO SOLTAR'),
            'pause': ('Mi pausa', 'UN RATO PARA MÍ'),
            'disconnect': ('Un rato fuera del ruido', 'DESCONECTAR'),
            'me_time': ('Una cita conmigo', 'TIEMPO PARA MÍ'),
            'support': ('No tengo que hacer todo sola/o', 'PEDIR APOYO'),
            'gestures': ('Algo pequeño también cuenta', 'PEQUEÑOS GESTOS'),
            'recharge': ('Cosas a las que puedo volver', 'MI CAJA DE RECARGA'),
            'review': ('Lo que quiero cuidar mejor', 'REVISIÓN DE AUTOCUIDADO'),
        }
        if template in titles:
            title, subtitle = titles[template]
            a.text(title, 60, 130, 18, 'Bold')
            a.text(subtitle, 60, 155, 12)
            a.lines(60, 280, 380, 6, 40)

def draw_finance_page(a, p):
    """Draw FINANZAS collection pages."""
    a.box(0, 0, W, H, '#ECE8EF', r=0)
    a.box(25, 65, 435, 867, '#F8F5F0', r=13)

    if p['kind'] == 'fin-divisor':
        a.text('FINANZAS', 250, 380, 32, 'Editorial', center=True)
        a.text('Decisiones con intención', 250, 450, 14, 'Editorial', center=True)
    else:
        template = p.get('template')
        titles = {
            'overview': ('Verlo todo más claro', 'MI PANORAMA FINANCIERO'),
            'budget': ('Presupuesto mensual', 'PLAN VS REALIDAD'),
            'expenses': ('Registro de gastos', 'EN QUÉ SE FUE'),
            'bills': ('Facturas y pagos', 'QUE NADA ME TOME POR SORPRESA'),
            'subscriptions': ('Mis suscripciones', 'LO QUE PAGO CADA MES'),
            'savings': ('Plan de ahorro', 'AHORRAR PARA ALGO CONCRETO'),
            'funds': ('Fondos y sobres', 'DINERO CON PROPÓSITO'),
            'debts': ('Deudas y compromisos', 'TENERLO CLARO'),
            'purchases': ('Compras planificadas', 'ANTES DE COMPRAR'),
            'calendar': ('Calendario financiero', 'FECHAS QUE IMPORTAN'),
            'review': ('Cierre financiero', 'CERRAR EL MES CON CLARIDAD'),
        }
        if template in titles:
            title, subtitle = titles[template]
            a.text(title, 60, 130, 18, 'Bold')
            a.text(subtitle, 60, 155, 12)
            a.lines(60, 280, 380, 6, 40)

def draw_study_page(a, p):
    """Draw ESTUDIO collection pages."""
    a.box(0, 0, W, H, '#ECE8EF', r=0)
    a.box(25, 65, 435, 867, '#F8F5F0', r=13)

    if p['kind'] == 'study-divisor':
        a.text('ESTUDIO', 250, 380, 32, 'Editorial', center=True)
        a.text('Aprender, conectar, crecer', 250, 450, 14, 'Editorial', center=True)
    else:
        template = p.get('template')
        titles = {
            'plan': ('Mi plan de estudio', 'VISIÓN GENERAL DEL CURSO'),
            'map': ('Todo lo que tengo que aprender', 'MAPA DE CONTENIDOS'),
            'week': ('Semana de estudio', 'QUÉ ESTUDIO ESTA SEMANA'),
            'session': ('Hoy estudio...', 'SESIÓN DE APRENDIZAJE'),
            'notes': ('Mis apuntes', 'NOTAS ESTRUCTURADAS'),
            'summary': ('Entenderlo en una página', 'RESUMEN DEL TEMA'),
            'questions': ('¿Realmente lo recuerdo?', 'PREGUNTAS DE REPASO'),
            'review': ('Volver antes de olvidar', 'TRACKER DE REPASO'),
            'assessments': ('Lo que viene', 'EVALUACIONES Y ENTREGAS'),
            'resources': ('Mi biblioteca de aprendizaje', 'MIS RECURSOS'),
            'reflection': ('Lo que ya sé ahora', 'REVISIÓN DE APRENDIZAJE'),
        }
        if template in titles:
            title, subtitle = titles[template]
            a.text(title, 60, 130, 18, 'Bold')
            a.text(subtitle, 60, 155, 12)
            a.lines(60, 280, 380, 6, 40)

def draw_organization_page(a, p):
    """Draw ORGANIZACIÓN collection pages."""
    a.box(0, 0, W, H, '#ECE8EF', r=0)
    a.box(25, 65, 435, 867, '#F8F5F0', r=13)

    if p['kind'] == 'org-divisor':
        a.text('ORGANIZACIÓN', 250, 380, 32, 'Editorial', center=True)
        a.text('Un lugar para cada cosa', 250, 450, 14, 'Editorial', center=True)
    else:
        template = p.get('template')
        titles = {
            'pending': ('Lo que tengo pendiente', 'TODO EN SU LUGAR'),
            'home': ('Mi hogar', 'ESPACIOS ORGANIZADOS'),
            'maintenance': ('Limpieza y mantenimiento', 'CUIDADO DEL HOGAR'),
            'shopping': ('Lista de compras', 'QUÉ NECESITO COMPRAR'),
            'inventory': ('Lo que ya tengo', 'INVENTARIO DEL HOGAR'),
            'errands': ('Cosas que tengo que resolver', 'RECADOS'),
            'documents': ('Documentos importantes', 'LO QUE NECESITO GUARDAR'),
            'repairs': ('Cosas por reparar', 'A RESOLVER'),
            'declutter': ('Para donar/vender/descartar', 'LIMPIAR'),
            'packing': ('Preparar y empacar', 'ANTES DE SALIR'),
            'reset': ('Volver a poner todo en orden', 'RESET'),
        }
        if template in titles:
            title, subtitle = titles[template]
            a.text(title, 60, 130, 18, 'Bold')
            a.text(subtitle, 60, 155, 12)
            a.lines(60, 280, 380, 6, 40)

def draw_notes_page(a, p):
    """Draw NOTAS collection pages."""
    a.box(0, 0, W, H, '#ECE8EF', r=0)
    a.box(25, 65, 435, 867, '#F8F5F0', r=13)

    if p['kind'] == 'notes-divisor':
        a.text('NOTAS', 250, 380, 32, 'Editorial', center=True)
        a.text('Ideas que merecen quedarse', 250, 450, 14, 'Editorial', center=True)
    else:
        template = p.get('template')
        titles = {
            'lined': ('Notas libres', 'LÍNEAS PARA ESCRIBIR'),
            'dotted': ('Puntos', 'PÁGINA PUNTEADA'),
            'grid': ('Cuadrícula', 'PARA ESQUEMAS Y DIAGRAMAS'),
            'blank': ('Página en blanco', 'TUYA PARA CREAR'),
            'idea': ('Una idea para recordar', 'IDEAS'),
            'quick': ('Que no se me olvide', 'LISTA RÁPIDA'),
            'mindmap': ('Mapa mental', 'CONECTAR IDEAS'),
            'compare': ('Ponerlo lado a lado', 'COMPARAR'),
            'meeting': ('Reunión o conversación', 'PUNTOS IMPORTANTES'),
            'capture': ('Lo anoto ahora', 'CAPTURAR RÁPIDO'),
            'mixed': ('A mi manera', 'PÁGINA MIXTA'),
        }
        if template in titles:
            title, subtitle = titles[template]
            a.text(title, 60, 130, 18, 'Bold')
            a.text(subtitle, 60, 155, 12)
            a.lines(60, 280, 380, 6, 40)

def draw_extras_page(a, p):
    """Draw EXTRAS collection pages."""
    a.box(0, 0, W, H, '#ECE8EF', r=0)
    a.box(25, 65, 435, 867, '#F8F5F0', r=13)

    if p['kind'] == 'extras-divisor':
        a.text('EXTRAS', 250, 380, 32, 'Editorial', center=True)
        a.text('Pequeños extras que hacen la diferencia', 250, 450, 14, 'Editorial', center=True)
    else:
        template = p.get('template')
        titles = {
            'functional': ('Stickers funcionales', 'ELEMENTOS VISUALES'),
            'life': ('Stickers de vida', 'ICONOGRAFÍA'),
            'labels': ('Etiquetas', 'MARCADORES VISUALES'),
            'checks': ('Checkboxes y marcadores', 'SEÑALIZADORES'),
            'numbers': ('Números', '1–31'),
            'months': ('Meses', 'ENE–DIC'),
            'weekdays': ('Días de la semana', 'LUNES–DOMINGO'),
            'mood': ('Mood & weather', 'ESTADOS Y CLIMA'),
            'decorative': ('Decorativos', 'ELEMENTOS BONITOS'),
            'paper': ('Papelitos y notas', 'FORMAS ESPECIALES'),
            'free': ('Mi página extra', 'HAZLA TUYA'),
        }
        if template in titles:
            title, subtitle = titles[template]
            a.text(title, 60, 130, 18, 'Bold')
            a.text(subtitle, 60, 155, 12)
            a.lines(60, 280, 380, 6, 40)

def draw_annual_page(a, p):
    """Draw front matter and annual overview pages."""
    if p['kind'] == 'portada':
        cover(a)
    elif p['kind'] == 'dashboard':
        dashboard(a)
    elif p['kind'] == 'menu':
        menu(a)
    elif p['kind'] == 'year-selector':
        a.text("YOYI'R", 60, 127, 16, 'Editorial')
        a.text('ELIGE TU AÑO', 60, 166, 29, 'Editorial')
        for i, year in enumerate((2026, 2027, 2028)):
            a.chip(str(year), f'year-{year}', 58 + i * 130, 201, 122, COLORS[[0, 7, 5][i]])
    elif p['kind'] == 'annual':
        annual(a, p['year'])
    elif p['kind'] == 'quarter':
        a.box(0, 0, W, H, '#ECE8EF', r=0)
        a.box(25, 65, 435, 867, '#F8F5F0', r=13)
        a.text(f"TRIMESTRE {p['quarter']}", 60, 130, 18, 'Bold')
        a.text(p['months'], 60, 155, 12)
        a.lines(60, 250, 380, 4, 40)

def build_master_final():
    """Build complete MASTER: 1532 pages (all 10 collections)."""
    register_fonts()

    annual = annual_core_block()
    objectives = objectives_collection()
    life = life_collection()
    productivity = productivity_collection()
    wellness = wellness_collection()
    selfcare = selfcare_collection()
    finance = finance_collection()
    study = study_collection()
    organization = organization_collection()
    notes = notes_collection()
    extras = extras_collection()
    dated_pages, dated_known = dated_core_block()

    all_pages = annual + objectives + life + productivity + wellness + selfcare + finance + study + organization + notes + extras + dated_pages
    known = {p['id'] for p in all_pages}
    nav = []
    future = []
    arts = []

    for i, p in enumerate(all_pages):
        p['previous'] = all_pages[i - 1]['id'] if i > 0 else 'portada'
        p['next'] = all_pages[i + 1]['id'] if i + 1 < len(all_pages) else 'portada'

        # Reorganizar navegación: YEAR_OVERVIEW salta directo a enero del mismo año
        if p['kind'] == 'annual':
            year = p['year']
            p['next'] = f'cal-{year}-01'

        # Recursos anuales: navegar entre recursos, no a meses
        if p['kind'] == 'resource':
            year = p['year']
            resources_list = ['goals', 'dates', 'birthdays', 'projects', 'finance', 'personal', 'wellness', 'professional', 'vision', 'review']
            resource_idx = resources_list.index(p['resource'])
            if resource_idx > 0:
                p['previous'] = f'res-{year}-{resources_list[resource_idx - 1]}'
            if resource_idx < len(resources_list) - 1:
                p['next'] = f'res-{year}-{resources_list[resource_idx + 1]}'

        # Trimestres: navegar entre trimestres
        if p['kind'] == 'quarter':
            year = p['year']
            q = p['quarter']
            if q > 1:
                p['previous'] = f'q-{year}-{q - 1}'
            if q < 4:
                p['next'] = f'q-{year}-{q + 1}'

    out = OUTPUT / '.build'
    out.mkdir(parents=True, exist_ok=True)
    pdf = out / 'YOYIR-DIGITAL-PLANNER-MASTER.pdf'

    c = canvas.Canvas(str(pdf), pagesize=(W, H), pageCompression=1, pdfVersion=(1, 4), invariant=1)
    c.setTitle("YOYI'R · Digital Planner 2026–2028")
    c.setAuthor("E-books para la vida — YOYI'R")

    for i, p in enumerate(all_pages):
        c.bookmarkPage(p['id'], fit='Fit')
        a = BlockArt(c, p['id'], nav, known)

        if p['kind'] == 'resource':
            draw_resource_page(a, p)
        elif p['kind'] in ('obj-divisor', 'obj-page'):
            draw_objectives_page(a, p)
            # Global navigation for OBJECTIVES collection
            a.link('dashboard', 60, 50, 80, 40, 'INICIO', minimum=0)
            a.link('menu', 160, 50, 80, 40, 'MENÚ', minimum=0)
            a.link('obj-div', 260, 50, 140, 40, 'OBJETIVOS', minimum=0)
        elif p['kind'] in ('life-divisor', 'life-page'):
            draw_life_page(a, p)
            # Global navigation for LIFE collection
            a.link('dashboard', 60, 50, 80, 40, 'INICIO', minimum=0)
            a.link('menu', 160, 50, 80, 40, 'MENÚ', minimum=0)
            a.link('life-div', 260, 50, 140, 40, 'VIDA', minimum=0)
        elif p['kind'] in ('prod-divisor', 'prod-page'):
            draw_productivity_page(a, p)
            # Global navigation for PRODUCTIVITY collection
            a.link('dashboard', 60, 50, 80, 40, 'INICIO', minimum=0)
            a.link('menu', 160, 50, 80, 40, 'MENÚ', minimum=0)
            a.link('prod-div', 260, 50, 140, 40, 'PRODUCTIVIDAD', minimum=0)
        elif p['kind'] in ('well-divisor', 'well-page'):
            draw_wellness_page(a, p)
            # Global navigation for WELLNESS collection
            a.link('dashboard', 60, 50, 80, 40, 'INICIO', minimum=0)
            a.link('menu', 160, 50, 80, 40, 'MENÚ', minimum=0)
            a.link('well-div', 260, 50, 140, 40, 'BIENESTAR', minimum=0)
        elif p['kind'] in ('self-divisor', 'self-page'):
            draw_selfcare_page(a, p)
            # Global navigation for SELFCARE collection
            a.link('dashboard', 60, 50, 80, 40, 'INICIO', minimum=0)
            a.link('menu', 160, 50, 80, 40, 'MENÚ', minimum=0)
            a.link('self-div', 260, 50, 140, 40, 'AUTOCUIDADO', minimum=0)
        elif p['kind'] in ('fin-divisor', 'fin-page'):
            draw_finance_page(a, p)
            # Global navigation for FINANCE collection
            a.link('dashboard', 60, 50, 80, 40, 'INICIO', minimum=0)
            a.link('menu', 160, 50, 80, 40, 'MENÚ', minimum=0)
            a.link('fin-div', 260, 50, 140, 40, 'FINANZAS', minimum=0)
        elif p['kind'] in ('study-divisor', 'study-page'):
            draw_study_page(a, p)
            # Global navigation for STUDY collection
            a.link('dashboard', 60, 50, 80, 40, 'INICIO', minimum=0)
            a.link('menu', 160, 50, 80, 40, 'MENÚ', minimum=0)
            a.link('study-div', 260, 50, 140, 40, 'ESTUDIO', minimum=0)
        elif p['kind'] in ('org-divisor', 'org-page'):
            draw_organization_page(a, p)
            # Global navigation for ORGANIZATION collection
            a.link('dashboard', 60, 50, 80, 40, 'INICIO', minimum=0)
            a.link('menu', 160, 50, 80, 40, 'MENÚ', minimum=0)
            a.link('org-div', 260, 50, 140, 40, 'ORGANIZACIÓN', minimum=0)
        elif p['kind'] in ('notes-divisor', 'notes-page'):
            draw_notes_page(a, p)
            # Global navigation for NOTES collection
            a.link('dashboard', 60, 50, 80, 40, 'INICIO', minimum=0)
            a.link('menu', 160, 50, 80, 40, 'MENÚ', minimum=0)
            a.link('notes-div', 260, 50, 140, 40, 'NOTAS', minimum=0)
        elif p['kind'] in ('extras-divisor', 'extras-page'):
            draw_extras_page(a, p)
            # Global navigation for EXTRAS collection
            a.link('dashboard', 60, 50, 80, 40, 'INICIO', minimum=0)
            a.link('menu', 160, 50, 80, 40, 'MENÚ', minimum=0)
            a.link('extras-div', 260, 50, 140, 40, 'EXTRAS', minimum=0)
        elif p['kind'] in ('portada', 'dashboard', 'menu', 'year-selector', 'annual', 'quarter'):
            draw_annual_page(a, p)

            # Agregar navegación principal con formas individuales
            if p['kind'] == 'dashboard':
                # Year chips (horizontal row): 2026, 2027, 2028
                a.link('year-2026', 58, 201, 122, 68, 'YEAR_2026', minimum=0)
                a.link('year-2027', 188, 201, 122, 68, 'YEAR_2027', minimum=0)
                a.link('year-2028', 318, 201, 122, 68, 'YEAR_2028', minimum=0)
                # SIN FECHA chip
                a.link('sin-fecha', 58, 282, 162, 33, 'SIN_FECHA', minimum=0)
                # OBJETIVOS - sticky (left)
                a.link('obj-div', 58, 374, 236, 154, 'OBJETIVOS')
                # VIDA - circular (right)
                a.link('life-div', 309, 374, 133, 154, 'VIDA')
                # BIENESTAR - box (left)
                a.link('well-div', 58, 545, 133, 139, 'WELLNESS')
                # PRODUCTIVIDAD - box (right)
                a.link('prod-div', 207, 545, 235, 139, 'PRODUCTIVITY')
                # Bottom row chips: FINANZAS, ESTUDIO, NOTAS, EXTRAS
                a.link('fin-div', 58, 700, 184, 50, 'FINANCE', minimum=0)
                # ESTUDIO
                a.link('study-div', 258, 700, 184, 50, 'STUDY', minimum=0)
                # NOTAS
                a.link('notes-div', 58, 773, 184, 50, 'NOTES', minimum=0)
                # EXTRAS
                a.link('extras-div', 258, 773, 184, 50, 'EXTRAS', minimum=0)
            elif p['kind'] == 'menu':
                # Menu entries - each 64pt tall with circle icon + text
                a.link('obj-div', 58, 200, 384, 64, 'OBJECTIVES')
                a.link('life-div', 58, 264, 384, 64, 'LIFE')
                a.link('prod-div', 58, 328, 384, 64, 'PRODUCTIVITY')
                a.link('well-div', 58, 392, 384, 64, 'WELLNESS')
                a.link('self-div', 58, 456, 384, 64, 'SELFCARE')
                a.link('fin-div', 58, 520, 384, 64, 'FINANCE')
                a.link('study-div', 58, 584, 384, 64, 'STUDY')
                a.link('org-div', 58, 648, 384, 64, 'ORGANIZATION')
                a.link('notes-div', 58, 712, 384, 64, 'NOTES')
                a.link('extras-div', 58, 776, 384, 64, 'EXTRAS')
        else:
            digital_planner_shell(a, p, i, len(all_pages))
            draw_block_page(a, p)

        future += a.future
        arts.append(a)
        c.showPage()

    c.save()
    return pdf, all_pages

if __name__ == '__main__':
    candidate, pages = build_master_final()

    manifest = {
        'FRONT_MATTER': sum(1 for p in pages if p['kind'] in ('portada', 'dashboard', 'menu', 'year-selector')),
        'YEAR_OVERVIEWS': sum(1 for p in pages if p['kind'] == 'annual'),
        'ANNUAL_RESOURCES': sum(1 for p in pages if p['kind'] == 'resource'),
        'QUARTERS': sum(1 for p in pages if p['kind'] == 'quarter'),
        'OBJECTIVES': sum(1 for p in pages if p['kind'] in ('obj-divisor', 'obj-page')),
        'LIFE': sum(1 for p in pages if p['kind'] in ('life-divisor', 'life-page')),
        'PRODUCTIVITY': sum(1 for p in pages if p['kind'] in ('prod-divisor', 'prod-page')),
        'WELLNESS': sum(1 for p in pages if p['kind'] in ('well-divisor', 'well-page')),
        'SELFCARE': sum(1 for p in pages if p['kind'] in ('self-divisor', 'self-page')),
        'FINANCE': sum(1 for p in pages if p['kind'] in ('fin-divisor', 'fin-page')),
        'STUDY': sum(1 for p in pages if p['kind'] in ('study-divisor', 'study-page')),
        'ORGANIZATION': sum(1 for p in pages if p['kind'] in ('org-divisor', 'org-page')),
        'NOTES': sum(1 for p in pages if p['kind'] in ('notes-divisor', 'notes-page')),
        'EXTRAS': sum(1 for p in pages if p['kind'] in ('extras-divisor', 'extras-page')),
        'MONTH_DIVIDERS': sum(1 for p in pages if p['kind'] == 'divider'),
        'MONTH_CALENDARS': sum(1 for p in pages if p['kind'] == 'calendar'),
        'MONTH_INTENTIONS': sum(1 for p in pages if p['kind'] == 'plan'),
        'WEEKS': sum(1 for p in pages if p['kind'] == 'week'),
        'DAYS': sum(1 for p in pages if p['kind'] == 'day'),
    }

    total = len(pages)
    manifest_total = sum(manifest.values())

    print(f'\nMASTER FINAL BUILD')
    print(f'TOTAL PAGES: {total}')
    for k, v in manifest.items():
        print(f'{k}: {v}')
    print(f'MANIFEST TOTAL: {manifest_total}')

    try:
        doc = fitz.open(str(candidate))
        integrity = len(doc) == total == manifest_total == 1532
        doc.close()

        print(f'INTEGRITY: {"PASS" if integrity else "FAIL"}')

        if integrity:
            master = OUTPUT / 'YOYIR-DIGITAL-PLANNER-MASTER.pdf'
            candidate.replace(master)
            print('[OK] MASTER replaced')
    except Exception as e:
        print(f'[ERROR] {e}')
