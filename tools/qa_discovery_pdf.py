"""Audit the generated Discovery PDF and make contact sheets from current renders."""
from pathlib import Path
import collections, importlib.util, json, re, sys, unicodedata
from urllib.parse import urlparse
import pdfplumber
from pypdf import PdfReader
from PIL import Image, ImageDraw
ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'discovery/discovery.md'
PDF=ROOT/'output/pdf/PRODE-discovery-aprobado.pdf'
md=SOURCE.read_text(encoding='utf-8-sig')
revision=re.search(r'\*\*Revisi[oó]n:\*\*\s*(\d+)',md).group(1)
OUT=ROOT/f'output/pdf/previews/revision-{revision}'
OUT.mkdir(parents=True,exist_ok=True)
def norm(s):
    return ' '.join(re.findall(r'\w+',unicodedata.normalize('NFC',s).lower()))
r=PdfReader(str(PDF)); texts=[p.extract_text() or '' for p in r.pages]
joined='\n'.join(texts); normalized=norm(joined)
# Exclude repeated running headers/footers so split paragraphs stay contiguous.
with pdfplumber.open(str(PDF)) as body_pdf:
    source_body='\n'.join(p.crop((0,65,p.width,p.height-62)).extract_text() or '' for p in body_pdf.pages)
source_normalized=norm(source_body)
(OUT/'extracted-text.txt').write_text(joined,encoding='utf-8')
issues=[]
headers=re.findall(r'^#{2,4}\s+(.+)$',md,re.M)
for h in headers:
    if norm(h.replace('**','').replace('`','')) not in normalized: issues.append('Missing heading: '+h)
ids=sorted(set(re.findall(r'\bRN-?\d+\b',md)))
for rule in ids:
    if rule not in joined: issues.append('Missing rule ID: '+rule)
# Compare every rendered source paragraph/cell, independently of page wrapping.
spec=importlib.util.spec_from_file_location('generator',ROOT/'tools/generate_discovery_pdf.py')
g=importlib.util.module_from_spec(spec); spec.loader.exec_module(g); g.register_fonts()
flows=g.parse_markdown(md,g.make_styles(),(210-42)*g.mm)
expected=[]
def collect(f):
    if hasattr(f,'getPlainText'): expected.append(f.getPlainText())
    elif hasattr(f,'_cellvalues'):
        for row in f._cellvalues:
            for cell in row:
                for item in cell if isinstance(cell,(list,tuple)) else [cell]: collect(item)
for f in flows: collect(f)
for n,paragraph in enumerate(expected,1):
    if norm(paragraph) not in normalized and norm(paragraph) not in source_normalized: issues.append(f'Missing source paragraph/cell {n}: {paragraph[:140]}')
links=[]
for n,p in enumerate(r.pages,1):
    if not texts[n-1].strip(): issues.append(f'Empty page: {n}')
    if '\ufffd' in texts[n-1] or '\x00' in texts[n-1]: issues.append(f'Replacement/null glyph page {n}')
    if n>1 and f'/ R{revision} /' not in texts[n-1]: issues.append(f'Revision footer/header missing page {n}')
    for ar in p.get('/Annots',[]):
        a=ar.get_object(); uri=a.get('/A',{}).get('/URI')
        if uri:
            links.append(str(uri)); u=urlparse(uri)
            if u.scheme not in ('http','https') or not u.netloc: issues.append(f'Invalid URI page {n}: {uri}')
        rect=a.get('/Rect')
        if rect:
            x0,y0,x1,y1=map(float,rect); w=float(p.mediabox.width); h=float(p.mediabox.height)
            if not (0<=x0<=x1<=w and 0<=y0<=y1<=h): issues.append(f'Annotation geometry page {n}')
with pdfplumber.open(str(PDF)) as pp:
    for n,p in enumerate(pp.pages,1):
        bad=[c for c in p.chars if c['x0'] < -0.5 or c['x1'] > p.width+0.5 or c['top'] < -0.5 or c['bottom'] > p.height+0.5]
        if bad: issues.append(f'Out-of-page text page {n}: {len(bad)} chars')
if revision=='3' and '19 NOV 2026' not in joined: issues.append('Missing revision-3 update date 19 NOV 2026')
source_urls=set(re.findall(r'https?://[^\s<>)]*',md))
for url in source_urls:
    url=url.rstrip('.,;')
    if url not in links: issues.append('Missing source URL annotation: '+url)
report={'revision':revision,'pages':len(r.pages),'links':len(links),'unique_links':len(set(links)),'headings_checked':len(headers),'rule_ids':ids,'source_paragraphs_cells_checked':len(expected),'source_urls_checked':len(source_urls),'issues':issues,'visual_inspected':False}
(OUT/'qa-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
files=sorted(OUT.glob('page-*.png'))
if files:
    for offset in range(0,len(files),4):
        batch=files[offset:offset+4]; sheet=Image.new('RGB',(1240,1800),'#DDE3E8'); draw=ImageDraw.Draw(sheet)
        for i,path in enumerate(batch):
            im=Image.open(path).convert('RGB'); im.thumbnail((600,840))
            x=(i%2)*620+(620-im.width)//2; y=(i//2)*900+35
            sheet.paste(im,(x,y)); draw.text(((i%2)*620+22,(i//2)*900+12),f'Page {offset+i+1}',fill='#162B40')
        sheet.save(OUT/f'contact-{offset//4+1:02}.png')
print(json.dumps(report,ensure_ascii=False,indent=2))
if issues: sys.exit(1)
