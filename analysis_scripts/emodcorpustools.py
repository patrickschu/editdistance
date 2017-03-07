import os
import re
import codecs
import nltk.tokenize
import pandas
import string
import time
import json
from collections import defaultdict



#some of these are taken from clustertools
def tagextractor(text, tag, fili):
    regexstring="<"+tag+"=(.*?)>"
    result=re.findall(regexstring, text, re.DOTALL)
    if len(result) != 1:
        print "alarm in tagextractor", fili, result
    return result[0]
    
    
#regexes and strings
punct= string.punctuation
metaregex= "({|<).*?(>|})"


#helper functions
def authornameconverter(name_string, corpus_name):
	"""
	Converts all author names from different corpora to lastname_firstname according to rules associated with corpus_name. 
	Separators set to " " and "_".
	If only one item, returns unchanged. 
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
			#print "turned {} into {}".format(name_string.decode("utf-8"), name_string.lower().decode("utf-8"))
			return name_string.lower()
	else:
		outputname= seps.split(name_string.lower())
		#print "turned {} into {}".format(name_string, corpusdict[corpus_name](outputname).decode("utf-8"))
		return corpusdict[corpus_name](outputname)

def dictbuilder(input_dir, output_csv=False):
	"""
	Builds a dictionary of all texts in input_dir.
	Format: {word:count}
	"""
	dicti=defaultdict(int)
	for w in os.walk(input_dir):
		folder=w[0]
		print "folder", folder 
		for fili in [i for i in w[2] if i.endswith(".txt")]:
			text= CorpusText(os.path.join(input_dir, folder, fili))
			for word in text.tokenizer(cleantext=True):
				dicti[word.lower()]= dicti[word]+1
	if output_csv:
		with codecs.open("dictbuilder_output.json", "w") as jsonout:
			json.dump(dicti, jsonout, encoding="utf-8")
		print "File written to", jsonout
	return dicti


def variantfinder(input_dict, variant_one, variant_two):
	"""
	The variantfinder identifies words in in the input_dict that exist with both variant_1 and variant_2.
	I.e. if variant_one is "u" and variant_two is "v", this will pick up on "us" and "vs".
	It returns a dictionary with the counts for each variant, the key being variant_one.
	"""
	print "running the variantfinder"
	variantonedict= {k:v for k,v in input_dict.items() if variant_one in list(k)}
	outputdict= {}
	for entry in variantonedict:
		if input_dict.get(re.sub(variant_one, variant_two, entry), None):
			outputdict[entry]={variant_one:variantonedict[entry], variant_two:input_dict[re.sub(variant_one, variant_two, entry)]}
	return outputdict



def contextfinder(input_word, variant, pre_window, post_window):
	"""
	The contextfinder finds all instances of variant in the input_word.
	It yields a number of characters preceding and folllowing it as specified by pre_window and post_window.
	Pre_window is the number of characters preceding, post_window the number following the variant. 
	"""
	#print "running the contextfinder"
	#establish position of variants in the word
	indices= [no for no,i in enumerate(list(input_word)) if i==variant]
	if len(indices) < 1:
		print "\nERROR in contextfinder: No instances of '{}' found in '{}'\n".format(variant, input_word)
	#establish the indices for context
	ranges= [(range(i-pre_window, i),range(i+1, i+1+post_window))  for i in indices]
	for ran in ranges:
		output=tuple(tuple((input_word[x] for x in i if -1 < x < len(input_word))) for i in ran)
		#print output
		yield output



##classes

class CorpusText(object):
	"""
	The CorpusText object compiles all the relevant infos for individual corpus files/texts.
	Metadata outside of text are stored in dictionary 'meta'.
	"""
	def __init__(self, file_name):
		self.filename = file_name
		self.fullfile = codecs.open(file_name, "r", 'utf-8').read()
		self.fulltext = self._adtextextractor(self.fullfile)
		self.cleantext= re.sub(metaregex, " ", self.fulltext)
		self.charcount = float(len(self.fulltext))
		self.wordcount = float(len([i for i in nltk.word_tokenize(self.cleantext) if not i in punct]))
		self.metalist= [
		'no', 
		'corpusnumber', 
		'corpus', 
		'title', 
		'author', 
		'dialect', 
		'authorage', 
		'pubdate', 
		'genre1', 
		'genre2', 
		#'notes', 
		#'extraction_notes', 
		#'encoding'
		]
		
		self.uniq = "this is the overall corpus number"
		self.meta = {k:re.sub("(\t+|\n+|\r+)", " ", self._tagextractor(self.fullfile, k)) for k in self.metalist}
		
	def test(self):
		print "fulltext", len(self.fulltext)
		print "charcount", self.charcount
		print self.meta
	
	def tokenizer(self, cleantext=False):
		if cleantext:
			return nltk.word_tokenize(self.cleantext)
		else:
			return nltk.word_tokenize(self.fulltext)
	
	def gettag(self, tag):
		#flexible tag extractor; returns what _tagextractor finds for relevant tag
		result=self._tagextractor(self.fullfile, tag)
		print result
		return result
		
	def _tagextractor(self, text, tag):
		#from clustertools
		regexstring="<"+tag+"=(.*?)>"
		result=re.findall(regexstring, text, re.DOTALL)
		if len(result) != 1:
			print "alarm in tagextractor", result, tag
		return result[0]
		
	def _adtextextractor(self, text):
		#from clustertools
		regexstring="<text>(.*?)</text>"
		result=re.findall(regexstring, text, re.DOTALL)
		if len(result) != 1:
			print "alarm in adtextextractor", fili, result
		return result[0]




class Corpus(object):
	"""
	The Corpus object compiles all relevant info for an entire corpus. 
	It reads in a tab-separated spreadsheet. 
	"""
	def __init__(self, spreadsheet):
		self.corpusname = spreadsheet
		self.data = pandas.read_csv(spreadsheet, delimiter = "\t", encoding = "utf-8")
	
	def filecount(self):
		#returns the number of files, a.k.a. the number of rows
		#NAs?
		filecount = len(self.data.index)
		#print "{} files".format(filecount)
		return filecount
	
	def wordcount(self, column_name):
		#returns the sum of the column with column_name, which contains wordcounts per file
		#also returns dict with major statistics
		wordcount = self.data[column_name].sum()
		wordmean = self.data[column_name].mean()
		wordmedian = self.data[column_name].median()
		wordstdev = self.data[column_name].std()
		#print "{} words".format(wordcount)
		return wordcount, {'count': wordcount, 'mean': wordmean, 'median': wordmedian, 'stdev': wordstdev}
	
	def categoryfeatures(self, column_name):
		#this returns the features of the category contained in column_name:
		#how many Ns, how many uniques
		subset=self.data[column_name]
		categorytype = subset.dtype
		categorylevels = subset.unique()
		return {'type': categorytype , 'levels': categorylevels}
		
	def describe(self):
		self.data.describe()


