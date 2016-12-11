import os
import re
import codecs
import nltk.tokenize

#partially, these are taken from clustertools


def tagextractor(text, tag, fili):
    regexstring="<"+tag+"=(.*?)>"
    result=re.findall(regexstring, text, re.DOTALL)
    if len(result) != 1:
        print "alarm in tagextractor", fili, result
    return result[0]




class CorpusText(object):
	"""
	The Corpus object compiles all the relevant infos for corpus files.
	Metadata outside of text are stored in dictionary 'meta'.
	"""
	def __init__(self, file_name):
		self.filename = file_name
		self.fulltext = codecs.open(file_name, "r", 'utf-8').read()
		self.charcount = float(len(self._adtextextractor(self.fulltext)))
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
		'notes', 
		'extraction_notes', 
		'encoding'
		]
		
		self.uniq = "this is the overall corpus number"
		self.meta = {k:re.sub("(\t|\n)", " ", self._tagextractor(self.fulltext, k)) for k in self.metalist}
		
	def test(self):
		print "fulltext", len(self.fulltext)
		print "charcount", self.charcount
		print self.meta
	
	def gettag(self, tag):
		#flexible tag extractor; returns what _tagextractor finds for relevant tag
		result=self._tagextractor(self.fulltext, tag)
		print result
		return result
		
	def _tagextractor(self, text, tag):
		#from clustertools
		regexstring="<"+tag+"=(.*?)>"
		result=re.findall(regexstring, text, re.DOTALL)
		if len(result) != 1:
			print "alarm in tagextractor", result
		return result[0]
		
	def _adtextextractor(self, text):
		#from clustertools
		regexstring="<text>(.*?)</text>"
		result=re.findall(regexstring, text, re.DOTALL)
		if len(result) != 1:
			print "alarm in adtextextractor", fili, result
		return result[0]