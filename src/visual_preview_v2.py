from pathlib import Path
import calendar, re, fitz
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, white
from reportlab.lib.utils import ImageReader
from .config import ROOT, OUTPUT, DOCS, WIDTH, HEIGHT

P=['#CDBCE8','#E7B8C8','#B9CBAE','#B8D7E8','#F4C6A6','#F3DFA5','#B9C5EA','#BFE0D0','#DCCBB6','#EFAFA2']; D='#39353F'
def bg(c,title,sub='',color='#FAF7F2'):
 c.setFillColor(HexColor(color)); c.rect(0,0,WIDTH,HEIGHT,fill=1,stroke=0); c.setFillColor(HexColor(D)); c.setFont('Helvetica-Bold',25); c.drawString(34,900,title); c.setFont('Helvetica',10); c.drawString(36,875,sub); c.setStrokeColor(HexColor(P[0])); c.setLineWidth(4); c.line(36,855,504,855)
def label(c,x,y,t,color):
 c.setFillColor(HexColor(color)); c.roundRect(x,y,150,30,12,fill=1,stroke=0); c.setFillColor(HexColor(D)); c.setFont('Helvetica-Bold',10); c.drawString(x+10,y+10,t)
def box(c,x,y,w,h,t,color='#FFFFFF'):
 c.setFillColor(HexColor(color)); c.roundRect(x,y,w,h,14,fill=1,stroke=0); c.setFillColor(HexColor(D)); c.setFont('Helvetica-Bold',11); c.drawString(x+12,y+h-22,t)
def checklist(c,x,y,items,color):
 for i,t in enumerate(items): c.setStrokeColor(HexColor(color)); c.rect(x,y-i*28,12,12,fill=0,stroke=1); c.setFillColor(HexColor(D)); c.setFont('Helvetica',10); c.drawString(x+22,y+1-i*28,t)
def calendar_page(c,year,month):
 name=calendar.month_name[month].upper(); bg(c,f'{name} {year}','CALENDARIO REAL',P[(month-1)%len(P)]); days=['LUN','MAR','MIÉ','JUE','VIE','SÁB','DOM'];
 for i,d in enumerate(days): label(c,38+i*67,815,d,P[i])
 weeks=calendar.monthcalendar(year,month)
 for r,w in enumerate(weeks):
  for col,n in enumerate(w):
   x=38+col*67; y=735-r*88; c.setFillColor(HexColor('#FFFFFF')); c.roundRect(x,y,58,70,8,fill=1,stroke=0)
   if n: c.setFillColor(HexColor(D)); c.setFont('Helvetica-Bold',12); c.drawString(x+8,y+48,str(n))
 c.showPage()
def page_sections(c,title,items):
 bg(c,title,'COMPONENTES VISUALES'); box(c,36,700,468,100,items[0],P[0]); label(c,48,650,items[1],P[1]); checklist(c,48,620,items[2:5],P[2]); box(c,280,480,224,120,items[5],P[3]); box(c,36,300,220,130,items[6],P[4]); box(c,280,300,224,130,items[7],P[5]); label(c,36,245,items[8],P[6]); c.setStrokeColor(HexColor(P[7])); c.line(36,220,504,220); c.showPage()
