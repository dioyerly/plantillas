from datetime import date
from .covers import cover
from ..config import MODULES, MONTHS, MONTH_NAMES
from ..planner.dates import month_weeks, week_dates
from ..planner.manifest import SAMPLES
from ..templates import notes, sample_template, two_panels, tracker
from ..themes import THEMES

def grid_buttons(d,items,y=196,columns=2,w=492,h=72,gap=12):
    bw=(w-gap*(columns-1))/columns
    for i,(label,target) in enumerate(items):
        d.button(label,target,24+(i%columns)*(bw+gap),y+(i//columns)*(h+gap),bw,h)

def calendar(d,year,month,x,y,w,h,small=False):
    weeks=month_weeks(year,month)
    if small:
        d.box(x,y,w,h,d.t.paper,stroke=True,radius=5)
        d.text(MONTH_NAMES[month-1].upper(),x+9,y+15,10,'Bold',d.t.accent)
        top=y+30
        rh=(h-40)/6
        for i,label in enumerate(['M','T','W','T','F','S','S']):
            d.text(label,x+(i+.5)*w/7,top,8,'Bold',center=True)
        for row,week in enumerate(weeks):
            for col,number in enumerate(week):
                if number:
                    d.text(number,x+(col+.5)*w/7,top+12+row*rh,8,center=True)
    else:
        header=32
        rh=(h-header)/len(weeks)
        d.box(x,y,w,header,d.t.soft,radius=4)
        for i,label in enumerate(['MON','TUE','WED','THU','FRI','SAT','SUN']):
            d.text(label,x+(i+.5)*w/7,y+22,10,'Bold',center=True)
        for i in range(8):
            d.line(x+i*w/7,y+header,x+i*w/7,y+h)
        for row in range(len(weeks)+1):
            d.line(x,y+header+row*rh,x+w,y+header+row*rh)
        for row,week in enumerate(weeks):
            for col,number in enumerate(week):
                if number:
                    d.text(number,x+col*w/7+8,y+header+row*rh+19,12,'Bold')

def draw_page(d,p,sticker_files):
    kind=p['kind']
    if kind in ('cover','cover_sample'):
        cover(d,p.get('variant',0),kind=='cover_sample')
        return
    annual='year' in p
    kicker = 'PHASE 1 / DESIGN & NAVIGATION EDITION'
    if p.get('month'):
        kicker='JANUARY 2026 / DATED SAMPLE'
    if kind in ('week','week_life'):
        dates=week_dates(date(2026,1,31))
        kicker=f"WEEK OF {dates[0]:%d %b %Y} — {dates[-1]:%d %b %Y}".upper()
    if kind in ('day','day_life'):
        kicker='31 JANUARY 2026 / DAILY SAMPLE'
    d.header(p['title'],kicker,annual)
    if annual:
        d.month_tabs(p['year'])
    if kind=='welcome':
        d.text('Plans can support your life.',24,237,28,'Editorial')
        d.text('They do not have to fill it.',24,275,28,'Editorial')
        y=326
        for paragraph in [
            "Welcome to E-books para la vida — YOYI'R. This is a space for clear intentions, useful routines and the small things you want to remember.",
            'Start with a year, explore the January sample, or make a page your own. Your handwriting and choices bring this planner to life.',
            'This edition includes complete annual calendars for 2026–2028 and selected working templates. The remaining dated daily and weekly pages belong to a later phase.',
            'Hyperlinked PDF Digital Planner designed for PDF annotation apps on tablets and phones.'
        ]:
            y=d.paragraph(paragraph,24,y,470,17,26)+24
        d.footer([('QUICK START','quick'),('INDEX','index')])
    elif kind=='quick':
        steps=[('01 / IMPORT','Save the PDF locally and import it into your PDF annotation app. Once imported, the planner needs no internet connection.'),
               ('02 / NAVIGATE','Tap the filled navigation tabs. Some apps activate links in reading mode. HOME returns to the cover; INDEX opens all sections.'),
               ('03 / WRITE','Use your app to write, draw, highlight or insert images. Ruled boxes, calendar cells and tracker marks are writing areas, not controls.'),
               ('04 / PERSONALIZE','Covers and themes are static page designs. Replacing covers, duplicating templates and adding PNG stickers depend on your app. Duplicating a page may preserve links to the original.'),
               ('05 / TEST','Month edge tabs stay in their selected year. Overview tabs use standard PDF zoom destinations: zoom back out to reach HOME or INDEX. Test this behavior in your app.')]
        y=206
        for title,body in steps:
            d.text(title,24,y,13,'Bold',d.t.accent)
            y=d.paragraph(body,24,y+25,480,15,21)+28
        d.footer([('YEAR SELECTOR','years'),('INDEX','index')])
    elif kind=='index':
        grid_buttons(d,[('HOME','home'),('YEAR','years'),('MONTH','month'),('WEEK','week'),('DAY','day'),('GOALS','goals'),('LIFE','life'),('WELLNESS','wellness'),('SELF-CARE','selfcare'),('PRODUCTIVITY','productivity'),('MONEY','money'),('NOTES','notes')],columns=3)
        d.text('MAKE IT YOURS',24,560,13,'Bold',d.t.accent)
        grid_buttons(d,[('6 THEMES','theme-lavender'),('12 COVERS','cover-01'),('STICKERS','stickers'),('QUICK START','quick')],y=580)
        d.paragraph('Notebook test: open YOYIR-Notebook-Test.pdf from the bundle. It is a separate, self-contained notebook.',24,788,480,15,22)
        d.footer([('WELCOME','welcome'),('YEAR SELECTOR','years')])
    elif kind=='years':
        grid_buttons(d,[(str(y),f'year-{y}') for y in (2026,2027,2028)]+[('UNDATED','undated')],y=214,h=144)
        d.panel('MY INTENTION FOR THIS SEASON',24,550,492,190)
        d.paragraph('Annual dates are complete. The expanded month, week and day examples use January 2026.',24,785,480,16,23)
        d.footer([('JANUARY SAMPLE','month'),('INDEX','index')])
    elif kind=='year':
        year=p['year']
        for month in range(1,13):
            x=24+((month-1)%2)*210
            y=191+((month-1)//2)*110
            calendar(d,year,month,x,y,198,103,True)
            d.nav.anchor(d.c,f'month-{year}-{month:02d}',p['id'],(x,y,198,103))
        d.footer([('PREVIOUS',f'year-{year-1}' if year>2026 else 'years'),('YEARS','years'),('NEXT',f'year-{year+1}' if year<2028 else 'undated')],True)
    elif kind=='undated':
        d.text('MONTH / YEAR',24,207,12,'Bold')
        d.line(126,210,516,210)
        d.box(24,229,492,32,d.t.soft)
        for i,label in enumerate(['MON','TUE','WED','THU','FRI','SAT','SUN']):
            d.text(label,24+(i+.5)*492/7,251,11,'Bold',center=True)
        for i in range(8):
            d.line(24+i*492/7,261,24+i*492/7,555)
        for i in range(7):
            d.line(24,261+i*49,516,261+i*49)
        d.panel('FOCUS / PRIORITIES',24,575,240,148)
        d.panel('NOTES / IMPORTANT DATES',276,575,240,148)
        d.paragraph('Reusable monthly base. Add dates by hand. Duplicate pages using your app; PDF links do not retarget themselves to duplicated pages.',24,768,480,16,23)
        d.footer([('GOALS','goals'),('NOTES','notes'),('YEARS','years')])
    elif kind=='month':
        grid_buttons(d,[('CALENDAR','calendar'),('GOALS & PRIORITIES','month-goals'),('HABITS','month-habits'),('FINANCE','month-money'),('REFLECTION','month-reflection'),('WEEK SAMPLE','week')],w=408,h=74)
        d.panel('MONTHLY FOCUS',24,467,408,130)
        d.panel('IMPORTANT DATES',24,611,198,152)
        d.panel('NOTES',234,611,198,152)
        d.paragraph('Sample week: Jan 26–Feb 1. Sample day: Jan 31.',24,800,400,15,22)
        d.footer([('YEAR','year-2026'),('DAY SAMPLE','day'),('NEXT','calendar')],True)
    elif kind=='calendar':
        calendar(d,2026,1,24,196,408,391)
        d.panel('IMPORTANT DATES',24,608,408,114)
        d.panel('NOTES',24,736,408,114)
        d.footer([('MONTH','month'),('WEEK','week'),('NEXT','month-goals')],True)
    elif kind=='month_goals':
        two_panels(d,['MONTHLY GOALS','PRIORITIES','TO DO'],True)
        d.footer([('PREVIOUS','calendar'),('MONTH','month'),('NEXT','month-habits')],True)
    elif kind=='month_habits':
        d.paragraph('Choose up to four habits. Write their names below and mark your own rhythm.',24,210,400,15,22)
        tracker(d,31,y=300)
        d.panel('HABITS 1 / 2 / 3 / 4',24,727,408,123)
        d.footer([('PREVIOUS','month-goals'),('MONTH','month'),('NEXT','month-money')],True)
    elif kind=='month_money':
        d.text('CURRENCY',24,210,12,'Bold'); d.line(95,212,432,212)
        d.table(['CATEGORY','PLAN','ACTUAL'],24,238,408,8,40,[208,100,100])
        d.panel('INCOME / SAVINGS / UPCOMING',24,610,408,130)
        d.panel('NOTES',24,754,408,96)
        d.footer([('PREVIOUS','month-habits'),('MONTH','month'),('NEXT','month-reflection')],True)
    elif kind=='month_reflection':
        two_panels(d,['WHAT WORKED / WHAT I LEARNED','WHAT I WANT TO CHANGE','END OF MONTH REFLECTION'],True)
        d.footer([('PREVIOUS','month-money'),('MONTH','month'),('NEXT','week')],True)
    elif kind=='week':
        for i,day in enumerate(week_dates(date(2026,1,31))):
            d.panel(day.strftime('%A / %d %b').upper(),24,196+i*81,408,73,spacing=26)
        d.paragraph('Continue to the companion page for focus, habits, meals and reflection.',24,795,402,15,22)
        d.footer([('MONTH','month'),('DAY','day'),('NEXT','week-life')],True)
    elif kind=='week_life':
        for i,label in enumerate(['WEEKLY FOCUS','TOP PRIORITIES','TO DO','HABITS','MEAL PLAN','NOTES']):
            d.panel(label,24+(i%2)*210,196+(i//2)*151,198,139)
        d.panel('WEEKLY REFLECTION',24,661,408,189)
        d.footer([('PREVIOUS','week'),('MONTH','month'),('DAY','day')],True)
    elif kind=='day':
        d.panel("TODAY'S FOCUS",24,196,408,85)
        d.panel('TOP 3 PRIORITIES',24,293,198,156)
        d.panel('TO DO',24,461,198,221)
        d.panel('SCHEDULE / TIME BLOCKING',234,293,198,389)
        d.panel('NOTES',24,696,408,154)
        d.footer([('WEEK','week'),('MONTH','month'),('NEXT','day-life')],True)
    elif kind=='day_life':
        for i,label in enumerate(['MEALS','WATER','MOVEMENT','MOOD']):
            d.panel(label,24+(i%2)*210,196+(i//2)*153,198,141)
        d.panel('GRATITUDE',24,514,408,158)
        d.panel('TOMORROW',24,686,408,164)
        d.footer([('PREVIOUS','day'),('WEEK','week'),('MONTH','month')],True)
    elif kind=='goals':
        d.panel('MY GOAL / WHY IT MATTERS',24,196,492,126)
        d.panel('A MEANINGFUL MEASURE OF PROGRESS',24,336,492,100)
        d.table(['ACTION STEP','WHEN','REVIEW'],24,454,492,5,42,[286,103,103])
        d.panel('NEXT SMALL STEP / SUPPORT I NEED',24,722,492,128)
        d.footer([('PRODUCTIVITY','productivity'),('MONTH','month')])
    elif kind=='module':
        key=p['module']
        grid_buttons(d,[(label,f'{key}-{i+1}') for i,(label,_) in enumerate(SAMPLES[key])],h=82)
        d.text('IN THIS EDITION',24,188,10,'Bold',d.t.accent)
        d.text('PLANNED LIBRARY / CONTENT MAP',24,321,12,'Bold',d.t.accent)
        d.paragraph('The list below defines future templates. Only the filled buttons open pages in this edition.',24,349,480,14,20)
        for i,label in enumerate(MODULES[key][1].split('|')):
            col=i%2; row=i//2
            d.text(label,24+col*250,410+row*28,11,'Body')
        if key=='notes':
            grid_buttons(d,[('LINED','lined'),('DOT GRID','dot'),('CORNELL','cornell')],y=606,columns=3)
            d.paragraph('Additional notebook: YOYIR-Notebook-Test.pdf. Ten numbered sections let you write your own titles.',24,735,480,15,23)
        else:
            d.paragraph('Use your own words, numbers and symbols. These pages are for personal organization and handwriting.',24,758,480,15,23)
        d.footer([('INDEX','index'),('GOALS','goals'),('NOTES','notes')])
    elif kind=='template':
        sample_template(d,p['template'])
        d.footer([('MODULE',p['module']),('INDEX','index'),('NOTES','notes')])
    elif kind=='theme':
        keys=list(THEMES); i=keys.index(p['theme'])
        d.text(f'0{i+1} / A COLOR FOR YOUR RHYTHM',24,216,13,'Bold',d.t.accent)
        for j,color in enumerate([d.t.background,d.t.soft,d.t.accent,d.t.ink]):
            d.box(24+j*126,247,114,72,color,stroke=True)
        d.panel('ONE THING TO MAKE SPACE FOR',24,342,492,150)
        d.panel('TODAY / A FEW QUIET NOTES',24,508,492,226)
        d.paragraph('One design system, six palettes. This page is a static theme preview; the generator selects the palette at build time.',24,782,480,15,22)
        d.footer([('PREVIOUS','theme-'+keys[i-1] if i else 'index'),('INDEX','index'),('NEXT','theme-'+keys[i+1] if i<5 else 'cover-01')])
    elif kind=='note':
        notes(d,p['template'])
        d.footer([('NOTES','notes'),('INDEX','index'),('STICKERS','stickers')])
    elif kind=='stickers':
        from reportlab.lib.utils import ImageReader
        from ..config import HEIGHT
        d.paragraph('A small sample of reusable PNG markers. Insert the separate transparent files with your annotation app.',24,206,480,16,23)
        for i,path in enumerate(sticker_files):
            x=24+(i%3)*168; y=291+(i//3)*114
            d.c.drawImage(ImageReader(str(path)),x,HEIGHT-y-90,156,90,mask='auto',preserveAspectRatio=True,anchor='c')
        d.paragraph('The page is a visual reference. These printed shapes are not buttons and do not add stickers when tapped.',24,800,480,15,22)
        d.footer([('INDEX','index'),('NOTES','notes'),('COVERS','cover-01')])
    else:
        raise ValueError(kind)
