import os
from pathlib import Path
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from .config import WIDTH, HEIGHT, FONT_FILES

def register_fonts():
    root = Path(os.environ.get('YOYIR_FONT_DIR', 'C:/Windows/Fonts'))
    for key,file in FONT_FILES.items():
        path = root / file
        if not path.is_file():
            raise FileNotFoundError(f'Font required: {path}. Set YOYIR_FONT_DIR to your licensed font directory.')
        pdfmetrics.registerFont(TTFont('Y'+key, str(path)))

class Drawing:
    def __init__(self, canvas, theme, navigation, page):
        self.c, self.t, self.nav, self.page = canvas, theme, navigation, page
        self.text_boxes = []

    def box(self,x,y,w,h,color=None,stroke=False,radius=10):
        self.c.setFillColor(HexColor(color or self.t.paper))
        self.c.setStrokeColor(HexColor(self.t.rule))
        self.c.setLineWidth(.6)
        self.c.roundRect(x,HEIGHT-y-h,w,h,radius,fill=1,stroke=int(stroke))

    def text(self,text,x,y,size=14,font='Body',color=None,center=False):
        text = str(text)
        self.c.setFillColor(HexColor(color or self.t.ink))
        self.c.setFont('Y'+font,size)
        width = pdfmetrics.stringWidth(text,'Y'+font,size)
        left = x-width/2 if center else x
        assert left>=0 and left+width<=WIDTH+.01, (self.page,text,left,width)
        self.c.drawString(left,HEIGHT-y,text)

    def paragraph(self,text,x,y,w,size=14,leading=21,color=None):
        words = text.split()
        current = ''
        for word in words:
            candidate = (current+' '+word).strip()
            if current and pdfmetrics.stringWidth(candidate,'YBody',size)>w:
                self.text(current,x,y,size,color=color)
                y += leading
                current = word
            else:
                current = candidate
        if current:
            self.text(current,x,y,size,color=color)
        return y+leading

    def line(self,x,y,x2,y2,color=None):
        self.c.setStrokeColor(HexColor(color or self.t.rule))
        self.c.setLineWidth(.6)
        self.c.line(x,HEIGHT-y,x2,HEIGHT-y2)

    def button(self,label,target,x,y,w,h=66):
        self.box(x,y,w,h,self.t.soft)
        # Deliberate wrapping preserves legibility instead of shrinking labels.
        words=label.split()
        lines=['']
        for word in words:
            candidate=(lines[-1]+' '+word).strip()
            if pdfmetrics.stringWidth(candidate,'YBold',15)>w-16:
                lines.append(word)
            else:
                lines[-1]=candidate
        assert len(lines)<=3,(label,lines)
        for j,s in enumerate(lines):
            self.text(s,x+w/2,y+h/2+5+(j-(len(lines)-1)/2)*19,15,'Bold',center=True)
        self.nav.link(self.c,self.page,target,label,(x,y,w,h))

    def panel(self,label,x,y,w,h,spacing=29):
        self.box(x,y,w,h,stroke=True)
        self.text(label,x+12,y+23,12,'Bold',self.t.accent)
        self.line(x+12,y+34,x+w-12,y+34)
        for yy in range(int(y+34+spacing),int(y+h-8),spacing):
            self.line(x+12,yy,x+w-12,yy)

    def header(self,title,kicker='A LITTLE STRUCTURE. MORE ROOM TO LIVE.',annual=False,notebook=False):
        content_w = 408 if annual else 492
        width=(content_w-16)/3
        for i,(label,target) in enumerate([('HOME','home'),('INDEX','index'),('SECTIONS' if notebook else 'YEAR','index' if notebook else 'years')]):
            self.button(label,target,24+i*(width+8),24,width)
        self.text(title,24,139,27 if len(title)<25 else 23,'Editorial')
        self.text(kicker,24,164,10,'Bold',self.t.accent)

    def footer(self,items,annual=False):
        content_w=408 if annual else 492
        width=(content_w-8*(len(items)-1))/len(items)
        for i,(label,target) in enumerate(items):
            self.button(label,target,24+i*(width+8),876,width)

    def table(self,headers,x,y,w,rows=8,row_h=38,widths=None):
        widths=widths or [w/len(headers)]*len(headers)
        self.box(x,y,w,34,self.t.soft,radius=4)
        xx=x
        for head,col_w in zip(headers,widths):
            self.text(head,xx+9,y+22,11,'Bold')
            if xx>x:
                self.line(xx,y+34,xx,y+34+rows*row_h)
            xx+=col_w
        for r in range(rows+1):
            self.line(x,y+34+r*row_h,x+w,y+34+r*row_h)

    def month_tabs(self,year):
        from .config import MONTHS
        for i,label in enumerate(MONTHS):
            target='month' if year==2026 and i==0 else f'month-{year}-{i+1:02d}'
            self.button(label,target,444,24+i*71,72,66)
