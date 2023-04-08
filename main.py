import asyncio
import os
import time
import zipfile
import shutil
import tqdm
from stringgen import docgen, header_footer_gen
import subprocess as sp
import PyPDF2 as pdf2


"""
Variables

indent !
font size !
font style
line spacing !
alignment !
italics !
bold (will hurt readability) !
n. columns (for future)
paper darkness (comes in post pdf)
"""


PATH = "/home/amankp/drst_saves"


for subdirname in ("docxes", "reprs", "pdfs", "single_page_pdfs", "dev"):
    if not os.path.exists(PATH + "/" + subdirname):
        os.mkdir(PATH + "/" + subdirname)


n_subdirs = 8
# for i in range(n_subdirs):
#     if not os.path.exists(PATH + f"/docxes/subdir{i}"):
#         os.mkdir(PATH + f"/docxes/subdir{i}")
#
#
n_docxs = 1000
# subdir = 0
# for i in tqdm.tqdm(range(n_docxs)):
#     shutil.copy("filing/template.zip", "filing/temptemplate.zip")
#     if not os.path.exists("filing/temp"):
#         os.mkdir("filing/temp")
#
#     docxml, ps = docgen()
#
#     with open(PATH + f"/reprs/repr{i}.txt", "w+") as f:
#         ps = [["".join([w + " " for w in s[:-1]]) + s[-1] for s in p] for p in ps]
#         ps = ["".join([s + " " for s in p[:-1]]) + p[-1] for p in ps]
#         ps = "".join([p + "\n" for p in ps[:-1]]) + ps[-1]
#
#         f.write(ps)
#
#     h, f = header_footer_gen("h"), header_footer_gen("f")
#     for content, fname in zip((docxml, h, f), ("document", "header1", "footer1")):
#         with open(f"filing/temp/{fname}.xml", "w+") as f:
#             f.write(content)
#
#     with zipfile.ZipFile("filing/temptemplate.zip", "a") as z:
#         for fname in "document", "header1", "footer1":
#             z.write(f"filing/temp/{fname}.xml", f"word/{fname}.xml")
#
#     if i % (n_docxs // n_subdirs) == 0 and i:
#         subdir += 1
#
#     shutil.copy("filing/temptemplate.zip", PATH + f"/docxes/subdir{subdir}/doc{i}.docx")
#
#     shutil.rmtree("filing/temp")
#     os.remove("filing/temptemplate.zip")
#
#
# a = time.time()
# null = open(PATH + os.devnull, "w")
# sp.call(" & ".join([f"nohup libreoffice --headless -env:UserInstallation=file:///tmp/test{i} --convert-to pdf {PATH}/docxes/subdir{i}/* --outdir {PATH}/pdfs" for i in range(n_subdirs)]), shell=True, stdout=null)


for i in range(n_docxs):
    print(i)
    with open(PATH + f'/pdfs/doc{i}.pdf', 'rb') as file:
        pdf_reader = pdf2.PdfReader(file)

        pdf_writer = pdf2.PdfWriter()

        pdf_writer.add_page(pdf_reader.pages[0])

        with open(PATH + f'/single_page_pdfs/doc{i}.pdf', 'wb') as output_file:
            pdf_writer.write(output_file)

        with open(PATH + f'/single_page_pdfs/doc{i}.pdf', 'rb') as file:
            text = pdf2.PdfReader(file).pages[0].extract_text()
            print(text)
    exit()