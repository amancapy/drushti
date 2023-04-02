import asyncio
import os
import zipfile
import shutil
from stringgen import docgen, header_footer_gen
import subprocess as sp


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


if not os.path.exists("filing/docxes"):
    os.mkdir("filing/docxes")
if not os.path.exists("filing/reprs"):
    os.mkdir("filing/reprs")


for i in range(1000000):
    if i % 1000 == 0:
        print(i)
    shutil.copy("filing/template.zip", "filing/temptemplate.zip")
    if not os.path.exists("filing/temp"):
        os.mkdir("filing/temp")

    docxml, ps = docgen()
    h, f = header_footer_gen("h"), header_footer_gen("f")

    with open(f"filing/reprs/repr{i}.txt", "w+") as f:
        ps = [["".join([w + " " for w in s[:-1]]) + s[-1] for s in p] for p in ps]
        ps = ["".join([s + " " for s in p[:-1]]) + p[-1] for p in ps]
        ps = "".join([p + "\n" for p in ps[:-1]]) + ps[-1]

        f.write(ps)
        f.close()

    for content, fname in zip((docxml, h, f), ("document", "header1", "footer1")):
        with open(f"filing/temp/{fname}.xml", "w") as f:
            f.write(content)

    with zipfile.ZipFile("filing/temptemplate.zip", "a") as z:
        for fname in "document", "header1", "footer1":
            z.write(f"filing/temp/{fname}.xml", f"word/{fname}.xml")

    shutil.copy("filing/temptemplate.zip", f"filing/docxes/doc{i}.docx")

    shutil.rmtree("filing/temp")
    os.remove("filing/temptemplate.zip")
