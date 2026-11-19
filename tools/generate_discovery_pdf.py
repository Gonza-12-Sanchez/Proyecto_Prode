"""Build the approved PRODE Discovery PDF from its canonical Markdown source.

Run with the bundled Python runtime (ReportLab and pypdf required).
The PDF is a document preview, not an approved product design system.
"""
from __future__ import annotations

import argparse
import html
import re
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate, Frame, HRFlowable, KeepTogether, PageBreak, PageTemplate,
    Paragraph, Spacer, Table, TableStyle,
)
from reportlab.platypus.tableofcontents import TableOfContents

ROOT = Path(__file__).resolve().parents[1]
NAVY = colors.HexColor("#162B40")
INK = colors.HexColor("#263646")
MUTED = colors.HexColor("#617181")
TEAL = colors.HexColor("#126F70")
PALE = colors.HexColor("#EFF5F5")
LINE = colors.HexColor("#D8E2E7")
GOLD = colors.HexColor("#D6A558")


def register_fonts():
    fonts = Path("C:/Windows/Fonts")
    for name, filename in [("Body", "arial.ttf"), ("Body-Bold", "arialbd.ttf"),
                           ("Body-Italic", "ariali.ttf"), ("Body-BoldItalic", "arialbi.ttf")]:
        pdfmetrics.registerFont(TTFont(name, str(fonts / filename)))
    pdfmetrics.registerFontFamily("Body", normal="Body", bold="Body-Bold",
                                 italic="Body-Italic", boldItalic="Body-BoldItalic")


def make_styles():
    base = dict(fontName="Body", textColor=INK, fontSize=10, leading=14.5,
                spaceAfter=7, splitLongWords=True, allowWidows=0, allowOrphans=0)
    return {
        "body": ParagraphStyle("BodyTextCustom", **base),
        "small": ParagraphStyle("Small", **{**base, "fontSize": 8.4, "leading": 11.5}),
        "table": ParagraphStyle("Table", **{**base, "fontSize": 8.5, "leading": 11.5, "spaceAfter": 0}),
        "th": ParagraphStyle("TableHead", **{**base, "fontName": "Body-Bold", "fontSize": 8.5, "leading": 11.5,
                                               "textColor": colors.white, "spaceAfter": 0}),
        "h1": ParagraphStyle("Section", fontName="Body-Bold", fontSize=17,
                               leading=21, textColor=NAVY, spaceBefore=16,
                               spaceAfter=10, keepWithNext=True),
        "h2": ParagraphStyle("Subsection", fontName="Body-Bold", fontSize=11.5,
                               leading=15, textColor=TEAL, spaceBefore=11,
                               spaceAfter=6, keepWithNext=True),
        "h3": ParagraphStyle("Subsubsection", fontName="Body-Bold", fontSize=10,
                               leading=14, textColor=NAVY, spaceBefore=8,
                               spaceAfter=5, keepWithNext=True),
        "bullet": ParagraphStyle("BulletCustom", **{**base, "leftIndent": 12, "firstLineIndent": -9,
                                                     "spaceAfter": 4}),
        "quote": ParagraphStyle("Quote", **{**base, "backColor": PALE, "borderPadding": 10,
                                             "spaceBefore": 5, "spaceAfter": 10}),
        "toc": ParagraphStyle("ContentsEntry", fontName="Body", fontSize=9.2,
                                leading=13, textColor=INK, leftIndent=0,
                                firstLineIndent=0, spaceBefore=2),
    }


def inline(text: str) -> str:
    text = text.replace("\u2011", "-").replace("\u2013", "-").replace("\u2014", "-")
    text = html.escape(text)
    text = re.sub(r"\[([^\]]+)\]\((https?://[^\s)]+)\)",
                  r'<a href="\2" color="#126F70"><u>\1</u></a>', text)
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r"\1", text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"`([^`]+)`", r'<font color="#126F70">\1</font>', text)
    # Link bare external references, keeping XML syntax untouched.
    if "<a " not in text:
        def link_url(match):
            raw = match.group(1)
            url = raw.rstrip(".,;")
            suffix = raw[len(url):]
            return f'<a href="{url}" color="#126F70">{url}</a>{suffix}'
        text = re.sub(r"(https?://[^\s<]+)", link_url, text)
    return text


