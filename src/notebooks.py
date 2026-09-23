from .templates import notes
from .layouts.covers import cover
from .config import NOTEBOOK_TYPES

def notebook_catalog():
    return [{'id':f'notebook-{i+1:02d}','type':kind,'sections':10,
             'templates_per_section':2,'status':'test-generated' if i==0 else 'configured'}
            for i,kind in enumerate(NOTEBOOK_TYPES)]

def notebook_pages(theme='lavender',style='LINED'):
    assert style in NOTEBOOK_TYPES
    base={'LINED':'lined','DOT GRID':'dot','GRID':'grid','BLANK':'blank','STUDY':'study','PROJECT':'project'}[style]
    pages=[dict(id='home',title="YOYI'R NOTEBOOK",kind='cover',theme=theme),
           dict(id='index',title='Ten spaces, your own titles',kind='index',theme=theme)]
    for i in range(1,11):
        pages.append(dict(id=f'section-{i:02d}',title=f'Section {i:02d}',kind='section',theme=theme,section=i))
        for j,template in enumerate([base,'cornell' if style=='STUDY' else 'project']):
            pages.append(dict(id=f'section-{i:02d}-{j+1}',title=f'{i:02d} / {template.title()} notes',kind='note',theme=theme,section=i,template=template))
    return pages

def draw_notebook(d,p):
    if p['kind']=='cover':
        cover(d,3,notebook=True)
        return
    d.header(p['title'],'DIGITAL NOTEBOOK / WRITE YOUR OWN SECTION TITLES',annual=True,notebook=True)
    for i in range(1,11):
        d.button(f'{i:02d}',f'section-{i:02d}',444,24+(i-1)*85,72,76)
    if p['kind']=='index':
        for i in range(1,11):
            x=24+((i-1)%2)*210
            y=196+((i-1)//2)*118
            d.button(f'SECTION {i:02d}',f'section-{i:02d}',x,y,198)
            d.line(x+4,y+99,x+194,y+99)
        d.paragraph('Write a title under each section. Numbered tabs stay fixed. Renaming text and duplicating pages are actions in your app.',24,811,400,13,18)
        d.footer([('OPEN SECTION 01','section-01'),('HOME','home')],True)
    elif p['kind']=='section':
        i=p['section']
        d.text(f'{i:02d}',228,350,130,'Editorial',d.t.soft,True)
        d.text('THIS SECTION IS FOR',228,410,13,'Bold',center=True)
        d.line(66,465,390,465)
        d.panel('IDEAS / CONTENTS',24,515,408,211)
        d.button('WRITING PAGE',f'section-{i:02d}-1',24,760,198)
        d.button('PROJECT NOTES',f'section-{i:02d}-2',234,760,198)
        d.footer([('PREVIOUS',f'section-{i-1:02d}' if i>1 else 'index'),('INDEX','index'),('NEXT',f'section-{i+1:02d}' if i<10 else 'index')],True)
    else:
        i=p['section']
        notes(d,p['template'],w=408)
        other=f'section-{i:02d}-2' if p['id'].endswith('-1') else f'section-{i:02d}-1'
        d.footer([('SECTION',f'section-{i:02d}'),('OTHER PAGE',other),('INDEX','index')],True)
