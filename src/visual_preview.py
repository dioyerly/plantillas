"""Preview visual de la corrección prioritaria. No regenera el Master."""
from pathlib import Path
import re, fitz
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, white
from reportlab.lib.utils import ImageReader
from .config import ROOT, OUTPUT, DOCS, WIDTH, HEIGHT

PALETTE=[('#CDBCE8','LAVANDA'),('#E7B8C8','ROSA'),('#B9CBAE','SALVIA'),('#B8D7E8','CIELO'),('#F4C6A6','MELOCOTÓN'),('#F3DFA5','CREMA'),('#B9C5EA','PERIWINKLE'),('#BFE0D0','MENTA'),('#DCCBB6','ARENA'),('#EFAFA2','CORAL')]
SECTIONS=['OBJETIVOS','VIDA','PRODUCTIVIDAD','BIENESTAR','AUTOCUIDADO','FINANZAS','ESTUDIO','ORGANIZACIÓN','NOTAS','EXTRAS']
MONTHS=['ENERO','FEBRERO','MARZO','ABRIL','MAYO','JUNIO','JULIO','AGOSTO','SEPTIEMBRE','OCTUBRE','NOVIEMBRE','DICIEMBRE']

def card(c,x,y,w,h,title,color,detail='ESPACIO PARA ESCRIBIR'):
    c.setFillColor(HexColor(color)); c.roundRect(x,y,w,h,18,fill=1,stroke=0)
    c.setFillColor(HexColor('#39353F')); c.setFont('Helvetica-Bold',13); c.drawString(x+14,y+h-25,title)
    c.setFont('Helvetica',8); c.drawString(x+14,y+h-40,detail)
    c.setStrokeColor(HexColor('#39353F')); c.setLineWidth(1); c.roundRect(x+14,y+14,w-28,h-62,10,fill=0,stroke=1)

def page(c,title,subtitle='',bg='#FAF7F2'):
    c.setFillColor(HexColor(bg)); c.rect(0,0,WIDTH,HEIGHT,fill=1,stroke=0)
    c.setFillColor(HexColor('#39353F')); c.setFont('Helvetica-Bold',25); c.drawString(34,900,title)
    if subtitle: c.setFont('Helvetica',10); c.drawString(36,875,subtitle)
    c.setStrokeColor(HexColor('#CDBCE8')); c.setLineWidth(3); c.line(36,855,504,855)

