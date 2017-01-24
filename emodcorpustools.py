import os
import re
import codecs
import nltk.tokenize
import pandas

#partially, these are taken from clustertools

def tagextractor(text, tag, fili):
    regexstring="<"+tag+"=(.*?)>"
    result=re.findall(regexstring, text, re.DOTALL)
    if len(result) != 1:
        print "alarm in tagextractor", fili, result
    return result[0]
    
    
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
			print "turned {} into {}".format(name_string, name_string.lower())
			return name_string.lower()
	else:
		outputname= seps.split(name_string.lower())
		print "turned {} into {}".format(outputname, corpusdict[corpus_name](outputname))
		return corpusdict[corpus_name](outputname)




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


class CorpusText(object):
	"""
	The CorpusText object compiles all the relevant infos for corpus files.
	Metadata outside of text are stored in dictionary 'meta'.
	"""
	def __init__(self, file_name):
		self.filename = file_name
		self.fullfile = codecs.open(file_name, "r", 'utf-8').read()
		self.fulltext = self._adtextextractor(self.fullfile)
		self.charcount = float(len(self.fulltext))
		self.wordcount = float(len(nltk.word_tokenize(self.fulltext)))
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