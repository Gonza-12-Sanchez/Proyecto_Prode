from pathlib import Path
import json,re
from pypdf import PdfReader
import pdfplumber
from PIL import Image,ImageOps,ImageDraw
ROOT=Path(__file__).resolve().parents[2]
PDF=ROOT/'output/pdf/PRODE-discovery-aprobado.pdf'
PRE=ROOT/'output/pdf/previews/revision-2'
PRE.mkdir(parents=True,exist_ok=True)
reader=PdfReader(PDF)
texts=[p.extract_text() or '' for p in reader.pages]
all_text='\n'.join(texts)
issues=[]
links=[]
for p in reader.pages:
    for a in p.get('/Annots',[]):
        obj=a.get_object()
        action=obj.get('/A',{})
        if action.get('/URI'): links.append(str(action['/URI']))
with pdfplumber.open(PDF) as pdf:
    for i,p in enumerate(pdf.pages,1):
        for w in p.extract_words():
            if w['x0'] < -1 or w['x1'] > p.width+1 or w['top'] < -1 or w['bottom'] > p.height+1:
                issues.append({'page':i,'kind':'out_of_page','text':w['text']})
        if len(p.extract_text() or '') < 120:
            issues.append({'page':i,'kind':'nearly_empty_page'})
rule_ids=sorted(set(int(x) for x in re.findall(r'RN[-\s]*(\d\d)',all_text)))
missing_rules=[n for n in range(1,19) if n not in rule_ids]
if missing_rules: issues.append({'kind':'missing_rules','ids':missing_rules})
required=['Google','Supabase Auth','Cloudflare','Render','Neon','SQLite','PostgreSQL','mantenimiento','Docker','Full Stack Open','FastAPI','Vite']
missing_terms=[s for s in required if s.casefold() not in all_text.casefold()]
if missing_terms: issues.append({'kind':'missing_terms','terms':missing_terms})
if '\ufffd' in all_text: issues.append({'kind':'replacement_chars'})
if 'flowchart LR' in all_text or '```mermaid' in all_text: issues.append({'kind':'raw_mermaid'})
bad_links=[x for x in links if x.endswith(('.',',',';'))]
if bad_links: issues.append({'kind':'bad_link_punctuation','links':bad_links})
if 'Revisión 2' not in all_text: issues.append({'kind':'revision_metadata_missing'})
source=(ROOT/'discovery/discovery.md').read_text(encoding='utf-8-sig')
headings=re.findall(r'^##\s+(.+)$',source,re.M)
def norm(s): return re.sub(r'\s+',' ',s).strip()
missing_headings=[h for h in headings if norm(h) not in norm(all_text)]
if missing_headings: issues.append({'kind':'missing_headings','headings':missing_headings})
report={'revision':2,'pdf':str(PDF),'pages':len(reader.pages),'issues':issues,'rule_ids':rule_ids,'required_terms':{s:s.casefold() in all_text.casefold() for s in required},'outline_entries':len(reader.outline),'links':links,'unique_links':len(set(links)),'page_chars':[(i+1,len(t)) for i,t in enumerate(texts)],'section_pages':{h:next((i+1 for i,t in enumerate(texts) if i >= 2 and norm(h) in norm(t)),None) for h in headings},'feature_pages':{s:[i+1 for i,t in enumerate(texts) if s.casefold() in t.casefold()] for s in ['autenticación','Google','despliegue','SQLite','mantenimiento']}}
(PRE/'qa-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
(ROOT/'output/pdf/previews/qa-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
(PRE/'text-extracted.txt').write_text(all_text,encoding='utf-8')
images=sorted(PRE.glob('page-*.png'))
for start in range(0,len(images),4):
    sheet=Image.new('RGB',(1260,1820),'#dbe3e8')
    draw=ImageDraw.Draw(sheet)
    for j,path in enumerate(images[start:start+4]):
        im=Image.open(path).convert('RGB')
        im.thumbnail((610,860))
        x=15+(j%2)*630;y=30+(j//2)*910
        draw.text((x,y-20),path.stem,fill='#203345')
        sheet.paste(im,(x,y))
    sheet.save(PRE/f'contact-{start//4+1}.png')
print(json.dumps({k:report[k] for k in ['pages','issues','outline_entries','unique_links','section_pages','feature_pages']},ensure_ascii=False,indent=2))
