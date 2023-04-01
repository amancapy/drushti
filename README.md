# drushti
Deep Reading of Scanned Texts with 2D self-attention

Timeline:

28/3: Should have started uploads earlier to leave a footprint, but better late I guess.

Right now I am still working on the data generation part. I think that the model should never learn to recognize real words from the language, so that it can generalize to proper nouns and whatever else it hasn't seen before. Additionally to gather the corpus of real Telugu words is more effort than it's worth, and would have me doing more menial labour than I already have done so far with the XML nightmare: it seems that python-docx can not successfully assign styles to runs of non-ASCII text, so I am having to generate document XMLs from literal scratch. This gives me more low-level control of the text but at the cost of entirely too much coffee and a net day of my life probably.

A lot of progress so far: Documents made of paragraphs made of sentences made of words made of letters are generated probabilistically. Originally I was intent on using regular expressions to generate them, but unfortunately re generators with input probabilities aren't too well documented from what I have seen. Nevertheless. Now what remains is relatively simple. Before the model itself comes in of course.


30/3: Document generation is more or less done. Currently only single-column documents are "supported." I want to see if a model can be learned at all, since the task is fairly ambitious, before dedicating more time to data generation than is necessary. What is left for now is being able to go straight to docx from scratch, then to pdf from docx, or directly to png from docx. A fairly annoying issue is that I don't really know exactly where to cut the text off to have it represent only the first page of the document. Once that is done, what remains is trivial, again before the model itself comes in.


1/4: Document generation is done, generating xmls from scratch and using a preexisting empty document as template. The issue of knowing where to cut off the repr still stands. One idea is simply matching the last word in the document with the preexisting string and cutting it off there. 
