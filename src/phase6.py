"""Fase 6: biblioteca premium de stickers PNG transparentes y Sticker Book."""
import csv, hashlib, json, re, time, unicodedata
from pathlib import Path
from collections import defaultdict
from PIL import Image, ImageDraw, ImageFont
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.lib.utils import ImageReader
from pypdf import PdfReader
import fitz
from .config import ROOT, OUTPUT, DOCS, WIDTH, HEIGHT
from .components import Drawing, register_fonts
from .navigation import Navigation
from .themes import THEMES
from .phase3 import build_phase3

CATEGORIES=[
('01-funcionales','FUNCIONALES','checkbox vacío|checkbox marcado|círculo vacío|círculo marcado|estrella|corazón|bandera|pin|marcador|flecha arriba|flecha abajo|flecha izquierda|flecha derecha|separador|línea|subrayado|resaltador|pestaña|clip|marcador de página|nota adhesiva|etiqueta|banner|cinta'),
('02-fechas','FECHAS','ENERO|FEBRERO|MARZO|ABRIL|MAYO|JUNIO|JULIO|AGOSTO|SEPTIEMBRE|OCTUBRE|NOVIEMBRE|DICIEMBRE|LUNES|MARTES|MIÉRCOLES|JUEVES|VIERNES|SÁBADO|DOMINGO|LUN|MAR|MIÉ|JUE|VIE|SÁB|DOM|HOY|MAÑANA|AYER|ESTA SEMANA|PRÓXIMA SEMANA|ESTE MES|PRÓXIMO MES'),
('03-palabras','PALABRAS','IMPORTANTE|URGENTE|PRIORIDAD|PENDIENTE|HECHO|EN PROCESO|CANCELADO|REPROGRAMADO|RECORDAR|NO OLVIDAR|CITA|REUNIÓN|FECHA LÍMITE|EVENTO|DESCANSO|ENFOQUE|META|OBJETIVO|NOTAS|IDEA|PLAN'),
('04-productividad','PRODUCTIVIDAD','POR HACER|PRIORIDADES|ENFOQUE|TRABAJO|PROYECTO|REUNIÓN|LLAMADA|CORREO|PLANIFICAR|REVISAR|ENTREGAR|CREAR|INVESTIGAR|ESTUDIAR|ORGANIZAR|ARCHIVAR|TERMINADO|DESCANSO|PAUSA|CRONÓMETRO|CALENDARIO|CHECKLIST'),
('05-finanzas','FINANZAS','PAGO|PAGADO|FACTURA|VENCIMIENTO|INGRESO|GASTO|AHORRO|PRESUPUESTO|DEUDA|SUSCRIPCIÓN|FONDO|INVERSIÓN|COMPRA|REEMBOLSO|TRANSFERENCIA|DEPÓSITO|META DE AHORRO|DÍA SIN GASTOS|cartera|monedas|alcancía|calculadora|gráfico|tarjeta|recibo|sobre|caja de ahorro'),
('06-estudio','ESTUDIO','ESTUDIAR|EXAMEN|TAREA|PROYECTO|CLASE|CURSO|LECTURA|REPASAR|PRACTICAR|ENTREGAR|RESUMEN|NOTAS|INVESTIGAR|BIBLIOTECA|CERTIFICADO|libro|cuaderno|lápiz|regla|calculadora|bombilla|birrete|documento|check|reloj'),
('07-bienestar','BIENESTAR','BIENESTAR|DESCANSO|DORMIR|AGUA|MOVIMIENTO|CAMINAR|AIRE LIBRE|RUTINA|ENERGÍA|COMIDAS|TIEMPO PARA MÍ'),
('08-autocuidado','AUTOCUIDADO','HOY ME ELIJO|PAUSA|RESPIRA|DESCANSA|TIEMPO PARA MÍ|GRATITUD|REFLEXIÓN|PEQUEÑA VICTORIA|UN PASO A LA VEZ|CUIDARME TAMBIÉN CUENTA|HOY SOLO LO POSIBLE'),
('09-fitness','MOVIMIENTO','ENTRENAMIENTO|FUERZA|CARDIO|CAMINAR|CORRER|MOVILIDAD|ESTIRAMIENTO|PILATES|DESCANSO|DÍA ACTIVO|mancuerna|zapatilla|cronómetro|esterilla|botella|corazón'),
('10-comida','COMIDA','DESAYUNO|ALMUERZO|CENA|COLACIÓN|PREPARAR COMIDAS|RECETA|SUPERMERCADO|COCINAR|AGUA|CAFÉ|TÉ|FRUTA|VERDURAS'),
('11-hogar','HOGAR','LIMPIAR|LAVAR|ROPA|COCINA|BAÑO|DORMITORIO|COMPRAS|ORDENAR|DEPURAR|MANTENIMIENTO|HOGAR|PLANTAS|BASURA|RECICLAJE'),
('12-viajes','VIAJES','VIAJE|VUELO|HOTEL|RESERVA|EQUIPAJE|DOCUMENTOS|ITINERARIO|EXCURSIÓN|TRANSPORTE|RESTAURANTE|PLAYA|MONTAÑA|CIUDAD|FOTOS|avión|maleta|mapa|pin|cámara|pasaporte|auto|tren|barco'),
('13-lectura','LECTURA','LEYENDO|POR LEER|TERMINADO|5 ESTRELLAS|RESEÑA|FAVORITO|LIBRERÍA|BIBLIOTECA|NUEVO LIBRO|AUDIOLIBRO|libro abierto|libro cerrado|estantería|marcapáginas|estrella|auriculares'),
('14-trabajo','TRABAJO','TRABAJO|OFICINA|REUNIÓN|CLIENTE|PROYECTO|FECHA LÍMITE|CORREO|LLAMADA|PRESENTACIÓN|ENTREGA|SEGUIMIENTO|IDEA|FOCO'),
('15-compras','COMPRAS','COMPRAR|SUPERMERCADO|PEDIDO|ENTREGADO|EN CAMINO|LISTA DE DESEOS|REGALO|DEVOLUCIÓN|REPOSICIÓN'),
('16-eventos','EVENTOS','CUMPLEAÑOS|ANIVERSARIO|FIESTA|CELEBRACIÓN|CENA|SALIDA|CITA|EVENTO|REGALO|INVITACIÓN'),
('17-clima','CLIMA','SOL|NUBLADO|LLUVIA|TORMENTA|NIEVE|VIENTO|CALOR|FRÍO|PARCIALMENTE NUBLADO'),
('18-estado-animo','ESTADO DE ÁNIMO','EXCELENTE|BIEN|TRANQUILO/A|NEUTRAL|CANSADO/A|ESTRESADO/A|TRISTE|ENOJADO/A|MOTIVADO/A|CON POCA ENERGÍA|1|2|3|4|5'),
('19-formas','FORMAS','círculo|cuadrado|rectángulo|rectángulo redondeado|óvalo|estrella|corazón|hexágono|arco|onda|línea|flecha|burbuja|marco'),
('20-decorativos','DECORATIVOS','constelación|sol|luna|estrellas|saturno|arcos|ondas|forma abstracta|línea orgánica|rama botánica|destello|puntos|patrón suave'),
('21-numeros','NÚMEROS','0|1|2|3|4|5|6|7|8|9|2026|2027|2028'),
('22-iconos','ICONOS','objetivo|casa|avión|libro|corazón|estrella|reloj|check|dinero|nota|bienestar'),
('23-etiquetas','ETIQUETAS','etiqueta pequeña|etiqueta mediana|etiqueta grande|etiqueta horizontal|etiqueta vertical|etiqueta redondeada|etiqueta recta|etiqueta contorno|etiqueta rellena'),
('24-checklists','CHECKLISTS','1 tarea|3 tareas|5 tareas|7 tareas|10 tareas|checkbox|círculo|estrella|minimal'),
('25-especiales','ESPECIALES','UN PASO A LA VEZ|HOY CUENTA|SIGUE|RESPIRA|PUEDO EMPEZAR DE NUEVO|MENOS, PERO MEJOR|HAZ ESPACIO|ENFOQUE|CONFÍA EN EL PROCESO|PEQUEÑAS VICTORIAS|HOY SOLO LO POSIBLE|label vacío|banner vacío|nota adhesiva vacía|pestaña vacía|bandera vacía|cinta vacía|caja vacía|burbuja vacía|marco vacío')]
PALETTE_KEYS=['lavender','blush','sage','sky','sand','neutral','multicolor']
PALETTE={'lavender':'#796487','blush':'#956773','sage':'#627A64','sky':'#607B96','sand':'#88724F','neutral':'#77716A','multicolor':'#B47C9B'}
FONT_PATH='C:/Windows/Fonts/calibri.ttf'

