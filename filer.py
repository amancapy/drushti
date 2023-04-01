import os
import zipfile
import shutil
from stringgen import docgen, header_footer_gen


shutil.copy("filing/template.zip", "filing/temptemplate.zip")
if not os.path.exists("filing/temp"):
    os.mkdir("filing/temp")


for content, fname in zip((docgen()[0], header_footer_gen("h"), header_footer_gen("f")), ("document", "header1", "footer1")):
    with open(f"filing/temp/{fname}.xml", "w") as f:
        f.write(content)


with zipfile.ZipFile("filing/temptemplate.zip", "a") as z:
    for fname in "document", "header1", "footer1":
        z.write(f"filing/temp/{fname}.xml", f"word/{fname}.xml")


shutil.copy("filing/temptemplate.zip", "filing/fin.docx")


shutil.rmtree("filing/temp")
os.remove("filing/temptemplate.zip")