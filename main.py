import os
import time
import zipfile
import shutil
import tqdm
from stringgen import docgen, header_footer_gen
import subprocess as sp
from distutils.dir_util import copy_tree
import docx


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
paper darkness (comes in post png)
"""


PATH = "/home/amankp/drst"
n_docxs = 1000


if not os.path.exists(PATH):
    os.mkdir(PATH)


for subdirname in ("docxes", "dev", "texts", "pngs"):
    if not os.path.exists(PATH + "/" + subdirname):
        os.mkdir(PATH + "/" + subdirname)
null = open(PATH + os.devnull, "w")


n_workers = 8
for i in range(n_workers):
    if not os.path.exists(PATH + f"/docxes/{i}"):
        os.mkdir(PATH + f"/docxes/{i}")

for i in range(n_workers):
    if not os.path.exists(f"/home/amankp/.config/libreoffice/user{i}"):
        copy_tree("/home/amankp/.config/libreoffice/4", f"/home/amankp/.config/libreoffice/workers/user{i}")


def to_docx():
    subdir = 0
    for i in tqdm.tqdm(range(n_docxs)):
        if i % (n_docxs // n_workers) == 0 and i:
            subdir += 1

        shutil.copy("filing/template.zip", "filing/temptemplate.zip")
        if not os.path.exists("filing/temp"):
            os.mkdir("filing/temp")

        docxml, ps = docgen()

        h, f = header_footer_gen("h"), header_footer_gen("f")
        for content, fname in zip((docxml, h, f), ("document", "header1", "footer1")):
            with open(f"filing/temp/{fname}.xml", "w+") as f:
                f.write(content)

        with zipfile.ZipFile("filing/temptemplate.zip", "a") as z:
            for fname in "document", "header1", "footer1":
                z.write(f"filing/temp/{fname}.xml", f"word/{fname}.xml")

        shutil.copy("filing/temptemplate.zip", PATH + f"/docxes/{subdir}/doc{i}.docx")

        shutil.rmtree("filing/temp")
        os.remove("filing/temptemplate.zip")

    breaks = range(0, n_docxs + 1, n_docxs // n_workers)

    clip_cmd = " & ".join([
        f'libreoffice --nologo --nofirststartwizard --invisible'
        f' -env:UserInstallation=file:///home/amankp/.config/libreoffice/workers/user{j}'
        f' "macro:///Standard.Module1.del({breaks[j]}, {breaks[j+1]}, {j})"'
        for j in range(n_workers)])

    a = time.time()
    sp.call(clip_cmd, shell=True, stdout=null)
    print(time.time() - a)


def to_png_and_text():
    for i in range(n_workers):
        for j in range((n_docxs // n_workers) * i, (n_docxs // n_workers) * (i + 1)):
            doc = docx.Document(PATH + f"/docxes/{i}/doc{j}.docx")
            text = " ".join([p.text for p in doc.paragraphs])

            with open(PATH + f"/texts/{j}.txt", "w+") as f:
                f.write(text)
                f.close()

    cvt_cmd = " & ".join([f'libreoffice --nologo --nofirststartwizard --headless --invisible -env:UserInstallation=file:///home/amankp/.config/libreoffice/workers/user{i} --convert-to png {PATH}/docxes/{i}/* --outdir {PATH}/pngs' for i in range(n_workers)])
    sp.call(cvt_cmd, shell=True, stdout=null)


# to_docx()
to_png_and_text()