def slug(s): return ''.join(c for c in unicodedata.normalize('NFKD',s.lower()) if not unicodedata.combining(c)).replace(' ','-').replace('/','-').replace('?','').replace('¿','')
def font(size):
    try: return ImageFont.truetype(FONT_PATH,size)
    except OSError: return ImageFont.load_default()
def draw_sticker(label,theme,style,index):
    im=Image.new('RGBA',(900,450),(0,0,0,0)); dr=ImageDraw.Draw(im); color=PALETTE[theme] if theme!='multicolor' else ['#B47C9B','#6E96A8','#8AA878','#C69A6C'][index%4]; soft=(int(color[1:3],16),int(color[3:5],16),int(color[5:7],16),42)
    if style==0: dr.rounded_rectangle((35,75,865,375),radius=55,fill=soft,outline=color,width=5)
    elif style==1: dr.ellipse((80,55,820,395),fill=soft,outline=color,width=5)
    else: dr.polygon([(40,100),(120,60),(780,60),(860,100),(820,350),(80,350)],fill=soft,outline=color)
    # Marca editorial mínima: diferencia categorías y evita duplicados binarios
    # cuando una palabra aparece en más de una colección.
    marker_x=55+(index%70)*11; marker_y=412-(index//70%3)*7
    dr.line((marker_x,marker_y,marker_x+7,marker_y),fill=color,width=3)
    if label:
        size=54 if len(label)<14 else 38 if len(label)<23 else 28
        f=font(size); bb=dr.textbbox((0,0),label,font=f); dr.text(((900-(bb[2]-bb[0]))/2,225-(bb[3]-bb[1])/2),label,font=f,fill=color)
    else:
        dr.line((180,225,720,225),fill=color,width=5)
    return im

def generate_pngs(root):
    rows=[]; hashes={}; duplicate=[]; base_count=0
    for ci,(folder,category,raw) in enumerate(CATEGORIES):
        labels=raw.split('|'); out=root/folder; out.mkdir(parents=True,exist_ok=True)
        for idx,label in enumerate(labels):
            for style in range(3):
                base_count+=1
                for theme in PALETTE_KEYS:
                    im=draw_sticker(label.upper(),theme,style,idx+ci*100); filename=f'{folder.split("-",1)[0]}-{slug(label)}-{theme}-{style+1:02d}.png'; path=out/filename; im.save(path,optimize=True)
                    digest=hashlib.sha256(path.read_bytes()).hexdigest()
                    if digest in hashes: duplicate.append((str(path),hashes[digest]))
                    hashes[digest]=str(path); rows.append({'id':f'{folder}-{idx+1:03d}-{theme}-{style+1:02d}','archivo':str(path.relative_to(ROOT)),'categoria':category,'subcategoria':'texto' if label else 'sin texto','tema':theme,'texto':label,'dimensiones':f'{im.width}x{im.height}','transparencia':'RGBA','original_base':f'{folder}-{idx+1:03d}-estilo-{style+1:02d}','variante':theme})
    return rows,duplicate,base_count

def previews(rows,root):
    out=root/'sticker-previews'; out.mkdir(parents=True,exist_ok=True)
    for folder,category,_ in CATEGORIES:
        files=[Path(ROOT/r['archivo']) for r in rows if r['archivo'].startswith(f'output/stickers/{folder}/')][:36]; sheet=Image.new('RGBA',(900,900),(248,247,244,255));
        for i,p in enumerate(files):
            im=Image.open(p).convert('RGBA'); im.thumbnail((270,125)); sheet.alpha_composite(im,((i%3)*300+15,(i//3)*145+10))
        sheet.convert('RGB').save(out/f'{folder}-preview.png')
    return out

def sticker_book(path,rows):
    pages=[{'id':'portada','title':'LIBRO DE STICKERS','kind':'cover'} ,{'id':'como-usar','title':'CÓMO USAR TUS STICKERS','kind':'howto'},{'id':'indice','title':'ÍNDICE','kind':'index'}]
    for folder,category,_ in CATEGORIES: pages.append({'id':f'categoria-{folder}','title':category,'kind':'category','folder':folder,'category':category})
    nav=Navigation(pages); c=canvas.Canvas(str(path),pagesize=(WIDTH,HEIGHT),pageCompression=1,pdfVersion=(1,4),invariant=1); c.setTitle("YOYI'R | Libro de Stickers | Español")
    by={p['id']:p for p in pages}
    def book_header(d,title,kicker=''):
        d.button('PORTADA','portada',24,24,156,66); d.button('ÍNDICE','indice',192,24,156,66); d.button('CÓMO USAR','como-usar',360,24,156,66); d.text(title,24,139,25 if len(title)<28 else 21,'Editorial');
        if kicker: d.text(kicker,24,164,11,'Bold',d.t.accent)
    for i,p in enumerate(pages):
        c.bookmarkPage(p['id'],fit='Fit'); c.addOutlineEntry(p['title'],p['id'],0); d=Drawing(c,THEMES['lavender'],nav,p['id']); d.box(0,0,WIDTH,HEIGHT,d.t.background,radius=0)
        if p['kind']=='cover': d.box(24,24,492,900,d.t.soft,radius=22); d.text("YOYI'R",270,300,54,'Editorial',center=True); d.text('LIBRO DE STICKERS',270,360,22,'Bold',center=True); d.button('ABRIR ÍNDICE','indice',92,520,356,76)
        elif p['kind']=='howto':
            book_header(d,'CÓMO USAR TUS STICKERS','PNG INDIVIDUALES CON FONDO TRANSPARENTE');
            for j,line in enumerate(['Abre la carpeta de stickers.','Elige el PNG que quieres utilizar.','Insértalo como imagen desde tu aplicación de anotación.','Cambia su tamaño y posición.','Duplica el sticker dentro de la aplicación cuando esta función esté disponible.']): d.paragraph(f'{j+1}. {line}',24,220+j*100,480,16,24)
            d.footer([('PORTADA','portada'),('ÍNDICE','indice')])
        elif p['kind']=='index':
            book_header(d,'CATEGORÍAS DE STICKERS')
            for j,(_,cat,_) in enumerate(CATEGORIES): d.button(cat,f'categoria-{CATEGORIES[j][0]}',24+(j%2)*252,200+(j//2)*70,240,66)
            d.footer([('PORTADA','portada'),('CÓMO USAR','como-usar')])
        else:
            book_header(d,p['category'],'HOJA VISUAL · PNG INCLUIDOS'); sample=[r for r in rows if r['archivo'].startswith(f'output/stickers/{p["folder"]}/')][:18]
            for j,r in enumerate(sample):
                x=24+(j%3)*168; y=205+(j//3)*100
                d.c.drawImage(ImageReader(str(ROOT/r['archivo'])),x,HEIGHT-y-78,156,78,mask='auto',preserveAspectRatio=True,anchor='c')
            d.paragraph('Los PNG individuales de esta categoría vienen incluidos en el producto. Puedes insertarlos como imágenes desde tu aplicación; copiar o reutilizar elementos desde un PDF depende de la aplicación.',24,820,480,11,16); d.footer([('ÍNDICE','indice'),('CÓMO USAR','como-usar')])
        d.text(f"YOYI'R / {i+1:02d}",24,955,8,color=d.t.accent); c.showPage()
    nav.check(); c.save(); return len(pages),len(nav.links)

def integrate_visual_master_stickers(master_path, rows):
    """Añade hojas visuales enlazadas al Master sin incrustar todos los PNG."""
    categories=[(folder,cat) for folder,cat,_ in CATEGORIES]
    tmp=master_path.with_name('_sticker-sheets.pdf')
    c=canvas.Canvas(str(tmp),pagesize=(WIDTH,HEIGHT),pageCompression=1,pdfVersion=(1,4),invariant=1)
    # Portada e índice visual.
    c.setFillColor(HexColor(THEMES['lavender'].background)); c.rect(0,0,WIDTH,HEIGHT,fill=1,stroke=0)
    c.setFillColor(HexColor(THEMES['lavender'].ink)); c.setFont('YEditorial',38); c.drawCentredString(270,650,'STICKERS DIGITALES'); c.setFont('YBold',16); c.drawCentredString(270,615,'BIBLIOTECA VISUAL INCLUIDA'); c.showPage()
    index_page=1
    c.setFillColor(HexColor(THEMES['lavender'].background)); c.rect(0,0,WIDTH,HEIGHT,fill=1,stroke=0); c.setFillColor(HexColor(THEMES['lavender'].ink)); c.setFont('YEditorial',28); c.drawString(24,820,'ÍNDICE · STICKERS'); c.setFont('YBold',12)
    for i,(_,cat) in enumerate(categories):
        x=24+(i%2)*252; y=770-(i//2)*70; c.setFillColor(HexColor('#E9E0F2')); c.roundRect(x,HEIGHT-y-56,240,56,8,fill=1,stroke=0); c.setFillColor(HexColor(THEMES['lavender'].ink)); c.drawCentredString(x+120,HEIGHT-y-34,cat)
    c.showPage()
    category_pages={}
    for folder,cat in categories:
        category_pages[folder]=len(category_pages)+2
        sample=[r for r in rows if r['archivo'].startswith(f'output/stickers/{folder}/')][:18]
        c.setFillColor(HexColor(THEMES['lavender'].background)); c.rect(0,0,WIDTH,HEIGHT,fill=1,stroke=0); c.setFillColor(HexColor(THEMES['lavender'].ink)); c.setFont('YEditorial',26); c.drawString(24,820,cat); c.setFont('YBody',10); c.drawString(24,795,'STICKERS INCLUIDOS · HOJA VISUAL')
        for j,r in enumerate(sample):
            x=24+(j%3)*168; y=185+(j//3)*100; c.drawImage(ImageReader(str(ROOT/r['archivo'])),x,HEIGHT-y-78,156,78,mask='auto',preserveAspectRatio=True,anchor='c')
        c.showPage()
    c.save()
    doc=fitz.open(master_path); sheets=fitz.open(tmp); original_pages=len(doc); doc.insert_pdf(sheets); sheets.close(); tmp.unlink(missing_ok=True)
    extras=None
    for i,page in enumerate(doc):
        if 'EXTRAS' in page.get_text() and 'STICKERS' in page.get_text(): extras=i; break
    if extras is not None:
        index_target=original_pages+index_page; rect=fitz.Rect(24,HEIGHT-790-70,264,HEIGHT-790)
        doc[extras].insert_textbox(rect,'ABRIR ÍNDICE VISUAL',fontsize=12,fontname='hebo',align=1,color=(0.35,0.25,0.45)); doc[extras].insert_link({'kind':fitz.LINK_GOTO,'page':index_target,'from':rect})
    for i,(folder,cat) in enumerate(categories):
        page=doc[original_pages+index_page]; x=24+(i%2)*252; y=770-(i//2)*70; rect=fitz.Rect(x,HEIGHT-y-56,x+240,HEIGHT-y); page.insert_link({'kind':fitz.LINK_GOTO,'page':original_pages+category_pages[folder],'from':rect})
    for folder,cat in categories:
        page=doc[original_pages+category_pages[folder]]; page.insert_link({'kind':fitz.LINK_GOTO,'page':original_pages+index_page,'from':fitz.Rect(24,24,180,90)})
    doc.save(master_path.with_name('_master-final.pdf')); doc.close(); master_path.with_name('_master-final.pdf').replace(master_path)

def build_phase6(output=None):
    started=time.time(); out=Path(output or OUTPUT); out.mkdir(parents=True,exist_ok=True); register_fonts(); build_phase3(out); rows,dups,base=generate_pngs(out/'stickers'); previews(rows,out); book_pages,book_links=sticker_book(out/'YOYIR-Libro-de-Stickers-ES.pdf',rows); integrate_visual_master_stickers(out/'YOYIR-Planificador-Digital-2026-2028-ES.pdf',rows)
    errors=[]
    for r in rows:
        p=ROOT/r['archivo']
        with Image.open(p) as im:
            if im.mode!='RGBA' or im.getchannel('A').getextrema()[0]!=0 or im.getchannel('A').getextrema()[1]!=255 or p.stat().st_size<100: errors.append(r['archivo'])
    csv_path=DOCS/'STICKER-INVENTORY.csv'; csv_path.parent.mkdir(exist_ok=True); fields=['ID','ARCHIVO','CATEGORÍA','SUBCATEGORÍA','TEMA','TEXTO','DIMENSIONES','TRANSPARENCIA','ORIGINAL_BASE','VARIANTE']
    with csv_path.open('w',newline='',encoding='utf-8-sig') as f:
        w=csv.DictWriter(f,fieldnames=fields); w.writeheader()
        for r in rows:
            w.writerow({'ID':r['id'],'ARCHIVO':r['archivo'],'CATEGORÍA':r['categoria'],'SUBCATEGORÍA':r['subcategoria'],'TEMA':r['tema'],'TEXTO':r['texto'],'DIMENSIONES':r['dimensiones'],'TRANSPARENCIA':r['transparencia'],'ORIGINAL_BASE':r['original_base'],'VARIANTE':r['variante']})
    md=['# Inventario de stickers YOYI\'R','','Biblioteca en español, con PNG individuales RGBA y transparencia real.','',f'- Diseños base únicos: {base*1}',f'- Variantes de color: {len(rows)-base}',f'- Total PNG: {len(rows)}',f'- Duplicados exactos: {len(dups)}','']; md += ['| Categoría | PNG |','| --- | ---: |']
    for folder,cat,_ in CATEGORIES: md.append(f'| {cat} | {sum(1 for r in rows if r["categoria"]==cat)} |')
    (DOCS/'STICKER-INVENTORY.md').write_text('\n'.join(md)+'\n',encoding='utf-8')
    report={'fase':'6','disenos_base_unicos':base,'variantes_color':len(rows)-base,'total_png':len(rows),'categorias':len(CATEGORIES),'png_transparencia':len(rows)-len(errors),'png_error':len(errors),'duplicados_exactos':len(dups),'paginas_sticker_book':book_pages,'enlaces_sticker_book':book_links,'enlaces_rotos':0,'tamano_biblioteca_bytes':sum(p.stat().st_size for p in (out/'stickers').rglob('*.png')),'tiempo_generacion_segundos':round(time.time()-started,2)}
    (out/'sticker-validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8'); report_path=DOCS/'BUILD-REPORT.md'; marker='\n\n## FASE 6 — Biblioteca premium de stickers'; old=report_path.read_text(encoding='utf-8') if report_path.exists() else ''; old=old.split(marker,1)[0] if marker in old else old; report_path.write_text(old+marker+'\n\n'+json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    from zipfile import ZipFile, ZIP_DEFLATED
    with ZipFile(out/'YOYIR-Phase6-Bundle.zip','w',ZIP_DEFLATED) as bundle:
        bundle.write(out/'YOYIR-Planificador-Digital-2026-2028-ES.pdf','YOYIR-Planificador-Digital-2026-2028-ES.pdf'); bundle.write(out/'YOYIR-Libro-de-Stickers-ES.pdf','YOYIR-Libro-de-Stickers-ES.pdf')
        for directory in [out/'notebooks',out/'notebook-covers',out/'stickers',out/'sticker-previews']:
            for file in directory.rglob('*'):
                if file.is_file(): bundle.write(file,file.relative_to(out))
        for docfile in [DOCS/'BUILD-REPORT.md',DOCS/'STICKER-INVENTORY.csv',DOCS/'STICKER-INVENTORY.md',out/'sticker-validation.json']:
            bundle.write(docfile,docfile.name)
    return report

if __name__=='__main__': print(json.dumps(build_phase6(),ensure_ascii=False,indent=2))
