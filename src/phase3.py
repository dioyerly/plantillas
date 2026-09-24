"""Fase 3: biblioteca premium de plantillas integrada en el Master."""
import json, time, unicodedata
from pathlib import Path
from reportlab.pdfgen import canvas
from pypdf import PdfReader
import fitz
from .config import ROOT, OUTPUT, DOCS, WIDTH, HEIGHT
from .components import Drawing, register_fonts
from .navigation import Navigation
from .themes import THEMES
from .phase2 import phase2_pages, render_phase2, draw_page, nav_button, footer, panel, header, L, NAV

MODULES = {
 'objetivos': ('OBJETIVOS', ['MI VISIÓN','OBJETIVOS DEL AÑO','OBJETIVOS A 5 AÑOS','OBJETIVOS A 3 AÑOS','OBJETIVOS A 1 AÑO','OBJETIVOS TRIMESTRALES','OBJETIVOS DEL MES','OBJETIVOS DE LA SEMANA','META SMART','PLAN DE ACCIÓN','MAPA DE METAS','SEGUIMIENTO DE OBJETIVOS','PROGRESO DE METAS','HITOS','OBSTÁCULOS Y SOLUCIONES','REVISIÓN DE META','LOGROS','LECCIONES APRENDIDAS']),
 'vida': ('VIDA', ['TABLERO DE VISIÓN','MI VIDA IDEAL','RUEDA DE LA VIDA','LISTA DE SUEÑOS','LISTA DE DESEOS','COSAS QUE QUIERO APRENDER','EXPERIENCIAS QUE QUIERO VIVIR','LUGARES QUE QUIERO CONOCER','MIS FAVORITOS','FRASES FAVORITAS','RECUERDOS','DIARIO DE SUEÑOS','CARTA A MI YO FUTURO','MI AÑO EN FOTOS','CALENDARIO DE CUMPLEAÑOS','FECHAS IMPORTANTES','ANIVERSARIOS','REGALOS','IDEAS DE REGALOS','REGALOS COMPRADOS','CONTACTOS IMPORTANTES','PLANIFICADOR DEL HOGAR','LIMPIEZA DIARIA','LIMPIEZA SEMANAL','LIMPIEZA MENSUAL','LIMPIEZA ESTACIONAL','LISTA DE TAREAS DEL HOGAR','PROYECTOS DEL HOGAR','MANTENIMIENTO','INVENTARIO DEL HOGAR','COMPRAS PARA EL HOGAR','ORGANIZACIÓN POR HABITACIÓN','DEPURACIÓN DEL HOGAR','VIAJES SOÑADOS','PLANIFICADOR DE VIAJE','PRESUPUESTO DE VIAJE','ITINERARIO','RESERVAS','VUELOS','ALOJAMIENTO','TRANSPORTE','ACTIVIDADES','RESTAURANTES','LISTA DE EQUIPAJE','DOCUMENTOS','GASTOS DEL VIAJE','DIARIO DE VIAJE','RECUERDOS DEL VIAJE','LISTA DE LECTURA','LIBROS POR LEER','LIBROS LEÍDOS','REGISTRO DE LECTURA','RESEÑA DE LIBRO','RETO DE LECTURA','CITAS FAVORITAS','AUTORES FAVORITOS','SERIES / SAGAS','PRÉSTAMOS DE LIBROS','PELÍCULAS POR VER','PELÍCULAS VISTAS','SERIES POR VER','SEGUIMIENTO DE SERIES','DOCUMENTALES','PODCASTS','MÚSICA','FAVORITOS DEL MES','LISTA DE COMPRAS','LISTA DEL SUPERMERCADO','LISTA DE DESEOS','COMPRAS PENDIENTES','SEGUIMIENTO DE PEDIDOS','COMPARADOR DE PRODUCTOS']),
 'productividad': ('PRODUCTIVIDAD', ['DESCARGA MENTAL','MATRIZ DE PRIORIDADES','BLOQUES DE TIEMPO','SEGUIMIENTO DEL TIEMPO','SESIÓN DE ENFOQUE','PLANIFICADOR DE PROYECTOS','SEGUIMIENTO DE PROYECTOS','PLANIFICADOR DE REUNIONES','NOTAS DE REUNIÓN','CITAS','LISTA MAESTRA','LISTA DE TAREAS','TAREAS DEL MES','TAREAS DE LA SEMANA','TAREAS DEL DÍA','RUTINA DE MAÑANA','RUTINA DE NOCHE','RUTINA SEMANAL','SEGUIMIENTO DE HÁBITOS','RETO DE 30 DÍAS','PLAN 30 / 60 / 90 DÍAS','REVISIÓN DE PRODUCTIVIDAD']),
 'bienestar': ('BIENESTAR', ['MI BIENESTAR','RUEDA DEL BIENESTAR','ESTADO DE ÁNIMO','ENERGÍA','SUEÑO','HIDRATACIÓN','MOVIMIENTO','PASOS','ENTRENAMIENTO','PLAN SEMANAL DE MOVIMIENTO','REGISTRO DE ENTRENAMIENTO','FUERZA','CARDIO','CAMINATA / CARRERA','COMIDAS','PLANIFICADOR DE COMIDAS','IDEAS DE COMIDAS','LISTA DE ALIMENTOS','INVENTARIO DE DESPENSA','RECETAS','RUTINAS DE BIENESTAR','REFLEXIÓN DE BIENESTAR']),
 'autocuidado': ('AUTOCUIDADO', ['MIS IDEAS DE AUTOCUIDADO','MENÚ DE AUTOCUIDADO','TARRO DE AUTOCUIDADO','RETO DE 30 DÍAS','MOMENTOS CONSCIENTES','GRATITUD DIARIA','GRATITUD SEMANAL','BANCO DE GRATITUD','CARTA DE GRATITUD','AFIRMACIONES','MIS AFIRMACIONES','REFLEXIÓN DIARIA','REFLEXIÓN SEMANAL','REFLEXIÓN MENSUAL','DIARIO DE 5 MINUTOS','PENSAMIENTOS','LO QUE PUEDO CONTROLAR','LO QUE QUIERO SOLTAR','MIS LÍMITES','TIEMPO PARA MÍ','COSAS QUE ME HACEN BIEN','PEQUEÑAS VICTORIAS','CARTA A MI YO FUTURO'])
}
COLORS={'objetivos':'lavender','vida':'blush','productividad':'sky','bienestar':'sage','autocuidado':'sand'}

