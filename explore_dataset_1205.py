import codecs
import os
import emodcorpustools as emo
from collections import defaultdict

##INSPECTING

def tagextractor(text, tag, fili):
    regexstring="<"+tag+"=(.*?)>"
    result=re.findall(regexstring, text, re.DOTALL)
    if len(result) != 1:
        print "alarm in tagextractor", fili, result
    return result[0]
    







def explorer(input_dir):
	dicti=defaultdict(dict)
	for fili in [i for i in os.listdir(input_dir) if not i.startswith(".")]:
		print "\n\n", fili
		texti=emo.CorpusText(os.path.join(input_dir, fili))
		dicti[fili]['wordcount']=texti.wordcount
		dicti[fili]['charcount']=texti.charcount
		dicti[fili]['avg_wordlength']=(dicti[fili]['charcount'])/(dicti[fili]['wordcount'])
		for key in texti.meta:
			dicti[fili][key]=texti.meta[key]

	return dicti


#for key in meta: fili[key]=meta[key]
#dicti={fili:text.meta}
#add word and character length

fullcorpus=explorer ('/Users/ps22344/Desktop/innsbruck_extracted')


def aggregator(dictionary, category, *list_of_terms):
	dicti=defaultdict(dict)
	for term in list_of_terms:
		dicti[term]={k:v for k,v in dictionary.items() if term in dictionary[k][category]}
		return dicti
		

	

for key in fullcorpus:
	print fullcorpus[key]['avg_wordlength']


for corpus in set([v['corpus'] for k,v in fullcorpus.items()]):
	by_subcorpus_corpus=aggregator(fullcorpus, 'corpus', corpus)
	by_subcorpus_corpus=aggregator(fullcorpus, 'author', 'Mary Evelyn')
	print by_subcorpus_corpus
	
#for corpus in set(fullcorpus)

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