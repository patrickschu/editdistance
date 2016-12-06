import codecs
import os
import emodcorpustools as emo

##INSPECTING

def tagextractor(text, tag, fili):
    regexstring="<"+tag+"=(.*?)>"
    result=re.findall(regexstring, text, re.DOTALL)
    if len(result) != 1:
        print "alarm in tagextractor", fili, result
    return result[0]
    







def taggetter(input_dir, tag):
	for fili in [i for i in os.listdir(input_dir) if not i.startswith(".")]:
		print "\n\n", fili
		with codecs.open(os.path.join(input_dir, fili), "r", "utf-8") as inputfili:
			inputtext=inputfili.read()
			#print "raw text", inputtext[-100:]
			result=emo.tagextractor(inputtext, tag, fili)
			print result
			
#taggetter("/Users/ps22344/Downloads/editdistance/outputfiles/eec_extracted/", "author")

rr=emo.CorpusText("/Users/ps22344/Downloads/editdistance/outputfiles/eec_extracted/L_STUART_058_extracted.txt")


rr.test()

rr.getdetail("notes")