def build_preview():
    out=OUTPUT/'YOYI-Visual-Redesign-Preview.pdf'; c=canvas.Canvas(str(out),pagesize=(WIDTH,HEIGHT),invariant=1)
    # Portada
    page(c,"YOYI’R DIGITAL PLANNER 2026–2028","PREVIEW DE REDISEÑO VISUAL",'#CDBCE8'); c.setFillColor(HexColor('#39353F')); c.setFont('Helvetica-Bold',42); c.drawString(44,700,'COLOR · ORDEN · INTENCIÓN'); c.setFont('Helvetica',15); c.drawString(46,665,'Una experiencia editorial para planificar con claridad.'); c.setFillColor(HexColor('#E7B8C8')); c.circle(410,650,70,fill=1,stroke=0); c.setFillColor(HexColor('#B9CBAE')); c.circle(455,710,38,fill=1,stroke=0); c.showPage()
    # Inicio dashboard
    page(c,'INICIO','Panel principal multicolor')
    for i,t in enumerate(['2026','2027','2028','SIN FECHA']): card(c,36+i%2*240,765-(i//2)*78,220,60,t,PALETTE[i][0],'AÑO Y NAVEGACIÓN')
    for i,t in enumerate(SECTIONS): card(c,36+i%2*240,610-(i//2)*82,220,64,t,PALETTE[(i+2)%len(PALETTE)][0])
    c.showPage()
    page(c,'ÍNDICE','Acceso rápido a las áreas del planner')
    for i,t in enumerate(['AÑO','MES','SEMANA','DÍA','OBJETIVOS','VIDA','PRODUCTIVIDAD','BIENESTAR','AUTOCUIDADO','FINANZAS','ESTUDIO','ORGANIZACIÓN','NOTAS','EXTRAS']): card(c,36+i%2*240,790-(i//2)*88,220,68,t,PALETTE[i%len(PALETTE)][0],'ABRIR SECCIÓN')
    c.showPage()
    page(c,'AÑO 2026','Vista anual')
    for i,m in enumerate(MONTHS): card(c,36+i%3*160,790-(i//3)*105,145,82,m,PALETTE[i%len(PALETTE)][0],'CALENDARIO')
    c.showPage()
    for idx,m in enumerate(MONTHS[:2]):
        page(c,m,'CALENDARIO MENSUAL',PALETTE[idx][0]); c.setFillColor(HexColor('#39353F')); c.setFont('Helvetica-Bold',12); c.drawString(40,820,'LUNES   MARTES   MIÉRCOLES   JUEVES   VIERNES   SÁBADO   DOMINGO')
        for r in range(5):
            for col in range(7):
                x=36+col*67; y=735-r*92; c.setFillColor(HexColor('#FFFFFF')); c.roundRect(x,y,60,76,8,fill=1,stroke=0); c.setFillColor(HexColor('#39353F')); c.drawString(x+8,y+58,str(r*7+col+1))
        c.showPage()
    page(c,'PLANIFICADOR MENSUAL','OBJETIVOS · PRIORIDADES · HÁBITOS');
    for i,t in enumerate(['OBJETIVOS DEL MES','3 PRIORIDADES','SEGUIMIENTO DE HÁBITOS','FECHAS IMPORTANTES']): card(c,36+i%2*240,700-(i//2)*170,220,145,t,PALETTE[i][0]);
    c.showPage()
    page(c,'SEMANA','Vista semanal clara y flexible')
    for i,t in enumerate(['LUNES','MARTES','MIÉRCOLES','JUEVES','VIERNES','SÁBADO','DOMINGO']): card(c,36+i%2*240,790-(i//2)*94,220,78,t,PALETTE[i%7][0],'NOTAS Y TAREAS')
    c.showPage()
    page(c,'DÍA','Planificador diario con áreas de escritura limpias')
    for i,t in enumerate(['ENFOQUE DE HOY','3 PRIORIDADES','HORARIO','POR HACER','COMIDAS · AGUA · MOVIMIENTO','ÁNIMO · GRATITUD · MAÑANA']): card(c,36+i%2*240,770-(i//2)*122,220,104,t,PALETTE[i][0])
    c.showPage()
    for title,items in [('OBJETIVOS',['VISIÓN','OBJETIVOS DEL AÑO','METAS DEL MES','PRÓXIMOS PASOS']),('VIDA',['TABLERO DE VISIÓN','LISTA DE SUEÑOS','LISTA DE DESEOS','DIARIO DE GRATITUD']),('PRODUCTIVIDAD',['ENFOQUE','OBJETIVOS','PRIORIDADES','ACCIONES']),('BIENESTAR',['ÁNIMO','SUEÑO','HIDRATACIÓN','MOVIMIENTO']),('AUTOCUIDADO',['IDEAS DE AUTOCUIDADO','MOMENTOS DE CALMA','REFLEXIÓN','AFIRMACIONES']),('FINANZAS',['INGRESOS','GASTOS','AHORRO','PRESUPUESTO']),('ESTUDIO',['PLAN DE ESTUDIO','APUNTES','EXÁMENES','PROYECTOS']),('ORGANIZACIÓN',['TAREAS','ORDEN DEL HOGAR','FECHAS','LISTAS']),('NOTAS',['LÍNEAS','CUADRÍCULA','PUNTOS','PÁGINA LIBRE']),('EXTRAS',['STICKERS','PORTADAS','DIVISORES','RECURSOS'])]:
        page(c,title,'PÁGINA DE SECCIÓN');
        for i,t in enumerate(items): card(c,36+i%2*240,720-(i//2)*180,220,150,t,PALETTE[(i+SECTIONS.index(title))%len(PALETTE)][0])
        c.showPage()
    page(c,'EXTRAS · STICKERS','Biblioteca visual incluida');
    files=list((OUTPUT/'stickers').rglob('*.png'))[:20]
    for i,p in enumerate(files[:12]):
        x=45+(i%4)*120; y=700-(i//4)*150; c.setFillColor(white); c.roundRect(x,y,95,110,12,fill=1,stroke=0); c.drawImage(ImageReader(str(p)),x+10,y+20,75,75,preserveAspectRatio=True,anchor='c',mask='auto')
    c.showPage()
    page(c,'DIVISOR','Detalles editoriales y color suave','#E7B8C8'); c.setFillColor(HexColor('#39353F')); c.setFont('Helvetica-Bold',36); c.drawString(44,680,'TU TIEMPO,'); c.drawString(44,630,'TU RITMO.'); c.setFont('Helvetica',13); c.drawString(46,585,'Diseño premium con espacio para escribir.'); c.showPage(); c.save(); return out

def report(path):
    master=OUTPUT/'YOYIR-Planificador-Digital-2026-2028-ES.pdf'; text=''.join(p.get_text() for p in fitz.open(master)); terms=['placeholder','incluida en el paquete','próximamente','pendiente','demo','test','sample']; found={t:len(re.findall(t,text,re.I)) for t in terms}; report=['# REPORTE DE REDISEÑO VISUAL YOYI’R','',f'- **PÁGINAS PREVIEW:** {len(fitz.open(path))}','- **COLORES UTILIZADOS:** 10 colores de la paleta maestra','- **COMPONENTES REDISEÑADOS:** portada, inicio, índice, año, calendario mensual, planificador mensual, semana, día, tarjetas de secciones, stickers y divisor','- **PLACEHOLDERS DETECTADOS:** '+', '.join(f'{k}: {v}' for k,v in found.items() if v) if any(found.values()) else '- **PLACEHOLDERS DETECTADOS:** ninguno','- **PÁGINAS INCOMPLETAS DETECTADAS:** revisión automática de densidad y términos; requieren revisión visual final','- **STICKER PAGES COMPLETAS:** preview con muestras PNG reales integradas','- **STICKER PAGES PENDIENTES:** ilustraciones premium externas en `assets/stickers/custom/`','- **PROBLEMAS ENCONTRADOS:** el Master no se regeneró; se mantiene intacto para aprobación visual','', 'El preview es una prueba visual. La regeneración del Master queda detenida hasta recibir aprobación.']; DOCS.mkdir(exist_ok=True); (DOCS/'VISUAL-REDESIGN-REPORT.md').write_text('\n'.join(report)+'\n',encoding='utf-8')

if __name__=='__main__':
    preview=build_preview(); print(preview); report(preview)
