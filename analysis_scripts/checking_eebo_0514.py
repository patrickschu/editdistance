import emodcorpustools as emo
import os
import codecs
import json
import random

input_dir= '/home/ps22344/Downloads/eebo'
output_file= 'fulltext_0514'

dicti= {}
print "we working with {} files".format(len([i for i in os.listdir(input_dir) if not i.startswith(".")]))

variable = 'genre1'

#for fili in random.sample([i for i in os.listdir(input_dir) if not i.startswith(".")],1000)
for fili in [i for i in os.listdir(input_dir) if not i.startswith(".")]:
	t= emo.CorpusText(os.path.join(input_dir,fili))
	#titles
	#if len(t.meta['title']) < 5:
	#	print "***\n", fili, '\n', t.meta['title']
	#	dicti[fili]= t.meta['title']
	#pubdate
	#t= emo.CorpusText(os.path.join(input_dir,fili))
	#if len(t.cleantext) < 400:
	#if len(t.meta[variable]) < 1:
	#print "***\n", fili, '\n', t.meta[variable]
	#	dicti[fili]= t.cleantext	
	#	print "***\n", fili, '\n', t.cleantext
	#tokens= t.tokenizer(cleantext=True)
	if len(t.fulltext) < 3:
		print  "***\n", fili, '\n', t.fulltext
		dicti[fili]= t.fulltext
		
		
with codecs.open(output_file, "w", "utf-8") as writeout:
	json.dump(dicti, writeout)


#no major issues with titles though some are long
#no crazy short (< 3) titles
#overly long pubdates very limited
#no crazy short ones either, they look good, just a few ?s and Latin numerals
#there are no genres
#the texts in problemtexts are probably just titles
#empty texts (tokenized) in tokenized_0514 , empty text (string) in 'fulltext_0514': these are the same ones presumably. 91 files. 