class DiscoveryDoc(BaseDocTemplate):
    def __init__(self, filename, revision="2", updated_label="18 NOV 2026", **kwargs):
        self.revision = revision
        self.updated_label = updated_label
        super().__init__(str(filename), pagesize=A4, leftMargin=21*mm,
                         rightMargin=21*mm, topMargin=23*mm, bottomMargin=22*mm,
                         title="PRODE - Discovery aprobado", author="PRODE",
                         subject="Producto, reglas, stack, autenticación Google, despliegue y mantenimiento", **kwargs)
        frame = Frame(self.leftMargin, self.bottomMargin, self.width, self.height,
                      leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
        self.addPageTemplates(PageTemplate(id="main", frames=[frame], onPage=self.decorate))
        self.heading_count = 0

    def beforeDocument(self):
        self.heading_count = 0

    def decorate(self, canvas, doc):
        canvas.saveState()
        w, h = A4
        if doc.page > 1:
            canvas.setStrokeColor(LINE)
            canvas.line(self.leftMargin, h-15.5*mm, w-self.rightMargin, h-15.5*mm)
            canvas.setFont("Body-Bold", 8)
            canvas.setFillColor(NAVY)
            canvas.drawString(self.leftMargin, h-12*mm, "PRODE")
            canvas.setFont("Body", 8)
            canvas.setFillColor(MUTED)
            canvas.drawRightString(w-self.rightMargin, h-12*mm, f"DISCOVERY APROBADO / R{self.revision} / ACT {self.updated_label}")
        canvas.setStrokeColor(LINE)
        canvas.line(self.leftMargin, 16.5*mm, w-self.rightMargin, 16.5*mm)
        canvas.setFont("Body", 7.5)
        canvas.setFillColor(MUTED)
        canvas.drawString(self.leftMargin, 12*mm, "Fundación en curso | Decisiones confirmadas y asuntos abiertos")
        canvas.drawRightString(w-self.rightMargin, 12*mm, str(doc.page))
        canvas.restoreState()

    def afterFlowable(self, flowable):
        if isinstance(flowable, Paragraph) and flowable.style.name == "Section":
            text = flowable.getPlainText()
            if text == "Contenido":
                return
            self.heading_count += 1
            key = f"section-{self.heading_count}"
            self.canv.bookmarkPage(key)
            self.canv.addOutlineEntry(text, key, level=0, closed=False)
            self.notify("TOCEntry", (0, text, self.page, key))


def table_from(lines, styles, width):
    rows = []
    for line in lines:
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if all(re.fullmatch(r":?-{2,}:?", cell.replace(" ", "")) for cell in cells):
            continue
        rows.append(cells)
    cols = max(map(len, rows))
    rows = [r + [""]*(cols-len(r)) for r in rows]
    if cols == 2:
        weights = [0.13, 0.87] if rows[0][0] == "ID" else [0.29, 0.71]
    elif cols == 3:
        weights = [0.22, 0.38, 0.40]
    elif cols == 4:
        weights = [0.18, 0.28, 0.22, 0.32]
    else:
        weights = [1/cols]*cols
    data = [[Paragraph(inline(cell), styles["th" if idx == 0 else "table"])
             for cell in row] for idx, row in enumerate(rows)]
    row_padding = 5 if rows[0][0] == "ID" else 7
    table = Table(data, colWidths=[width*x for x in weights], repeatRows=1,
                  hAlign="LEFT", spaceBefore=5, spaceAfter=11)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 7),
        ("RIGHTPADDING", (0, 0), (-1, -1), 7),
        ("TOPPADDING", (0, 0), (-1, -1), row_padding),
        ("BOTTOMPADDING", (0, 0), (-1, -1), row_padding),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F3F6F8")]),
        ("LINEBELOW", (0, 0), (-1, 0), 0.7, NAVY),
        ("LINEBELOW", (0, 1), (-1, -1), 0.3, LINE),
    ]))
    return table


