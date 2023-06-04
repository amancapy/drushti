import os
import time
import zipfile
import shutil
import tqdm
from stringgen import docgen, header_footer_gen
import subprocess as sp
from distutils.dir_util import copy_tree
import docx
from multiprocessing import Pool


"""
Variables (! = done)

indent !
font size !
font style
line spacing !
alignment !
italics !
bold (will hurt readability) !
n. columns (for future)
"""


PATH = "/home/amankp/drst"
n_docxs = 100000
n_subdirs = 32

if not os.path.exists(PATH):
    os.mkdir(PATH)


for subdirname in ("docxes", "dev", "texts", "pngs"):
    if not os.path.exists(PATH + "/" + subdirname):
        os.mkdir(PATH + "/" + subdirname)
null = open(PATH + os.devnull, "w")


for i in range(n_subdirs):
    if not os.path.exists(PATH + f"/docxes/{i}"):
        os.mkdir(PATH + f"/docxes/{i}")


if os.path.exists("/home/amankp/.config/libreoffice/workers"):
    shutil.rmtree("/home/amankp/.config/libreoffice/workers")
os.mkdir("/home/amankp/.config/libreoffice/workers")

for i in range(8):
    copy_tree("/home/amankp/.config/libreoffice/4", f"/home/amankp/.config/libreoffice/workers/user{i}")


def to_docx_subdir(args):
    start, end, subdir = args

    for i in tqdm.tqdm(range(start, end)):
        shutil.copy("template.zip", f"filing/temptemplate{subdir}.zip")
        if not os.path.exists(f"filing/temp{subdir}"):
            os.mkdir(f"filing/temp{subdir}")

        docxml, ps = docgen()

        h, f = header_footer_gen("h"), header_footer_gen("f")
        for content, fname in zip((docxml, h, f), ("document", "header1", "footer1")):
            with open(f"filing/temp{subdir}/{fname}.xml", "w+") as f:
                f.write(content)

        with zipfile.ZipFile(f"filing/temptemplate{subdir}.zip", "a") as z:
            for fname in "document", "header1", "footer1":
                z.write(f"filing/temp{subdir}/{fname}.xml", f"word/{fname}.xml")

        shutil.copy(f"filing/temptemplate{subdir}.zip", PATH + f"/docxes/{subdir}/doc{i}.docx")

        shutil.rmtree(f"filing/temp{subdir}")
        os.remove(f"filing/temptemplate{subdir}.zip")


def to_docx():
    breaks = range(0, n_docxs + 1, (n_docxs // n_subdirs))

    args = [(breaks[i], breaks[i+1], i) for i in range(n_subdirs)]

    for chunk in chunks(args, 8):
        pool = Pool(processes=8)
        pool.map(to_docx_subdir, chunk)
        pool.close()

    for i in range(0, n_subdirs, 8):
        clip_cmd = " & ".join([
            f'soffice --nologo --nofirststartwizard --norestore'
            f' -env:UserInstallation=file:///home/amankp/.config/libreoffice/workers/user{j}'
            f' "macro:///Standard.Module1.del({breaks[j] + i * n_docxs // n_subdirs}, {breaks[j + 1] + i * n_docxs // n_subdirs}, {i + j})"'
            for j in range(8)])

        a = time.time()
        print(clip_cmd)
        sp.call(clip_cmd, shell=True, stdout=null)
        print(time.time() - a)

        time.sleep(570)
        sp.call("killall soffice.bin", shell=True)
        time.sleep(30)

    for i in range(n_subdirs):
        for j in range(i * (n_docxs // n_subdirs), (i + 1) * (n_docxs // n_subdirs)):
            os.rename(f"{PATH}/docxes/{i}/doc{j}.docx", f"{PATH}/docxes/doc{j}.docx")

    for i in range(n_docxs // 100):
        if not os.path.exists(PATH + f"/docxes/{i}"):
            os.mkdir(PATH + f"/docxes/{i}")

        for j in range(i * 100, (i + 1) * 100):
            os.rename(f"{PATH}/docxes/doc{j}.docx", f"{PATH}/docxes/{i}/doc{j}.docx")


def to_text_subdir(args):
    subdir, start, end = args
    for j in tqdm.tqdm(range(start, end)):
        doc = docx.Document(PATH + f"/docxes/{subdir}/doc{j}.docx")
        text = "\n".join([p.text for p in doc.paragraphs])

        with open(PATH + f"/texts/{j}.txt", "w+") as f:
            f.write(text)
            f.close()


def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def to_text_and_png():
    args = [(i, 100 * i, 100 * (i+1)) for i in range(n_docxs // 100)]

    for chunk in chunks(args, 8):
        pool = Pool(processes=8)
        pool.map(to_text_subdir, chunk)
        pool.close()

    for i in range(0, n_docxs // 100, 8):
        clip_cmd = " & ".join(
            [f'libreoffice --nologo --nofirststartwizard --headless --norestore'
             f' -env:UserInstallation=file:///home/amankp/.config/libreoffice/workers/user{j}'
             f' --convert-to png --outdir {PATH}/pngs {PATH}/docxes/{i+j}/*' for j in range(8)]
        )
        print(clip_cmd)

        a = time.time()
        sp.call(clip_cmd, shell=True, stdout=null)
        print(time.time() - a)

        time.sleep(10)
        sp.call("killall soffice.bin", shell=True)
        time.sleep(5)


# to_docx()
to_text_and_png()
