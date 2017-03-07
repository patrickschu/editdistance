import emodcorpustools as emo
import re
import codecs
import os

"""
THIS IS IN ADDITION TO ~/Downloads/editdistance/processing_EEC_1206.py, NOT REPLACING IT
It goes like this
1.~/Downloads/editdistance/processing_EEC_1206.py
2. Extracting text
3. processing_eec_2_0114 (self)
delete all the terrible annotations from eec
while were at it, replace \n in metadata
"""

annotationregex=re.compile("\n(AUTHOR|LETTER|RECIPIENT)(:.+){5}.*")
smallannotationregex=re.compile("[A-Z]*\,([A-Z]{,2}\,)?(\d+\.?){3}")
metaregex=re.compile("<file>.*?<text>", re.DOTALL)
textregex=re.compile("<text>(.*?)</text>", re.DOTALL)

def metacleaner (input_dir):
	for fili in [i for i in os.listdir(input_dir) if not i.startswith(".")]:
		print fili
		with codecs.open(os.path.join(input_dir, fili), "r", "utf-8") as inputfile:
			inputtext = inputfile.read()
		meta=metaregex.findall(inputtext)[0]
		#if len(meta) != 1:
		#	print fili, "watch out, meta too long or short: it is {}".format(len(meta))
		text= textregex.findall(inputtext)[0]
		if len(textregex.findall(inputtext)) != 1:
			print fili, "watch out, text too long"
		text= annotationregex.sub(" ", text)
		text= smallannotationregex.sub("", text)
		with codecs.open(os.path.join("eecprocessed", fili), "w", "utf-8") as outputfile:
			outputfile.write(meta+text+"</text> </file>")
		print "written to", outputfile
			

metacleaner('/Users/ps22344/Downloads/editdistance/outputfiles/eec_extracted')




		