def parse_markdown(text, styles, width):
    out = []
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if not line or line == "---":
            i += 1
            continue
        if line.startswith("```"):
            language = line.strip("`").strip()
            block = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith("```"):
                block.append(lines[i].rstrip())
                i += 1
            i += 1
            if language == "mermaid":
                # Convert a simple architecture graph into a readable responsibility flow.
                labels = re.findall(r"[A-Za-z][A-Za-z0-9_]*\[(?:\()?([^^\]\n]+?)\](?:\))?", "\n".join(block))
                labels = list(dict.fromkeys(label.strip('()"') for label in labels))
                description = " / ".join(labels) if labels else "Cliente web o móvil, API FastAPI y PostgreSQL."
                out.append(Paragraph("<b>Esquema de componentes</b><br/>" + inline(description), styles["quote"]))
            else:
                for code_line in block:
                    if code_line.strip():
                        out.append(Paragraph(inline(code_line.strip()), styles["small"]))
            continue
        if line.startswith("# "):
            i += 1
            continue
        if line.startswith("|"):
            block = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                block.append(lines[i])
                i += 1
            out.append(table_from(block, styles, width))
            continue
        heading = re.match(r"^(#{2,4})\s+(.*)$", line)
        if heading:
            level = len(heading.group(1))-1
            title = heading.group(2)
            if level == 1 and (title.startswith("Anexo") or title.startswith("12. ")):
                out.append(PageBreak())
            out.append(Paragraph(inline(title), styles[f"h{level}"]))
            i += 1
            continue
        bullet = re.match(r"^([-*]|\d+\.)\s+(.*)$", line)
        if bullet:
            mark = "-" if bullet.group(1) in ["-", "*"] else bullet.group(1)
            content = bullet.group(2)
            i += 1
            while i < len(lines) and lines[i].strip() and lines[i].startswith("  "):
                content += " " + lines[i].strip()
                i += 1
            out.append(Paragraph(f"{mark} {inline(content)}", styles["bullet"]))
            continue
        if line.startswith(">"):
            out.append(Paragraph(inline(line.lstrip("> ")), styles["quote"]))
            i += 1
            continue
        para = [line]
        i += 1
        while i < len(lines) and lines[i].strip() and not re.match(r"^(#|\||>|[-*] |\d+\. )", lines[i].strip()):
            para.append(lines[i].strip())
            i += 1
        out.append(Paragraph(inline(" ".join(para)), styles["body"]))
    return out


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, default=ROOT / "discovery/discovery.md")
    parser.add_argument("--output", type=Path, default=ROOT / "output/pdf/PRODE-discovery-aprobado.pdf")
    args = parser.parse_args()
    register_fonts()
    styles = make_styles()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    source = args.source.read_text(encoding="utf-8-sig")
    revision_match = re.search(r"\*\*Revisi[oó]n:\*\*\s*(\d+)", source)
    revision = revision_match.group(1) if revision_match else "2"
    date_match = re.search(r"\*\*(?:[UÚ]ltima actualizaci[oó]n|Actualizaci[oó]n|Fecha de actualizaci[oó]n):\*\*\s*([^\n]+)", source)
    updated = date_match.group(1).strip() if date_match else "18 de noviembre de 2026"
    compact_date = updated.replace(" de noviembre de ", " NOV ").replace(" de noviembre ", " NOV ")
    doc = DiscoveryDoc(args.output, revision=revision, updated_label=compact_date.upper())
    cover_kicker = ParagraphStyle("Kicker", fontName="Body-Bold", fontSize=10, leading=14,
                                  textColor=TEAL, spaceAfter=20)
    cover_title = ParagraphStyle("Cover", fontName="Body-Bold", fontSize=48, leading=54,
                                 textColor=NAVY, spaceAfter=18)
    cover_subtitle = ParagraphStyle("Subtitle", fontName="Body", fontSize=23, leading=29,
                                    textColor=NAVY, spaceAfter=20)
    cover_desc = ParagraphStyle("CoverDescription", fontName="Body", fontSize=13, leading=20,
                               textColor=MUTED, spaceAfter=17)
    story = [Spacer(1, 30*mm), Paragraph("PRODUCTO / ESTRATEGIA / OPERACIÓN", cover_kicker),
             Paragraph("PRODE", cover_title), Paragraph("Discovery aprobado", cover_subtitle),
             HRFlowable(width="18%", thickness=3, color=GOLD, hAlign="LEFT", spaceAfter=25),
             Paragraph("Una plataforma para pronosticar fútbol con amigos, con evolución hacia empresas y suscripciones.", cover_desc),
             Spacer(1, 8*mm),
             Paragraph("<b>Primera etapa</b><br/>MVP web móvil gratuito, jugable con amigos.", styles["quote"]),
             Paragraph("<b>Base tecnológica confirmada</b><br/>React + TypeScript + Vite / FastAPI / PostgreSQL", styles["quote"]),
             Paragraph("<b>Acceso del MVP</b><br/>Sólo Google, gestionado por Supabase Auth. Sin correo y contraseña de PRODE.", styles["quote"]),
             Spacer(1, 12*mm), Paragraph(f"Actualizado: {updated} · Revisión {revision}", styles["body"]),
             Paragraph("Estado: Discovery aprobado por el usuario. La fundación continúa; la Knowledge Base, el diseño y el roadmap se elaborarán en las siguientes fases.", styles["small"]),
             PageBreak(), Paragraph("Contenido", styles["h1"])]
    toc = TableOfContents()
    toc.levelStyles = [styles["toc"]]
    toc.dotsMinLevel = 0
    story += [toc, Spacer(1, 12*mm), Paragraph("Cómo leer este documento", styles["h2"]),
              Paragraph("Las decisiones confirmadas describen lo acordado. Las propuestas y preguntas abiertas se mantienen identificadas para evitar convertirlas en compromisos. Los ejemplos de proveedores son alternativas, no servicios contratados.", styles["body"]),
              PageBreak()]
    story.extend(parse_markdown(source, styles, doc.width))
    doc.multiBuild(story)
    from pypdf import PdfReader
    reader = PdfReader(str(args.output))
    print(f"PDF: {args.output}")
    print(f"Pages: {len(reader.pages)}")
    print(f"External links: {sum(1 for p in reader.pages for a in p.get('/Annots', []) if a.get_object().get('/A', {}).get('/URI'))}")


if __name__ == "__main__":
    main()
