import json
import codecs


with codecs.open('/home/patrick/Downloads/editdistance/analysis_scripts/variablewords.json', "r", "utf-8") as inputfile:
	inputdict=json.load(inputfile)
	
	
print type(inputdict.viewkeys())

outputdict= {k:v for k,v in inputdict.viewitems() if "0" in k}

with codecs.open('firstletteronly_0527.json', "w", "utf-8") as outputfile:
	json.dump(outputdict, outputfile)

with codecs.open('firstletteronly_threshold1000_0527.txt', "w", "utf-8") as outputtext:
	for entry in outputdict:
		print entry, ",".join([":".join((k,str(v))) for k,v in outputdict[entry].items()])
		outputtext.write(entry+"\t"+",".join([":".join((k,str(v))) for k,v in outputdict[entry].items()])+"\n")
	
	
	#(inputfile)
