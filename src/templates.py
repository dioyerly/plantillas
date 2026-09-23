"""Reusable writing layouts, kept independent of page registration."""

def notes(d,kind,x=24,y=196,w=492,h=654):
    d.box(x,y,w,h,stroke=True)
    if kind in ('lined','study','project'):
        for yy in range(int(y+35),int(y+h-12),29):
            d.line(x+16,yy,x+w-16,yy)
        if kind=='study':
            d.line(x+130,y+12,x+130,y+h-130)
            d.box(x+1,y+h-129,w-2,128,d.t.background)
            d.text('SUMMARY',x+16,y+h-101,12,'Bold')
        if kind=='project':
            d.text('PROJECT / DATE',x+16,y+22,11,'Bold')
    elif kind=='grid':
        for xx in range(int(x+16),int(x+w-10),20):
            d.line(xx,y+16,xx,y+h-16)
        for yy in range(int(y+16),int(y+h-10),20):
            d.line(x+16,yy,x+w-16,yy)
    elif kind=='dot':
        from reportlab.lib.colors import HexColor
        from .config import HEIGHT
        d.c.setFillColor(HexColor(d.t.rule))
        for xx in range(int(x+18),int(x+w-12),18):
            for yy in range(int(y+18),int(y+h-12),18):
                d.c.circle(xx,HEIGHT-yy,.7,stroke=0,fill=1)
    elif kind=='cornell':
        d.text('CUES',x+12,y+23,11,'Bold')
        d.text('NOTES',x+146,y+23,11,'Bold')
        d.line(x+132,y,x+132,y+h-130)
        d.line(x,y+h-130,x+w,y+h-130)
        d.text('SUMMARY',x+12,y+h-106,11,'Bold')
        for yy in range(int(y+59),int(y+h-140),29):
            d.line(x+146,yy,x+w-12,yy)
        for yy in range(int(y+h-76),int(y+h-8),29):
            d.line(x+12,yy,x+w-12,yy)

def two_panels(d,labels,annual=False):
    w=408 if annual else 492
    for i,label in enumerate(labels):
        h=(654-12*(len(labels)-1))/len(labels)
        d.panel(label,24,196+i*(h+12),w,h)

def tracker(d,days,x=24,y=250,w=408):
    # Writing cells are not buttons. Split into two bands for larger annotation space.
    for band,(start,end) in enumerate([(1,16),(17,days)]):
        yy=y+band*225
        d.text(f'DAYS {start:02d}—{end:02d}',x,yy-15,12,'Bold')
        n=end-start+1
        cell=w/n
        for i in range(n):
            d.text(start+i,x+(i+.5)*cell,yy+18,10,center=True)
            d.line(x+i*cell,yy+28,x+i*cell,yy+172)
        d.line(x+w,yy+28,x+w,yy+172)
        for row in range(5):
            d.line(x,yy+28+row*36,x+w,yy+28+row*36)

def sample_template(d,kind):
    if kind=='vision':
        d.panel('HOW I WANT MY DAYS TO FEEL',24,196,492,150)
        d.panel('PEOPLE, PLACES & EXPERIENCES',24,360,240,238)
        d.panel('SPACE FOR IMAGES OR WORDS',276,360,240,238)
        d.panel('ONE SMALL STEP THIS WEEK',24,612,492,238)
    elif kind=='reading':
        d.table(['TITLE / AUTHOR','STARTED','FINISHED'],24,196,492,10,44,[290,101,101])
        d.panel('IDEAS I WANT TO KEEP',24,700,492,150)
    elif kind=='wellbeing':
        d.paragraph('Notice your patterns with curiosity. Choose your own words and scale.',24,207,480)
        d.table(['DAY','MOOD','ENERGY','SLEEP'],24,258,492,7,51,[81,137,137,137])
        d.panel('WHAT SUPPORTED ME?',24,674,492,176)
    elif kind=='movement':
        d.panel('MY INTENTION / WHAT FEELS POSSIBLE',24,196,492,110)
        d.table(['DAY','MOVEMENT','TIME / NOTES'],24,328,492,7,48,[80,210,202])
        d.panel('WHAT I ENJOYED',24,718,492,132)
    elif kind=='gratitude':
        two_panels(d,['A SMALL MOMENT I APPRECIATED','SOMEONE WHO MADE A DIFFERENCE','SOMETHING I WANT TO REMEMBER'])
    elif kind=='reflection':
        two_panels(d,['WHAT IS TAKING UP SPACE?','WHAT WOULD KINDNESS LOOK LIKE?','WHAT CAN I LET GO OF?'])
    elif kind=='project':
        d.panel('OUTCOME / WHY IT MATTERS',24,196,492,128)
        d.table(['NEXT ACTION','WHEN','STATUS'],24,342,492,7,43,[292,100,100])
        d.panel('RESOURCES / OPEN QUESTIONS',24,704,492,146)
    elif kind=='focus':
        d.panel('ONE TASK / DEFINITION OF DONE',24,196,492,136)
        d.panel('START / FINISH / BREAKS',24,346,492,110)
        d.panel('DISTRACTIONS TO PARK',24,470,240,220)
        d.panel('WORKING NOTES',276,470,240,220)
        d.panel('WHAT MOVED FORWARD?',24,704,492,146)
    elif kind=='budget':
        d.panel('PERIOD / CURRENCY / INTENTION',24,196,492,106)
        d.table(['CATEGORY','PLANNED','ACTUAL'],24,322,492,8,41,[250,121,121])
        d.panel('INCOME / SAVINGS / REVIEW',24,704,492,146)
    elif kind=='expenses':
        d.text('PERIOD / CURRENCY',24,210,12,'Bold')
        d.line(150,212,516,212)
        d.table(['DATE','DESCRIPTION','AMOUNT'],24,240,492,11,43,[92,285,115])
        d.panel('NOTES',24,772,492,78)
    else:
        notes(d,kind)
