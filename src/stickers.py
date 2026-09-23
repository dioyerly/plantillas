"""Original vector sticker primitives rasterized into transparent PNGs."""
from io import BytesIO
import fitz
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from .config import STICKER_CATEGORIES

SAMPLES = [('FOCUS','PRIORITIES'),('TODAY','FUNCTIONAL'),('NOTE','LABELS'),('PAY DAY','MONEY'),
           ('READ','READING'),('MOVE','FITNESS'),('REST','SELF CARE'),('PLAN','WORK'),
           ('REMEMBER','APPOINTMENTS'),('SMALL WIN','MOOD'),('SAVE','SAVINGS'),('TO DO','CHECKBOXES')]

def inventory():
    # 28 categories x 60 reserved variants = 1680 stable asset IDs.
    return [{'id':f'{category.lower().replace(" ","-")}-{n:03d}',
             'category':category,'variant':n,'status':'reserved'}
            for category in STICKER_CATEGORIES for n in range(1,61)]

def generate_stickers(folder,themes):
    folder.mkdir(parents=True,exist_ok=True)
    files=[]
    palettes=list(themes.values())
    for i,(label,category) in enumerate(SAMPLES):
        t=palettes[i%len(palettes)]
        buf=BytesIO()
        c=canvas.Canvas(buf,pagesize=(312,180),pdfVersion=(1,4))
        c.setFillColor(HexColor(t.soft))
        c.setStrokeColor(HexColor(t.accent))
        c.setLineWidth(1.3)
        shape=i%4
        if shape==0:
            c.roundRect(12,40,288,100,18,fill=1,stroke=0)
        elif shape==1:
            path=c.beginPath(); path.moveTo(12,40); path.lineTo(300,40)
            path.lineTo(275,90); path.lineTo(300,140); path.lineTo(12,140); path.close()
            c.drawPath(path,fill=1,stroke=0)
        elif shape==2:
            c.roundRect(12,35,288,110,54,fill=1,stroke=1)
        else:
            c.roundRect(12,35,288,110,8,fill=1,stroke=0)
            c.roundRect(25,78,24,24,4,fill=0,stroke=1)
        c.setFillColor(HexColor(t.ink))
        c.setFont('YBold',24)
        c.drawCentredString(163 if shape==3 else 156,82,label)
        c.showPage(); c.save()
        document=fitz.open(stream=buf.getvalue(),filetype='pdf')
        pix=document[0].get_pixmap(matrix=fitz.Matrix(4,4),alpha=True)
        file=folder/f'{i+1:02d}-{label.lower().replace(" ","-")}.png'
        pix.save(file)
        files.append(file)
        document.close()
    return files
