import codecs
import os
import emodcorpustools as emo
from collections import defaultdict
import pandas
import json
import nltk
import re

##INSPECTING

def yieldexplorer(input_dir):
	"""
	Failed experiment; this is just a version of the explorer that takes the super folder as input.
	The explorer wanders thru the input_dir, returns a dictionary with relevant info.
	Info supplied by CorpusText object.
	"""
	dicti=defaultdict(dict)
	for folder in [i for i in os.listdir(input_dir) if not i.startswith(".")]:
		print folder
		for fili in [i for i in os.listdir(os.path.join(input_dir, folder)) if not i.startswith(".")]:
			#print "\n\n", fili
			texti=emo.CorpusText(os.path.join(input_dir, folder, fili))
			dicti[texti.filename]={
			'wordcount':texti.wordcount,
			'charcount':texti.charcount,
			'filename':texti.filename
			}
			dicti[texti.filename]['avg_wordlength']=(dicti[texti.filename]['charcount'])/(dicti[texti.filename]['wordcount'])
			for key in texti.meta:
				dicti[texti.filename][key]=texti.meta[key]
	#print dicti
	return dicti



def explorer(input_dir):
	"""
	The explorer wanders thru the input_dir, returns a dictionary with relevant info/metadata on each file.
	Info supplied by CorpusText object.
	"""
	dicti=defaultdict(dict)
	for fili in [i for i in os.listdir(input_dir) if not i.startswith(".")]:
		#print "\n\n", fili
		texti=emo.CorpusText(os.path.join(input_dir, fili))
		dicti[fili]['wordcount']=texti.wordcount
		dicti[fili]['charcount']=texti.charcount
		dicti[fili]['avg_wordlength']=(dicti[fili]['charcount'])/(dicti[fili]['wordcount'])
		dicti[fili]['filename']=texti.filename
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
		
		
def bytext(input_dir, output_json=False):
	outputdict=yieldexplorer(input_dir)
	finaldict= {outputdict[k]['filename']:{
				'wordcount':outputdict[k]['wordcount'],
				'author':outputdict[k]['author'], 
				'corpus':outputdict[k]['corpus'], 
				'title': outputdict[k]['title'].lstrip(" ")} for k,v in outputdict.items()}
	if output_json:
		with codecs.open("bytext_0113.json", "w", "utf-8") as jsonout:
			json.dump(finaldict, jsonout)
	result= [v for k,v in finaldict.items()]
	sortedresult=sorted(result, key=lambda x:(x['wordcount'], x['title']) )
	outputi=codecs.open("titles_sorted_by_wordcount.txt", "a", "utf-8")
	for dict in sortedresult:
		outputi.write(dict['title']+"\t**"+dict['corpus']+"\t**"+dict['author']+"\t**"+unicode(dict['wordcount'])+"\n")
	outputi.close()
	


def bycount(input_dir, output_json=False):
	inputdict=yieldexplorer(input_dir)
	outputdict=defaultdict(list)
	outputtext=codecs.open("bycount.txt", "a", "utf-8")
	for entry in inputdict:
		outputdict[inputdict[entry]['wordcount']].append(inputdict[entry])
	for item in sorted(outputdict):
		if len(outputdict[item]) > 1:
			print "\n****",item
			print "\t".join(["author", "title", "corpus"])
			sortedresults= sorted(outputdict[item], key=lambda x:(x['author'], x['title']))
			print "\n".join(["\t".join((i['author'], i['title'], i['corpus'])) for i in sortedresults])
			#writeout
			outputtext.write("\n\n****"+unicode(item)+"\n")
			#outputtext.write("\t".join(["author", "title", "corpus"])+"\n")
			sortedresults= sorted(outputdict[item], key=lambda x:(x['author'], x['title']))
			#print sortedresults
			outputtext.write("\n".join(["\t*".join((i['author'], i['title'], i['corpus'], i['filename'])) for i in sortedresults]))
	outputtext.close()


