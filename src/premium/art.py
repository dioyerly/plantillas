from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics

W,H=540,960
INK='#383940'; RULE='#DCD7D2'; PAPER='#FFFCF7'
COLORS=['#CBB9E5','#E9BBCB','#EFAFA3','#F4C8A7','#F3DFA0','#B9CEAD','#BDE0CF','#B6D8EA','#BDC6EC','#DCCBB7']
NAMES=['LAVANDA','BLUSH','CORAL','PEACH','YELLOW','SAGE','MINT','SKY','PERIWINKLE','SAND']

class Art:
    def __init__(self,c,page,nav):
        self.c,self.page,self.nav=c,page,nav
        self.icons=[]; self.stickers=0; self.calendars=[]
    def box(self,x,y,w,h,fill=PAPER,r=8,stroke=None):
        c=self.c;c.setFillColor(HexColor(fill));c.setStrokeColor(HexColor(stroke or fill));c.setLineWidth(.65)
        c.roundRect(x,H-y-h,w,h,r,fill=1,stroke=bool(stroke))
    def line(self,x,y,x2,y2,color=RULE,width=.7):
        c=self.c;c.setStrokeColor(HexColor(color));c.setLineWidth(width);c.line(x,H-y,x2,H-y2)
    def text(self,s,x,y,size=13,font='Body',color=INK,center=False):
        c=self.c;c.setFillColor(HexColor(color));c.setFont('Y'+font,size)
        if center:c.drawCentredString(x,H-y,str(s))
        else:c.drawString(x,H-y,str(s))
    def circle(self,x,y,r,fill=None,stroke=INK,width=1):
        c=self.c;c.setFillColor(HexColor(fill or PAPER));c.setStrokeColor(HexColor(stroke));c.setLineWidth(width)
        c.circle(x,H-y,r,fill=bool(fill),stroke=bool(stroke))
    def lines(self,x,y,w,n=3,gap=28):
        for i in range(n):self.line(x,y+i*gap,x+w,y+i*gap)
    def label(self,s,x,y,color=COLORS[0],w=None):
        w=w or pdfmetrics.stringWidth(s,'YBold',11)+18
        self.box(x,y-15,w,21,color,r=3);self.text(s,x+9,y,11,'Bold')
    def title(self,title,kicker='',color=COLORS[0]):
        self.text(kicker,60,125,10,'Bold', '#6D6670')
        size=27 if len(title)<23 else 23
        self.text(title,58,163,size,'Editorial')
        self.line(60,180,136,180,color,5)
    def link(self,target,x,y,w,h,label,minimum=64):
        assert w>=minimum and h>=minimum,(label,w,h)
        self.c.linkAbsolute(label,target,Rect=(x,H-y-h,x+w,H-y),thickness=0)
        self.nav.append({'source':self.page,'target':target,'rect':[x,y,x+w,y+h],'label':label})
    def tab(self,label,target,x,y,w,h,color,active=False):
        # Colored tab emerges from the page edge, with a short seam and exposed lip.
        self.box(x+2,y+3,w,h,'#DED8D3',r=9)
        self.box(x,y,w,h,color,r=9)
        self.line(x+7,y+h-7,x+w-7,y+h-7,'#FFFCF7',1)
        self.text(label,x+w/2,y+h/2+5,13,'Bold',center=True)
        if active:self.line(x+12,y+8,x+w-12,y+8,INK,1.4)
        self.link(target,x,y,w,h,label)
    def chip(self,label,target,x,y,w=116,color=COLORS[0],h=66):
        self.box(x,y,w,h,color,r=24)
        self.text(label,x+w/2,y+h/2+5,13,'Bold',center=True)
        self.link(target,x,y,w,h,label)
    def check(self,x,y,w=150,n=3,gap=30):
        for i in range(n):
            self.box(x,y+i*gap,11,11,PAPER,r=2,stroke='#938C92')
            self.line(x+21,y+11+i*gap,x+w,y+11+i*gap)
    def bar(self,x,y,w=160,segments=8,color=COLORS[5]):
        self.box(x,y,w,17,PAPER,r=8,stroke='#A29BA1')
        for i in range(1,segments):self.line(x+i*w/segments,y+2,x+i*w/segments,y+15,color,1)
        self.text('0',x,y+34,10);self.text('100 %',x+w,y+34,10,center=True)
    def dots(self,x,y,cols=7,rows=4,gap=20):
        for r in range(rows):
            for col in range(cols):self.circle(x+col*gap,y+r*gap,3.2,stroke='#A49C9C',width=.65)
    def tape(self,x,y,w=70,color=COLORS[4]):
        c=self.c;c.setFillColor(HexColor(color));p=c.beginPath()
        p.moveTo(x,H-y);p.lineTo(x+w-4,H-y-2);p.lineTo(x+w,H-y-15);p.lineTo(x+3,H-y-18);p.close()
        c.drawPath(p,fill=1,stroke=0)
        for i in range(8,int(w)-4,12):self.line(x+i,y+3,x+i-3,y+14,PAPER,.6)
    def sticky(self,x,y,w,h,color=COLORS[4]):
        self.box(x+3,y+4,w,h,'#E7E0D6',r=2)
        self.box(x,y,w,h,color,r=2)
        self.tape(x+w/2-28,y-8,56,COLORS[3])
    def icon(self,name,x,y,size=44,color=INK):
        self.icons.append(name)
        c=self.c;c.saveState();c.translate(x,H-y-size);c.scale(size/48,size/48)
        c.setStrokeColor(HexColor(color));c.setFillColor(HexColor(PAPER));c.setLineWidth(1.65);c.setLineCap(1);c.setLineJoin(1)
        def line(a,b,cc,d):c.line(a,b,cc,d)
        def rect(a,b,w,h,r=3):c.roundRect(a,b,w,h,r,stroke=1,fill=0)
        def circ(a,b,r):c.circle(a,b,r,stroke=1,fill=0)
        def path(points,close=False):
            p=c.beginPath();p.moveTo(*points[0])
            for point in points[1:]:p.lineTo(*point)
            if close:p.close()
            c.drawPath(p,stroke=1,fill=0)
        if name in ('agenda','libro'):
            if name=='agenda':
                rect(9,5,31,38);line(16,5,16,43)
                for yy in (12,22,32):line(5,yy,12,yy)
                line(23,31,33,31);line(23,24,33,24)
            else:
                path([(24,9),(7,14),(7,40),(24,35),(41,40),(41,14),(24,9)])
                line(24,9,24,35)
                for yy in (20,26,32):line(12,yy,19,yy-2);line(29,yy-2,36,yy)
        elif name=='lapiz':
            path([(10,9),(15,22),(34,41),(42,33),(23,14),(10,9)],True);line(15,22,23,14);line(31,37,38,30)
        elif name in ('estrella','sol'):
            import math
            if name=='estrella':
                path([(24+(18 if i%2==0 else 8)*math.sin(i*math.pi/5),24+(18 if i%2==0 else 8)*math.cos(i*math.pi/5)) for i in range(10)],True)
            else:
                circ(24,24,10)
                for i in range(8):
                    a=i*math.pi/4;line(24+16*math.cos(a),24+16*math.sin(a),24+21*math.cos(a),24+21*math.sin(a))
        elif name=='luna':
            p=c.beginPath();p.moveTo(32,42);p.curveTo(0,45,0,1,32,6);p.curveTo(11,13,11,33,32,42);c.drawPath(p)
        elif name in ('hoja','planta'):
            line(24,7,24,40)
            for yy,side in [(16,-1),(24,1),(31,-1)]:
                p=c.beginPath();p.moveTo(24,yy);p.curveTo(24+side*20,yy-3,24+side*19,yy+17,24,yy+3);c.drawPath(p)
            if name=='planta':path([(14,11),(17,2),(31,2),(34,11)],True)
        elif name in ('cartera','maleta'):
            rect(5,9,38,28)
            if name=='maleta':
                rect(17,37,14,6);line(14,10,14,36);line(34,10,34,36)
            else:rect(28,19,16,10);circ(33,24,1)
        elif name=='corazon':
            p=c.beginPath();p.moveTo(24,8);p.curveTo(-8,29,13,51,24,34);p.curveTo(35,51,56,29,24,8);c.drawPath(p)
        elif name=='check':path([(8,23),(19,12),(40,37)])
        elif name=='reloj':circ(24,24,18);line(24,24,24,37);line(24,24,34,20)
        elif name=='taza':rect(7,9,26,26);c.arc(26,14,46,32,-90,180);line(10,4,36,4);line(15,39,15,44);line(24,39,24,44)
        elif name=='auriculares':
            c.arc(7,9,41,43,0,180);rect(5,8,8,18);rect(35,8,8,18)
        elif name=='casa':path([(4,25),(24,43),(44,25)]);path([(10,25),(10,6),(38,6),(38,25)]);rect(21,6,9,15,0)
        elif name=='sobre':rect(5,10,38,28,2);path([(6,36),(24,22),(42,36)])
        elif name=='regalo':
            rect(7,6,34,27,1);rect(4,29,40,7,1);line(24,6,24,36)
            c.ellipse(11,35,24,44);c.ellipse(24,35,37,44)
        elif name=='avion':path([(4,24),(44,42),(29,5),(23,20),(4,24),(44,42),(23,20)],False)
        elif name=='pastel':
            rect(6,6,36,23,3);line(6,19,42,19)
            for xx in (15,24,33):line(xx,29,xx,37);circ(xx,41,2)
        elif name=='zapatilla':path([(5,9),(44,9),(44,18),(28,24),(23,36),(13,31),(8,33),(5,9)],True);line(6,14,42,14);line(22,26,29,29);line(25,22,32,25)
        elif name=='botella':rect(14,4,20,31,6);rect(18,35,12,9,2);line(16,17,32,17);line(16,27,32,27)
        elif name=='comida':circ(24,24,15);circ(24,24,10);line(3,8,3,40);line(45,8,45,40)
        elif name=='camara':rect(4,9,40,28);circ(25,23,10);rect(12,37,12,6);circ(37,31,2)
        elif name=='gota':
            p=c.beginPath();p.moveTo(24,44);p.curveTo(17,33,7,19,13,9);p.curveTo(19,-1,36,3,36,16);p.curveTo(36,24,28,37,24,44);c.drawPath(p)
        elif name=='flecha':path([(6,24),(42,24),(32,34)]);path([(42,24),(32,14)])
        elif name=='clip':
            p=c.beginPath();p.moveTo(17,15);p.lineTo(17,35);p.curveTo(17,44,33,44,33,35);p.lineTo(33,10);p.curveTo(33,0,10,0,10,10);p.lineTo(10,34);c.drawPath(p)
        else:raise ValueError(name)
        c.restoreState()
    def sticker(self,name,x,y,size=66,color=COLORS[0]):
        self.stickers+=1
        self.circle(x+size/2+1.5,y+size/2+2,size/2,fill='#E5DED8',stroke='#E5DED8')
        self.circle(x+size/2,y+size/2,size/2,fill='#FFFFFF',stroke='#FFFFFF')
        self.circle(x+size/2,y+size/2,size/2-4,fill=color,stroke=color)
        self.icon(name,x+size*.19,y+size*.19,size*.62)
