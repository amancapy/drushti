# drushti
Image-Text Pairs for Native Language OCR Models


~~A self-attention model to map image inputs directly to token sequences, for automated, fast digitization of scans of books and documents. The target sequences are designed to train the model to ignore headers, numbering, etc. and focus only on the main text body.~~ (Has been postponed until I have some free time in life; the data however is ready :)

A small (20k) sample of data is available [here!](https://www.kaggle.com/datasets/amancapy/telugu-scans)

--------------------------------

Timeline:

25/4: Squished the last possible bug. Including the stop vowel (*nakaarapollu*) in the vowel pool means that there would be false consonant diacritics added to any letter in the middle of the word. This sometimes results in triple consonant diacritics, when doubles themselves are exceedingly rare, not to mention triples being literally unpronouncable. With that fixed, the data is now perfect, if not for the fact that some of the font styles were lazily designed and misbehave in some alignments. I am letting them stay to account for real documents that may be badly formatted.

That aside, I have a pretty solid idea for what the target tensors should look like. A 5xD tensor where the first row is the base letter, second and third rows are possible consonant diacritics, and fourth is a possible vowel diacritic. The fifth accounts for all non-Telugu characters, including digits. The choice remains whether to one-hot code each row or let them all be dense. From what I have read, indexing the token bank with dense predictions is somewhat expensive, but one-hots would result in very wide target tensors. Exams approach; I will pick this project back up come summer.

15/4: The data is ready. There was a small bug that I missed which I only caught after generating 100k pairs, but after regeneration the data is now perfect to a large degree of confidence.

10/4 (day): Scratch-to-PNG pipeline is complete and faster than I could hope for in my wildest dreams (exaggeration). Now comes a little bit of fun with making the images look like realistic scans with some cv stuff. After which comes the scary part, actually getting started with the model.


10/4: T-1 day for being done with the data generation. With the generous help of libreoffice forum members, finally the "delete everything after first page" is possible with a simple libre macro now. All that remains is to distribute it across user profiles so that cpu can be fully utilized.


8/4: Still frustratingly stuck on the pdf-png conversion, which will be the final step in being done with the data generation. What's annoying is that I am for now unable to clip the text where the pdf ends because pdf encoding means I can't directly know what the last word in the text is. Still I hope it won't be too much trouble this far in.


2/4: Tantalizingly close to being done with generating the data. Current bottleneck is how absurdly slow and inconvenient the docx to pdf to png pipeline is. Hypothesis is that the libreoffice server is being called to life for each conversion, and one would rather convert as a batch as many docx at once as the character limit on termnial commands will allow. This means that there won't be a single continuous pipeline from scratch to png, but a manual stop at docxing first, and so on. Nevertheless once the data part is done (and god willing), I will be allowed to have some fun. The issue of cutting off the text wrt the first page in the document is very much alive, and it seems that after the pdfing is done, there will be a small detour to match the last word in the pdf to the repr, cutting them both off there, and moving on. 


1/4: Document generation is done, generating xmls from scratch and using a preexisting empty document as template. The issue of knowing where to cut off the repr still stands. One idea is simply matching the last word in the document with the preexisting string and cutting it off there. 


30/3: Document generation is more or less done. Currently only single-column documents are "supported." I want to see if a model can be learned at all, since the task is fairly ambitious, before dedicating more time to data generation than is necessary. What is left for now is being able to go straight to docx from scratch, then to pdf from docx, or directly to png from docx. A fairly annoying issue is that I don't really know exactly where to cut the text off to have it represent only the first page of the document. Once that is done, what remains is trivial, again before the model itself comes in.


28/3: Should have started uploads earlier to leave a footprint, but better late I guess. Right now I am still working on the data generation part. I think that the model should never learn to recognize real words from the language, so that it can generalize to proper nouns and whatever else it hasn't seen before. Additionally to gather the corpus of real Telugu words is more effort than it's worth, and would have me doing more menial labour than I already have done so far with the XML nightmare: it seems that python-docx cannot successfully assign styles to runs of non-ASCII text, so I am having to generate document XMLs from literal scratch by trying to imitate manual styling. This gives me more low-level control of the text but at the cost of entirely too much coffee and several net days of my life probably. A lot of progress so far: Documents made of paragraphs made of sentences made of words made of letters are generated probabilistically. Originally I was intent on using regular expressions to generate them, but unfortunately re generators with input probabilities aren't too well documented from what I have seen. Nevertheless. Now what remains is relatively simple. Before the model itself comes in of course.