def dictmaker(input_dir, json_out=False):
	"""
	count all words in the corpus.
	Parameters
	---
	input_dir to iterate over
	
	Returns
	---
	Dictionary {word:count, word2:count, ...}
	"""
	htmlregex=re.compile("<.*?>", re.DOTALL)
	curlyregex=re.compile("\{.*?\}")
	fulldict=defaultdict(float)
	for folder in [i for i in os.listdir(input_dir) if not i.startswith(".")]:
		print folder
		for fili in [i for i in os.listdir(os.path.join(input_dir, folder)) if not i.startswith(".")]:
			#print "\n\n", fili
			texti=emo.CorpusText(os.path.join(input_dir, folder, fili))
			cleantext=curlyregex.sub("", texti.fulltext)
			cleantext=htmlregex.sub("", cleantext)
			for word in nltk.word_tokenize(cleantext):
				fulldict[word]=fulldict[word]+1
	if json_out:
		with codecs.open("fulldict.json", "w", "utf-8") as jsonout:
			json.dump(fulldict, jsonout, encoding="utf-8")
	sorteddict=sorted(fulldict, key=lambda x:fulldict[x], reverse=True)
	outputfile=codecs.open("dicti.txt","w", "utf-8")
	outputfile.write("\n".join([":".join((i, unicode(fulldict[i]))) for i in sorteddict if fulldict[i] > 100]))
	outputfile.close()		
			# dicti[texti.filename]={
# 			'wordcount':texti.wordcount,
# 			'charcount':texti.charcount,
# 			'filename':texti.filename
# 			}
# 			dicti[texti.filename]['avg_wordlength']=(dicti[texti.filename]['charcount'])/(dicti[texti.filename]['wordcount'])
# 			for key in texti.meta:
# 				dicti[texti.filename][key]=texti.meta[key]
# 		#print dicti
# 		return dicti
dictmaker('extracted_corpora', json_out=True)

"""
not even started on this one
"""
def byauthor(input_dir, output_json=False):
	inputdict=yieldexplorer(input_dir)
	outputdict=defaultdict(list)
	outputtext=codecs.open("bycount.txt", "a", "utf-8")
	for entry in inputdict:
		outputdict[inputdict[entry]['wordcount']].append(inputdict[entry])
	for item in sorted(outputdict):
		if len(outputdict[item]) > 1:
			print "\n****",item
			print "\t".join(["author", "title", "corpus"])
			sortedresults= sorted(outputdict[item], key=lambda x:(x['author'], x['title']))
			print "\n".join(["\t".join((i['author'], i['title'], i['corpus'])) for i in sortedresults])
			#writeout
			outputtext.write("\n\n****"+unicode(item)+"\n")
			#outputtext.write("\t".join(["author", "title", "corpus"])+"\n")
			sortedresults= sorted(outputdict[item], key=lambda x:(x['author'], x['title']))
			#print sortedresults
			outputtext.write("\n".join(["\t*".join((i['author'], i['title'], i['corpus'])) for i in sortedresults]))
	outputtext.close()
	
#bycount('extracted_corpora', output_json=True)



		
		
def byauthormaker (input_dir, full_corpus):
	"""Incomplete"""
	"""
	Parameters
	---
	input_dir	folder to iterate over
	full_corpus	dictioanry created by fullcorpusmaker
	"""
	fullcorpus_by_author=aggregator(full_corpus, 'author', set([v['author'] for k,v in fullcorpus.items()]))
	for d in fullcorpus_by_author:
		#print d, fullcorpus_by_author[d], "length", len(fullcorpus_by_author[d]) 
		authorlist=[v['wordcount'] for k,v in fullcorpus_by_author[d].items()]
		fullcorpus_by_author[d]['totalwords']=sum(authorlist)
		#print fullcorpus_by_author
		#structure: AUTHOR : {filename:{genre:X, corpus:Y, etc}, filename_2:{genre:Z, corpus:Y, etc}, totalwords:x}



	


#make overview
#by corpus
#by author
#by text length