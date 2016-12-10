import codecs
import os
import emodcorpustools as emo
from collections import defaultdict
import pandas

##INSPECTING



def explorer(input_dir):
	"""
	The explorer wanders thru the input_dir, returns a dictionary with relevant info.
	Info supplied by CorpusText object.
	"""
	dicti=defaultdict(dict)
	for fili in [i for i in os.listdir(input_dir) if not i.startswith(".")]:
		#print "\n\n", fili
		texti=emo.CorpusText(os.path.join(input_dir, fili))
		dicti[fili]['wordcount']=texti.wordcount
		dicti[fili]['charcount']=texti.charcount
		dicti[fili]['avg_wordlength']=(dicti[fili]['charcount'])/(dicti[fili]['wordcount'])
		for key in texti.meta:
			dicti[fili][key]=texti.meta[key]
	return dicti

def aggregator(dictionary, category, list_of_terms):
	"""
	The aggregator aggregates all items from dictionary.
	It goes thru the list of terms, and returns a dictionary.
	It adds each term as a key and enters all the relevant data from dicitonary.
	category author and DKA in list of terms gets you
	Dame Katherine Arundell  {'57_innsbruck_extracted.txt': {'genre1':, etc.
	Note how we can just run this over a set() of authors contained in fullcorpus. 
	"""
	dicti=defaultdict(dict)
	for term in list_of_terms:
		print term
		dicti[term]={k:v for k,v in dictionary.items() if term in dictionary[k][category]}
	print len(dicti)
	return dicti



filename="innsbruck_letters"
#make full corpus
fullcorpus=explorer ('/Users/ps22344/Desktop/innsbruck_extracted')
print set([v['author'] for k,v in fullcorpus.items()])
#look at authors
fullcorpus_by_author=aggregator(fullcorpus, 'author', set([v['author'] for k,v in fullcorpus.items()]))
#print fullcorpus_by_author
for key in fullcorpus_by_author:
	with codecs.open(filename+"_by_author.csv", "a", "utf-8") as fullcorpus_by_author_out:
		pandas.DataFrame(fullcorpus_by_author[key]).T.to_csv(fullcorpus_by_author_out)
		

	




# for corpus in set([v['corpus'] for k,v in fullcorpus.items()]):
# 	by_subcorpus_corpus=aggregator(fullcorpus, 'corpus', corpus)
# 	by_subcorpus_corpus=aggregator(fullcorpus, 'author', 'Mary Evelyn')
# 	print by_subcorpus_corpus
	
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