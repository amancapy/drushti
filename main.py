from stringgen import *
import random
import docx
from docx.shared import Inches, Pt
from docx.oxml import OxmlElement
from docx.oxml.ns import qn


"""
Variables

indent !
font size
font style
line spacing !
alignment
character spacing
italics !
bold (will hurt readability) !
n. columns
paper darkness
"""


def indent_randomize(doc_):
    sections = doc_.sections
    for section in sections:
        section.top_margin = Inches(random.random() * 2)
        section.bottom_margin = Inches(random.random() * 2)
        section.left_margin = Inches(random.random() * 2)
        section.right_margin = Inches(random.random() * 2)
    return doc_


def add_header_footer(doc_):
    doc_.sections[0].header.paragraphs[0].text = word() * random.choice([0, 1]) + "\t" + word() * random.choice(
        [0, 1]) + "\t" + word() * random.choice([0, 1])
    doc_.sections[0].footer.paragraphs[0].text = word() * random.choice([0, 1]) + "\t" + word() * random.choice(
        [0, 1]) + "\t" + word() * random.choice([0, 1])

    return doc_


def fontsize_randomize(doc_):
    for pgraph in doc_.paragraphs:
        pgraph.style.font.size = Pt(20)
        pgraph.style.font.name = "Gautami"
    return doc_


doc = docx.Document()

doc = indent_randomize(doc)
doc = add_header_footer(doc)

c = chapter(5)
doc.add_heading(c[0][0])


for p in c[1:]:
    pg = doc.add_paragraph()
    if type(p) is not list:
        prun = pg.add_run(p + random.randint(0, 3) * "\n")
    else:
        prun = pg.add_run(p[0] + random.randint(0, 3) * "\n")

    prun.font.name = "Gautami"
    prun.font.size = Pt(15)
    prun.bold = random.random() > 0.8
    prun.italic = random.random() > 0.8
    pg.paragraph_format.line_spacing = Inches((random.random() + 1) / 4)
    pg.alignment = 0 if random.random() > 0.2 else random.choice([1, 2, 3])

    if random.random() < 0.1:
        pg = doc.add_paragraph(("*" + random.randint(1, 5) * " ") * random.randint(2, 7))
        pg.alignment = 1


print(c[1])

# doc.save("temp.docx")
# doc.save("temp2.docx")
#
#
