import os
import re
import codecs

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
	"""
	def __init__(self, file_name):
		self.filename=file_name
		self.fulltext = codecs.open(file_name, "r", 'utf-8').read()
		self.charcount = len(self._adtextextractor(self.fulltext))
		
		self.uniq="this is the overall corpus number"
		self.corpusnumber=self._tagextractor(self.fulltext, "corpusnumber")
		self.corpusname=self._tagextractor(self.fulltext, "corpus")
		self.title=self._tagextractor(self.fulltext, "title")
		self.author=self._tagextractor(self.fulltext, "author")
		self.pubdate=self._tagextractor(self.fulltext, "pubdate")
		
	#we need a flexible tag extractor
	def test(self):
		print "fulltext", len(self.fulltext)
		print "charcount", self.charcount
		print "corpusnumber", self.corpusnumber
		print "title", self.title
		print "author", self.author
		print "pubdate", self.pubdate
	
	def getdetail(self, tag):
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