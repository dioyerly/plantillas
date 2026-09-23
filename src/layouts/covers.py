from reportlab.lib.colors import HexColor
from ..config import HEIGHT, COVER_CATEGORIES

def artwork(d,variant,x=48,y=190,w=444,h=240):
    c,t=d.c,d.t
    mode=variant
    c.setStrokeColor(HexColor(t.accent))
    c.setFillColor(HexColor(t.soft))
    c.setLineWidth(1)
    if mode==0:
        d.box(x+w*.22,y+12,w*.56,h-24,t.soft,radius=80)
        d.line(x+w/2,y+42,x+w/2,y+h-42,t.accent)
    elif mode==1:
        for i in range(5):
            d.box(x+18+i*79,y+26+(i%2)*28,63,h-78,t.soft if i%2==0 else t.paper,radius=30)
    elif mode==2:
        c.ellipse(x+20,HEIGHT-y-h+18,x+w*.7,HEIGHT-y-14,fill=1,stroke=0)
        c.setFillColor(HexColor(t.background))
        c.ellipse(x+w*.4,HEIGHT-y-h+4,x+w-10,HEIGHT-y-56,fill=1,stroke=0)
        d.line(x+50,y+h-25,x+w-40,y+45,t.accent)
    elif mode==3:
        for stem in range(3):
            sx=x+90+stem*128
            d.line(sx,y+h-15,sx-15,y+15,t.accent)
            for j in range(4):
                yy=y+40+j*42
                c.setFillColor(HexColor(t.soft))
                c.ellipse(sx-53,HEIGHT-yy-22,sx-5,HEIGHT-yy+2,fill=1,stroke=1)
                c.ellipse(sx-5,HEIGHT-yy-45,sx+39,HEIGHT-yy-20,fill=1,stroke=1)
    elif mode==4:
        c.circle(x+w/2,HEIGHT-y-h/2,80,fill=1,stroke=0)
        c.setFillColor(HexColor(t.background))
        c.circle(x+w/2+30,HEIGHT-y-h/2+16,70,fill=1,stroke=0)
        for xx,yy in [(x+50,y+50),(x+w-58,y+70),(x+90,y+h-35),(x+w-40,y+h-28)]:
            d.line(xx-8,yy,xx+8,yy,t.accent); d.line(xx,yy-8,xx,yy+8,t.accent)
    elif mode==5:
        for i in range(3):
            c.setStrokeColor(HexColor(t.accent)); c.setFillColor(HexColor(t.soft))
            c.circle(x+94+i*128,HEIGHT-y-h/2,54,fill=i%2==0,stroke=1)
            d.line(x+40+i*128,y+h/2,x+148+i*128,y+h/2,t.accent)
    elif mode==6:
        d.text('Y',x+w/2,y+h-34,210,'Editorial',t.soft,True)
        d.text('MAKE SPACE',x+w/2,y+h/2,18,'Bold',t.accent,True)
        d.text('FOR YOUR LIFE',x+w/2,y+h/2+28,18,'Bold',t.accent,True)
    elif mode==7:
        for inset in range(0,33,11):
            c.setStrokeColor(HexColor(t.accent))
            c.roundRect(x+inset,HEIGHT-y-h+inset,w-2*inset,h-2*inset,18,fill=0,stroke=1)
        d.text('Y / R',x+w/2,y+h/2+15,44,'Editorial',t.accent,True)
    elif mode==8:
        d.box(x+42,y+24,w-84,h-48,t.soft,radius=2)
        d.box(x+80,y+50,w-160,h-100,t.background,radius=2)
        d.text('01 / BEGIN AGAIN',x+w/2,y+h/2+5,17,'Editorial',t.accent,True)
    elif mode==9:
        for i in range(6):
            d.box(x+25+i*65,y+20+i*13,47,h-58-i*13,t.soft if i%2==0 else t.paper,radius=20)
        d.line(x+25,y+h-17,x+w-47,y+h-17,t.accent)
    elif mode==10:
        for i in range(4):
            c.setStrokeColor(HexColor(t.accent))
            path=c.beginPath()
            path.moveTo(x+25,HEIGHT-y-h+25+i*18)
            path.curveTo(x+w*.3,HEIGHT-y+35+i*6,x+w*.6,HEIGHT-y-h-12+i*12,x+w-25,HEIGHT-y-20-i*15)
            c.drawPath(path,stroke=1,fill=0)
        c.setFillColor(HexColor(t.soft))
        c.circle(x+w-80,HEIGHT-y-60,36,fill=1,stroke=0)
    elif mode==11:
        sx=x+w/2
        d.line(sx-70,y+h-15,sx+65,y+10,t.accent)
        for j in range(5):
            xx=sx-48+j*25; yy=y+h-48-j*34
            c.setFillColor(HexColor(t.soft))
            c.ellipse(xx-50,HEIGHT-yy-8,xx+6,HEIGHT-yy+22,fill=1,stroke=1)
            c.ellipse(xx+4,HEIGHT-yy-25,xx+58,HEIGHT-yy+5,fill=1,stroke=1)

def cover(d,variant=0,sample=False,notebook=False):
    d.box(16,16,508,934,d.t.soft, radius=20)
    d.box(30,30,480,906,d.t.background,radius=16)
    if sample:
        d.button('HOME','home',48,48,214)
        d.button('INDEX','index',278,48,214)
    d.text("E-books para la vida — YOYI'R",270,151,13,'Body',center=True)
    artwork(d,variant)
    d.text("YOYI'R",270,501,47,'Editorial',center=True)
    d.text('DIGITAL NOTEBOOK' if notebook else 'DIGITAL PLANNER',270,544,24,'Bold',center=True)
    d.text('10 SECTIONS / YOUR OWN RHYTHM' if notebook else '2026 • 2027 • 2028',270,581,19,'Body',center=True)
    d.text('Plan • Organize • Focus • Grow',270,624,17,'Body',center=True)
    if sample:
        d.button('PREVIOUS' if variant else 'INDEX',f'cover-{variant:02d}' if variant else 'index',48,680,214,76)
        d.button('NEXT' if variant<11 else 'INDEX',f'cover-{variant+2:02d}' if variant<11 else 'index',278,680,214,76)
    else:
        d.button('OPEN NOTEBOOK' if notebook else 'OPEN PLANNER','index' if notebook else 'welcome',92,680,356,76)
    d.text('THIS SPACE BELONGS TO',270,800,11,'Bold',center=True)
    d.line(110,842,430,842)
    if sample:
        d.text(f'COVER {variant+1:02d} / {COVER_CATEGORIES[variant%8]}',270,889,11,'Bold',center=True)

def cover_catalog():
    return [{'id':f'cover-{i+1:03d}', 'category':COVER_CATEGORIES[i%8],
             'composition':i if i<12 else None, 'edition':i//8, 'status':'rendered' if i<12 else 'reserved'} for i in range(150)]
