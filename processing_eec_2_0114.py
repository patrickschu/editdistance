import emodcorpustools as emo
import re
import codecs
import os

"""
delete all the terrible annotations from eec
while were at it, replace \n in metadata
"""

annotationregex=re.compile("\n(AUTHOR|LETTER|RECIPIENT)(:.+){5}.*")
smallannotationregex=re.compile("[A-Z]*\,(\d+.){3}")
metaregex=re.compile("<file>.*?<text>", re.DOTALL)
textregex=re.compile("<text>(.*?)</text>", re.DOTALL)

def metacleaner (input_dir):
	for fili in [i for i in os.listdir(input_dir) if not i.startswith(".")]:
		#print fili
		with codecs.open(os.path.join(input_dir, fili), "r", "utf-8") as inputfile:
			inputtext = inputfile.read()
		meta=metaregex.findall(inputtext)[0]
		#if len(meta) != 1:
		#	print fili, "watch out, meta too long or short: it is {}".format(len(meta))
		text= textregex.findall(inputtext)[0]
		if len(text) != 1:
			print fili, "watch out, text too long"
		text= annotationregex.sub(" ", text)
		text= smallannotationregex.sub("", text)
		with codecs.open(os.path.join("eecprocessed", fili), "w", "utf-8") as outputfile:
			outputfile.write(meta+text+"</text> </file>")
		print "written to", outputfile
			

metacleaner('/Users/ps22344/Downloads/editdistance/extracted_corpora/eec_extracted')




		