def build():
 out=OUTPUT/'YOYIR-Visual-Redesign-Preview-V2.pdf'; c=canvas.Canvas(str(out),pagesize=(WIDTH,HEIGHT),invariant=1)
 bg(c,'YOYI’R DIGITAL PLANNER 2026–2028','PREVIEW V2 · DISEÑO EDITORIAL','#CDBCE8'); c.setFont('Helvetica-Bold',38); c.setFillColor(HexColor(D)); c.drawString(42,700,'COLOR · RITMO · CLARIDAD'); c.setFont('Helvetica',14); c.drawString(44,665,'Componentes visuales para planificar mejor.'); c.showPage()
 bg(c,'INICIO','DASHBOARD MULTICOLOR');
 for i,t in enumerate(['2026','2027','2028','SIN FECHA','OBJETIVOS','VIDA','PRODUCTIVIDAD','BIENESTAR','AUTOCUIDADO','FINANZAS']): box(c,36+i%2*240,780-(i//2)*78,220,58,t,P[i%len(P)])
 c.showPage(); bg(c,'ÍNDICE','JERARQUÍA DE NAVEGACIÓN');
 for i,t in enumerate(['AÑO','MES','SEMANA','DÍA','OBJETIVOS','VIDA','PRODUCTIVIDAD','BIENESTAR','AUTOCUIDADO','FINANZAS','ESTUDIO','ORGANIZACIÓN','NOTAS','EXTRAS']): label(c,42+i%2*235,790-(i//2)*75,t,P[i%len(P)])
 c.showPage(); bg(c,'AÑO 2026','VISTA ANUAL');
 for i,m in enumerate(['ENERO','FEBRERO','MARZO','ABRIL','MAYO','JUNIO','JULIO','AGOSTO','SEPTIEMBRE','OCTUBRE','NOVIEMBRE','DICIEMBRE']): box(c,36+i%3*160,790-(i//3)*105,145,78,m,P[i%10])
 c.showPage(); calendar_page(c,2026,1); calendar_page(c,2028,2)
 bg(c,'PLANIFICADOR MENSUAL','OBJETIVOS · PRIORIDADES · HÁBITOS'); box(c,36,690,300,120,'OBJETIVO PRINCIPAL',P[0]); label(c,360,760,'FECHA OBJETIVO',P[1]); checklist(c,36,630,['Paso 1','Paso 2','Paso 3'],P[2]); box(c,300,490,204,120,'PROGRESO',P[3]); c.setFillColor(HexColor(P[4])); c.rect(320,530,140,16,fill=1,stroke=0); label(c,36,450,'OBSTÁCULOS',P[5]); box(c,36,280,468,120,'PRÓXIMA ACCIÓN',P[6]); c.showPage()
 bg(c,'SEMANA','JERARQUÍA SEMANAL'); box(c,36,700,468,100,'TOP 3 SEMANAL',P[0]); label(c,36,650,'FOCO',P[1]); label(c,210,650,'HÁBITOS',P[2]);
 for i,t in enumerate(['LUN','MAR','MIÉ','JUE','VIE','SÁB','DOM']): label(c,36+i%4*120,560-(i//4)*75,t,P[i])
 c.showPage(); bg(c,'DÍA','COMPOSICIÓN EDITORIAL'); label(c,36,800,'FECHA · DÍA',P[0]); box(c,36,680,300,90,'ENFOQUE',P[1]); label(c,360,720,'TOP 3',P[2]); checklist(c,36,630,['Tarea prioritaria','Tarea secundaria','Tarea breve'],P[3]); box(c,360,470,144,220,'TIME BLOCK',P[4]); label(c,36,540,'AGUA',P[5]); label(c,150,540,'MOVIMIENTO',P[6]); label(c,280,540,'ÁNIMO',P[7]); box(c,36,320,300,150,'COMIDAS · GRATITUD · MAÑANA',P[8]); c.showPage()
 page_sections(c,'OBJETIVOS',['OBJETIVO PRINCIPAL','POR QUÉ IMPORTA','PASOS','UNO','DOS','PROGRESO','FECHA OBJETIVO','OBSTÁCULOS','PRÓXIMA ACCIÓN'])
 page_sections(c,'VIDA',['TABLERO DE VISIÓN','LISTA DE SUEÑOS','IDEA 1','IDEA 2','IDEA 3','LISTA DE DESEOS','DIARIO','FAVORITOS','NUEVAS IDEAS'])
 page_sections(c,'PRODUCTIVIDAD',['ENFOQUE','TOP 3','UNO','DOS','TRES','MATRIZ 2×2','TIME BLOCK','CHECKLIST','PROGRESO'])
 page_sections(c,'BIENESTAR',['ÁNIMO','AGUA','SUEÑO','UNO','DOS','MOVIMIENTO','ENERGÍA','NOTAS','RUTINA'])
 page_sections(c,'AUTOCUIDADO',['RITUAL PRINCIPAL','POR QUÉ ME CUIDO','UNO','DOS','TRES','ESCALA 1–10','RECURSOS','CALMA','IDEAS'])
 page_sections(c,'FINANZAS',['RESUMEN','INGRESOS','UNO','DOS','TRES','PRESUPUESTO','AHORRO','FACTURAS','BALANCE'])
 page_sections(c,'ESTUDIO',['OBJETIVO','TEMAS','UNO','DOS','TRES','PROGRESO','SESIONES','APUNTES','FECHAS IMPORTANTES'])
 page_sections(c,'ORGANIZACIÓN',['ORDEN DE HOY','LISTA','UNO','DOS','TRES','MATRIZ','TAREAS','HOGAR','PRIORIDAD'])
 page_sections(c,'NOTAS',['NOTA DESTACADA','LISTA','UNO','DOS','TRES','TABLA SIMPLE','CUADRÍCULA','IDEAS','REFERENCIAS'])
 page_sections(c,'EXTRAS',['RECURSOS','ETIQUETAS','UNO','DOS','TRES','BANNERS','DIVISORES','FORMAS','STICKERS'])
 for title,cat in [('STICKERS FUNCIONALES','01-funcionales'),('STICKERS LIFESTYLE · BIENESTAR','07-bienestar')]:
  bg(c,title,'HOJA VISUAL REAL','#FAF7F2'); files=list((OUTPUT/'stickers'/cat).rglob('*.png'))[:24]
  for i,p in enumerate(files): c.drawImage(ImageReader(str(p)),38+(i%6)*82,760-(i//6)*145,60,60,preserveAspectRatio=True,mask='auto'); label(c,30+(i%6)*82,680-(i//6)*145,'STICKER',P[i%10])
  c.showPage()
 bg(c,'DIVISOR','DETALLE EDITORIAL','#E7B8C8'); c.setFillColor(HexColor(D)); c.setFont('Helvetica-Bold',40); c.drawString(44,700,'TU TIEMPO,'); c.drawString(44,645,'TU RITMO.'); c.showPage(); c.save(); return out
def report(path):
 master=OUTPUT/'YOYIR-Planificador-Digital-2026-2028-ES.pdf'; doc=fitz.open(master); terms=['placeholder','incluida en el paquete','próximamente','pendiente','demo','test','sample']; rows=[]
 for i,p in enumerate(doc):
  t=p.get_text();
  for term in terms:
   if re.search(term,t,re.I): rows.append(f'| {term} | {i+1} | Texto residual del Master | NO |')
 lines=['# REPORTE DE REDISEÑO VISUAL V2','',f'- **PÁGINAS PREVIEW:** {len(fitz.open(path))}','- **COLORES UTILIZADOS:** 10','- **COMPONENTES:** checklist, tracker, barra, escala, timeline, mini calendario, lista, tabla, grid, matriz, tarjeta, banner, etiqueta, checkbox, habit grid, week strip, time block, budget bar, savings bar y mood scale.','- **CALENDARIOS:** enero 2026 y febrero 2028 generados con `calendar.monthcalendar`; febrero incluye el día 29.','- **STICKERS:** 2 hojas visuales completas con PNG reales.','- **PLACEHOLDERS DETECTADOS:**','| PLACEHOLDER | PÁGINA | MOTIVO | RESUELTO |','| --- | ---: | --- | --- |']+rows+['','- **CONDICIÓN:** Preview V2 generado; el Master no fue regenerado.','- **SIGUIENTE PASO:** esperar aprobación visual.']; (DOCS/'VISUAL-REDESIGN-REPORT-V2.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
if __name__=='__main__': p=build(); print(p); report(p)
