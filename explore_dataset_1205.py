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
    







def explorer(input_dir):
	for fili in [i for i in os.listdir(input_dir) if not i.startswith(".")]:
		print "\n\n", fili
		text=emo.CorpusText(os.path.join(input_dir, fili))
		for item in text.meta:
			print item, text.meta[item]
explorer ('/Users/ps22344/Downloads/editdistance/outputfiles/eec_extracted/')
#rr=emo.CorpusText("/Users/ps22344/Downloads/editdistance/outputfiles/eec_extracted/L_STUART_058_extracted.txt")



#rr.test()

#rr.getdetail("notes")

# for k in rr.meta:
# 	print k, rr.meta[k]

#print rr.meta['title']


#make overview
#by corpus
#by author
#by text length