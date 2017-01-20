import codecs
import os
import emodcorpustools as emo
from collections import defaultdict
import pandas
import json
import nltk
import re


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


def authornameconverter(name_string, corpus_name):
	"""
	Converts all author names from different corpora to lastname_firstname.
	If not firstname, use "X"
	What about missing names?
	"""
	corpusdict={
	'parsed_corpus_of_early_english_correspondence': (lambda x: "_".join((x[len(x)-1], x[0]))),#"WILLIAM_MARYON",
	'lampeter_corpus' : (lambda x: "_".join((x[len(x)-1], x[0]))),#"Richard Mead"
	'early_modern_english_medical_texts' : (lambda x: "_".join((x[len(x)-1], x[0]))),#Joseph Blagrave 
	'helsinki_corpus_xml_edition' : (lambda x: "_".join((x[0], x[len(x)-1]))),#SMITH HENRY
	'innsbruck_letter_corpus' : (lambda x: "_".join((x[len(x)-1], x[0]))),#Queen Margaret, Dorothye Plumpton
	'first_folio_of_shakespeare_machine_readable_text_format' : (lambda x: "_".join((x[0], x[len(x)-1]))),#shakespeare, william
	'corpus_of_early_english_dialogs' : (lambda x: "_".join((x[0], x[len(x)-1])))#WARNER WILLIAM
	
	}
	seps=[" ", "_"]
	seps=re.compile("|".join(seps))
	
	name_string=name_string.strip(" ")
	if len(seps.split(name_string)) == 1:
			return name_string.lower()
	else:
		outputname= seps.split(name_string.lower())
		return corpusdict[corpus_name](outputname)



	
	
def authorfinder(input_dir, output_txt=False):
	"""
	Outputs list of authors to ID writers present in several corpora.
	Gives title and location for each
	"""
	authordict=defaultdict(list)
	for folder in [i for i in os.listdir(input_dir) if not i.startswith(".")]:
		print folder
		for fili in [i for i in os.listdir(os.path.join(input_dir, folder)) if not i.startswith(".")]:
			corpustext=emo.CorpusText(os.path.join(input_dir, folder, fili))
			author_normalized=authornameconverter(corpustext.meta['author'], corpustext.meta['corpus'])
			authordict[author_normalized].append((corpustext.meta['title'], corpustext.meta['corpus'], os.path.join(input_dir, folder)))
	for f in sorted(authordict.keys()):
		for title, corpus, file_name in authordict[f]:
			if len(set(corpus)) > 10:
				print f
	

authorfinder('/Users/ps22344/Downloads/editdistance/extracted_corpora')
	
	

def sametextfinder(input_dir, chunk_length, starting_point=0):
	"""
	Takes chunk length chunk_length from each text, starting at starting_point.
	Then compares to rest of corpus.
	"""
	print "assi"