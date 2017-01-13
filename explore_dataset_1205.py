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



def fullcorpusmaker (input_dir, output_csv=False):
	"""
	Iterates over input_dir, calls on explorer.
	Writes to tab-separated csv/
	"""
	for folder in [i for i in os.listdir(input_dir) if not i.startswith(".")]:
		print folder
		filename=folder
		#make full corpus
		fullcorpus=explorer (os.path.join(input_dir, folder))
		if output_csv:
			with open(filename+"_fullcorpus.csv", "w") as fullcorpus_out:
				pandas.DataFrame(fullcorpus).T.to_csv(fullcorpus_out, sep="\t", encoding='utf-8')
		print "full dataset written to", fullcorpus_out
		

		
def byauthormaker (input_dir, full_corpus):
	"""Incomplete"""
	fullcorpus_by_author=aggregator(fullcorpus, 'author', set([v['author'] for k,v in fullcorpus.items()]))
	for d in fullcorpus_by_author:
		#print d, fullcorpus_by_author[d], "length", len(fullcorpus_by_author[d]) 
		authorlist=[v['wordcount'] for k,v in fullcorpus_by_author[d].items()]
		fullcorpus_by_author[d]['totalwords']=sum(authorlist)
		#print fullcorpus_by_author
		#structure: AUTHOR : {filename:{genre:X, corpus:Y, etc}, filename_2:{genre:Z, corpus:Y, etc}, totalwords:x}

main ('extracted_corpora_small')

	


#make overview
#by corpus
#by author
#by text length