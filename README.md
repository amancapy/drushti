# drushti
Deep Reading of Scanned Texts with 2D self-attention (WIP, far from fruition)

Timeline:


8/4: Still frustratingly stuck on the pdf-png conversion, which will be the final step in being done with the data generation. What's annoying is that I am for now unable to clip the text where the pdf ends because pdf encoding means I can't directly know what the last word in the text is directly. Still I hope it won't be too much trouble this far in.


2/4: Tantalizingly close to being done with generating the data. Current bottleneck is how absurdly slow and inconvenient the docx to pdf to png pipeline is. Hypothesis is that the libreoffice server is being called to life for each conversion, and one would rather convert as a batch as many docx at once as the character limit on termnial commands will allow. This means that there won't be a single continuous pipeline from scratch to png, but a manual stop at docxing first, and so on. Nevertheless once the data part is done (and god willing), I will be allowed to have some fun. THe issue of cutting off the text wrt the first page in the document is very much alive and kicking, and it seems that after the pdfing is done, there will be a small detour to match the last word in the pdf to the repr, cutting them both off there, and moving on. 


1/4: Document generation is done, generating xmls from scratch and using a preexisting empty document as template. The issue of knowing where to cut off the repr still stands. One idea is simply matching the last word in the document with the preexisting string and cutting it off there. 


30/3: Document generation is more or less done. Currently only single-column documents are "supported." I want to see if a model can be learned at all, since the task is fairly ambitious, before dedicating more time to data generation than is necessary. What is left for now is being able to go straight to docx from scratch, then to pdf from docx, or directly to png from docx. A fairly annoying issue is that I don't really know exactly where to cut the text off to have it represent only the first page of the document. Once that is done, what remains is trivial, again before the model itself comes in.


28/3: Should have started uploads earlier to leave a footprint, but better late I guess.

Right now I am still working on the data generation part. I think that the model should never learn to recognize real words from the language, so that it can generalize to proper nouns and whatever else it hasn't seen before. Additionally to gather the corpus of real Telugu words is more effort than it's worth, and would have me doing more menial labour than I already have done so far with the XML nightmare: it seems that python-docx cannot successfully assign styles to runs of non-ASCII text, so I am having to generate document XMLs from literal scratch by trying to imitate manual styling. This gives me more low-level control of the text but at the cost of entirely too much coffee and several net days of my life probably.

A lot of progress so far: Documents made of paragraphs made of sentences made of words made of letters are generated probabilistically. Originally I was intent on using regular expressions to generate them, but unfortunately re generators with input probabilities aren't too well documented from what I have seen. Nevertheless. Now what remains is relatively simple. Before the model itself comes in of course.