def slug(s):
    return ''.join(c for c in unicodedata.normalize('NFKD',s.lower()) if not unicodedata.combining(c)).replace(' ','-').replace('/','-')
def tid(cat,name): return f'plantilla-{cat}-{slug(name)}'

def library_pages():
    pages=[]
    def add(i,t,k,**kw): pages.append(dict(id=i,title=t,kind=k,theme=COLORS.get(kw.get('category'),'lavender'),**kw))
    add('biblioteca','PLANTILLAS · BIBLIOTECA PREMIUM','library_home')
    add('extras-cuadernos','EXTRAS · CUADERNOS DIGITALES','extras')
    add('extras-stickers','EXTRAS · STICKERS DIGITALES','extras_stickers')
    add('favoritas','MIS PLANTILLAS FAVORITAS','favorites')
    add('plantillas','PLANTILLAS DUPLICABLES','duplicates')
    for cat,(title,names) in MODULES.items():
        add(f'hub-{cat}',title,'hub',category=cat)
        for chunk in range((len(names)+15)//16):
            suffix='' if chunk==0 else f'-{chunk+1}'
            add(f'indice-{cat}{suffix}',f'ÍNDICE · {title}{suffix}','index',category=cat,chunk=chunk)
        seen={}
        for n in names:
            pid=tid(cat,n); seen[pid]=seen.get(pid,0)+1; suffix='' if seen[pid]==1 else f'-{seen[pid]}'
            title_name=n if seen[pid]==1 else f'{n} · COMPRAS'
            add(pid+suffix,title_name,'template',category=cat)
    return pages

def lib_nav(d,label,target,x,y,w=156,h=70): nav_button(d,label,target,x,y,w,h)
def lib_footer(d,cat,index): footer(d,[('INICIO','inicio'),('BIBLIOTECA','biblioteca'),('ÍNDICE',index),('SECCIÓN',f'hub-{cat}')])

def lib_panel(d,label,x,y,w,h): panel(d,label,x,y,w,h)
def draw_template(d,p):
    cat=p['category']; name=p['title']; header(d,name,MODULES[cat][0])
    if name=='META SMART':
        fields=['MI META','ESPECÍFICA · ¿QUÉ QUIERO CONSEGUIR?','MEDIBLE · ¿CÓMO MEDIRÉ MI PROGRESO?','ALCANZABLE · ¿QUÉ NECESITO?','RELEVANTE · ¿POR QUÉ ES IMPORTANTE?','CON PLAZO · ¿CUÁNDO QUIERO CONSEGUIRLA?','PRIMER PASO','PRÓXIMAS ACCIONES','FECHA OBJETIVO','PROGRESO','NOTAS']
        for i,f in enumerate(fields): lib_panel(d,f,24+(i%2)*252,200+(i//2)*116,240,100)
    elif name=='PLAN DE ACCIÓN':
        for i,f in enumerate(['OBJETIVO','RESULTADO DESEADO','FECHA LÍMITE','PASOS','PRIORIDAD','RESPONSABLE','RECURSOS','ESTADO','PRÓXIMA ACCIÓN','NOTAS']): lib_panel(d,f,24+(i%2)*252,200+(i//2)*116,240,100)
    elif name=='MATRIZ DE PRIORIDADES':
        for i,f in enumerate(['URGENTE + IMPORTANTE · HACER','IMPORTANTE + NO URGENTE · PLANIFICAR','URGENTE + NO IMPORTANTE · DELEGAR','NO URGENTE + NO IMPORTANTE · RECONSIDERAR']): lib_panel(d,f,24+(i%2)*252,205+(i//2)*250,240,220)
    elif name=='SEGUIMIENTO DE HÁBITOS':
        lib_panel(d,'HÁBITOS DEL MES · 1–15',24,205,492,270); lib_panel(d,'HÁBITOS DEL MES · 16–31',24,500,492,270)
        d.text('Escribe hasta 12 hábitos y marca cada día.',24,800,14,'Body')
    elif name=='REGISTRO DE SUEÑO' or name=='SUEÑO':
        for i,f in enumerate(['FECHA','HORA DE DORMIR','HORA DE DESPERTAR','HORAS DE SUEÑO','CALIDAD PERCIBIDA','ENERGÍA AL DESPERTAR','NOTAS']): lib_panel(d,f,24,205+i*82,492,68)
    elif name=='REGISTRO DE ENTRENAMIENTO' or name in ('ENTRENAMIENTO','FUERZA','CARDIO','CAMINATA / CARRERA'):
        for i,f in enumerate(['FECHA','TIPO DE ENTRENAMIENTO','DURACIÓN','EJERCICIO','SERIES / REPETICIONES','CARGA / RESISTENCIA','INTENSIDAD PERCIBIDA','NOTAS']): lib_panel(d,f,24+(i%2)*252,205+(i//2)*145,240,125)
    elif name=='PLANIFICADOR DE COMIDAS':
        for i,day in enumerate(['LUNES','MARTES','MIÉRCOLES','JUEVES','VIERNES','SÁBADO','DOMINGO']): lib_panel(d,day,24+(i%2)*252,200+(i//2)*130,240,110)
        lib_panel(d,'LISTA DE COMPRAS / PREPARACIÓN / NOTAS',24,730,492,120)
    elif name=='RECETAS':
        for i,f in enumerate(['NOMBRE','CATEGORÍA','PORCIONES','TIEMPO','INGREDIENTES','PREPARACIÓN','NOTAS','VALORACIÓN PERSONAL']): lib_panel(d,f,24+(i%2)*252,200+(i//2)*145,240,125)
    elif name=='DIARIO DE 5 MINUTOS':
        for i,f in enumerate(['MAÑANA · HOY AGRADEZCO...','HOY QUIERO SENTIR...','MI PRIORIDAD PERSONAL...','ALGO QUE PUEDO HACER POR MÍ...','NOCHE · ALGO BUENO DE HOY...','ALGO QUE APRENDÍ...','ALGO QUE QUIERO DEJAR IR...','MAÑANA QUIERO...']): lib_panel(d,f,24+(i%2)*252,200+(i//2)*145,240,125)
    elif name=='RESEÑA DE LIBRO':
        for i,f in enumerate(['TÍTULO','AUTOR','GÉNERO','FECHA','VALORACIÓN','PERSONAJES','LO QUE MÁS ME GUSTÓ','FRASE FAVORITA','MIS NOTAS','¿LO RECOMENDARÍA?']): lib_panel(d,f,24+(i%2)*252,200+(i//2)*116,240,100)
    else:
        prompts={'MI VISIÓN':['CÓMO QUIERO SENTIRME','LO QUE QUIERO CREAR','MI PRÓXIMO PASO'], 'PLANIFICADOR DE VIAJE':['DESTINO / FECHAS','RESERVAS','PRESUPUESTO','ITINERARIO'], 'CONTACTOS IMPORTANTES':['NOMBRE','TELÉFONO','CORREO','DIRECCIÓN','NOTAS'], 'REFLEXIÓN DIARIA':['¿QUÉ DISFRUTÉ?','¿QUÉ ME DRENÓ ENERGÍA?','¿QUÉ QUIERO REPETIR?'], 'REFLEXIÓN SEMANAL':['¿QUÉ PUEDO SIMPLIFICAR?','¿QUÉ APRENDÍ?','¿QUÉ NECESITA ATENCIÓN?'], 'REFLEXIÓN MENSUAL':['¿QUÉ QUIERO CAMBIAR?','¿QUÉ LOGRO QUIERO RECONOCER?','PRÓXIMO ENFOQUE?']}
        fs=prompts.get(name,['ENFOQUE','OBJETIVOS','PRIORIDADES','ACCIONES','NOTAS'])
        for i,f in enumerate(fs): lib_panel(d,f,24+(i%2)*252,205+(i//2)*160,240,140)
    lib_footer(d,cat,f'indice-{cat}')

def draw_library(d,p):
    k=p['kind']; cat=p.get('category')
    if k=='library_home':
        header(d,'BIBLIOTECA PREMIUM','PLANTILLAS PARA TU VIDA REAL')
        cats=list(MODULES)
        for i,c in enumerate(cats): lib_nav(d,MODULES[c][0],f'hub-{c}',24+(i%2)*252,210+(i//2)*120,240,90)
        lib_nav(d,'MIS PLANTILLAS FAVORITAS','favoritas',24,700,240,80); lib_nav(d,'PLANTILLAS DUPLICABLES','plantillas',276,700,240,80); footer(d,[('INICIO','inicio'),('AÑO','selector-anio'),('EXTRAS','extras-cuadernos'),('BIBLIOTECA','biblioteca')]); return
    if k=='extras':
        header(d,'EXTRAS · CUADERNOS DIGITALES','ARCHIVOS INDEPENDIENTES')
        panel(d,'CUADERNO DE NOTAS',24,205,240,110); panel(d,'CUADERNO DE ESTUDIO',276,205,240,110); panel(d,'CUADERNO DE PROYECTOS',24,335,240,110); panel(d,'CUADERNO DE IDEAS',276,335,240,110); panel(d,'CUADERNO DE BIENESTAR',24,465,240,110); panel(d,'MI CUADERNO',276,465,240,110)
        d.paragraph('Los seis cuadernos se entregan como archivos PDF independientes dentro del paquete. Puedes importarlos por separado en tu aplicación de anotación.',24,635,480,16,24)
        d.paragraph('Las portadas y bibliotecas de cada cuaderno son recursos intercambiables. Este catálogo no intenta abrir archivos externos mediante enlaces PDF.',24,735,480,16,24)
        lib_nav(d,'STICKERS DIGITALES','extras-stickers',24,790,240,70); footer(d,[('INICIO','inicio'),('BIBLIOTECA','biblioteca'),('SIN FECHA','sin-fecha-mes'),('AÑO','selector-anio')]); return
    if k=='extras_stickers':
        header(d,'EXTRAS · STICKERS DIGITALES','RECURSOS PNG INDEPENDIENTES')
        panel(d,'1600+ STICKERS PNG',24,205,240,120); panel(d,'CATEGORÍAS ORGANIZADAS',276,205,240,120); panel(d,'FONDOS TRANSPARENTES',24,355,240,120); panel(d,'PALETAS COORDINADAS',276,355,240,120); panel(d,'STICKER BOOK INCLUIDO',24,505,492,120)
        d.paragraph('Los stickers se entregan en carpetas por categoría y pueden insertarse como imágenes desde tu aplicación de anotación. El Master no incrusta los PNG para conservar un tamaño razonable.',24,670,480,15,23)
        footer(d,[('INICIO','inicio'),('EXTRAS','extras-cuadernos'),('BIBLIOTECA','biblioteca'),('AÑO','selector-anio')]); return
    if k=='hub':
        header(d,MODULES[cat][0],'ÍNDICE DE PLANTILLAS')
        lib_nav(d,'PORTADA',f'hub-{cat}',24,195,156,70); lib_nav(d,'ÍNDICE',f'indice-{cat}',192,195,156,70)
        names=MODULES[cat][1]
        for i,n in enumerate(names[:6]): lib_nav(d,n,tid(cat,n),24+(i%2)*252,300+(i//2)*92,240,70)
        d.text(f'{len(names)} plantillas organizadas para explorar desde el índice.',24,800,14,'Body'); lib_footer(d,cat,f'indice-{cat}'); return
    if k=='index':
        header(d,p['title'],'TOCA UNA TARJETA PARA ABRIR')
        names=MODULES[cat][1]; chunk=p.get('chunk',0); start=chunk*16; occurrences={}
        for prior in names[:start]:
            base=tid(cat,prior); occurrences[base]=occurrences.get(base,0)+1
        for i,n in enumerate(names[start:start+16]):
            base=tid(cat,n); occurrences[base]=occurrences.get(base,0)+1; target=base if occurrences[base]==1 else f'{base}-{occurrences[base]}'
            lib_nav(d,f'{start+i+1:02d} · {n}',target,24+(i%2)*252,195+(i//2)*82,240,70)
        nxt=f'indice-{cat}-{chunk+2}' if start+16<len(names) else f'hub-{cat}'
        lib_footer(d,cat,p['id']); lib_nav(d,'SIGUIENTE ÍNDICE',nxt,192,820,240,70); return
    if k=='favorites':
        header(d,'MIS PLANTILLAS FAVORITAS','ACCESOS RÁPIDOS')
        fav=[('PLAN DEL DÍA','dia-2026-01-01'),('SEMANA','semana-2025-12-29'),('HÁBITOS',tid('productividad','SEGUIMIENTO DE HÁBITOS')),('PRESUPUESTO','mes-2026-01'),('COMIDAS',tid('bienestar','PLANIFICADOR DE COMIDAS')),('ENTRENAMIENTO',tid('bienestar','ENTRENAMIENTO')),('GRATITUD',tid('autocuidado','GRATITUD DIARIA')),('PROYECTOS',tid('productividad','PLANIFICADOR DE PROYECTOS')),('NOTAS','sin-fecha-dia')]
        for i,(label,target) in enumerate(fav): lib_nav(d,label,target,24+(i%2)*252,205+(i//2)*120,240,90)
        footer(d,[('INICIO','inicio'),('BIBLIOTECA','biblioteca'),('OBJETIVOS','hub-objetivos'),('VIDA','hub-vida')]); return
    if k=='duplicates':
        header(d,'PLANTILLAS','COPIAS LIMPIAS PARA DUPLICAR EN TU APP')
        dup=[('PLAN DIARIO SIN FECHA','sin-fecha-dia'),('PLAN SEMANAL SIN FECHA','sin-fecha-semana'),('PLAN MENSUAL SIN FECHA','sin-fecha-mes'),('META',tid('objetivos','META SMART')),('PROYECTO',tid('productividad','PLANIFICADOR DE PROYECTOS')),('HÁBITOS',tid('productividad','SEGUIMIENTO DE HÁBITOS')),('REUNIÓN',tid('productividad','NOTAS DE REUNIÓN')),('VIAJE',tid('vida','PLANIFICADOR DE VIAJE')),('RECETA',tid('bienestar','RECETAS')),('ENTRENAMIENTO',tid('bienestar','REGISTRO DE ENTRENAMIENTO')),('GRATITUD',tid('autocuidado','GRATITUD DIARIA')),('NOTAS','sin-fecha-dia')]
        for i,(label,target) in enumerate(dup): lib_nav(d,label,target,24+(i%2)*252,205+(i//2)*100,240,72)
        d.text('La duplicación depende de las funciones de tu aplicación de anotación.',24,820,13,'Body'); footer(d,[('INICIO','inicio'),('BIBLIOTECA','biblioteca'),('SIN FECHA','sin-fecha-mes'),('OBJETIVOS','hub-objetivos')]); return
    draw_template(d,p)

def render_phase3(path,pages):
    nav=Navigation(pages); c=canvas.Canvas(str(path),pagesize=(WIDTH,HEIGHT),pageCompression=1,pdfVersion=(1,4),invariant=1); c.setTitle("YOYI'R | Planificador Digital 2026–2028 | Español"); c.setAuthor("YOYI'R")
    byid={p['id']:p for p in pages}
    for i,p in enumerate(pages):
        c.bookmarkPage(p['id'],fit='Fit'); c.addOutlineEntry(p['title'],p['id'],0); d=Drawing(c,THEMES[p['theme']],nav,p['id']); d.box(0,0,WIDTH,HEIGHT,d.t.background,radius=0)
        if p['id']=='selector-anio':
            draw_page(d,byid,p)
            for j,cat in enumerate(MODULES): lib_nav(d,MODULES[cat][0],f'hub-{cat}',24+(j%2)*252,700+(j//2)*74,240,66)
        elif p.get('kind') in ('library_home','extras','extras_stickers','hub','index','template','favorites','duplicates'): draw_library(d,p)
        else: draw_page(d,byid,p)
        d.text(f"YOYI'R  /  {i+1:04d}",24,955,8,color=d.t.accent); c.showPage()
    nav.check(); c.save(); return nav

def build_phase3(output=None):
    started=time.time(); out=Path(output or OUTPUT); out.mkdir(parents=True,exist_ok=True); register_fonts(); pages=phase2_pages()+library_pages(); path=out/'YOYIR-Planificador-Digital-2026-2028-ES.pdf'; nav=render_phase3(path,pages)
    reader=PdfReader(path,strict=True); doc=fitz.open(path); broken=0
    for page in reader.pages:
        for ann in page.get('/Annots',[]):
            if ann.get_object().get('/Dest') is None: broken+=1
    base=1379; new=len(pages)-base; templates=sum(len(v[1]) for v in MODULES.values()); hubs=2+len(MODULES)*2+2
    report={'fase':'3','paginas_nuevas':new,'paginas_totales':len(pages),'plantillas_nuevas':templates,'indices_nuevos':hubs,'hipervinculos_nuevos':len(nav.links)-11847,'hipervinculos_totales':len(nav.links),'enlaces_rotos':broken,'tamano_bytes':path.stat().st_size,'tiempo_generacion_segundos':round(time.time()-started,2)}
    (out/'fase3-validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8'); doc.close(); write_inventory(templates)
    report_path=DOCS/'BUILD-REPORT.md'; old=report_path.read_text(encoding='utf-8'); marker='\n\n## FASE 3 — Biblioteca premium de plantillas'; old=old.split(marker,1)[0] if marker in old else old; report_path.write_text(old+marker+'\n\n'+json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8'); return report

def write_inventory(total):
    lines=['# Inventario de plantillas YOYI\'R','','Biblioteca activa en español. La edición inglesa permanece reservada.','']
    for cat,(title,names) in MODULES.items():
        lines += [f'## {title}','']+[f'- {i:02d}. {n}' for i,n in enumerate(names,1)]+['']
    lines += ['## Plantillas reutilizables','', '- Plan diario sin fecha','- Plan semanal sin fecha','- Plan mensual sin fecha','- Meta','- Proyecto','- Hábitos','- Reunión','- Viaje','- Receta','- Entrenamiento','- Gratitud','- Notas','']
    (DOCS/'TEMPLATE-INVENTORY.md').write_text('\n'.join(lines),encoding='utf-8')

if __name__=='__main__': print(json.dumps(build_phase3(),ensure_ascii=False,indent=2))
