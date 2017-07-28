# -*- coding: utf-8 -*-

import os
import re
import codecs
import nltk.tokenize
#import pandas
import string
import time
import json
from collections import defaultdict
from itertools import chain, combinations

#corpusdir = '/home/patrick/Downloads/editdistance/extracted_corpora_0420_small'
header = "\n+++++\n"
# note that apostrophes are taken care of by the NLTK tokenizer
affixes = ("s")


#some of these are taken from clustertools
def tagextractor(text, tag, fili):
    regexstring="<"+tag+"=(.*?)>"
    result=re.findall(regexstring, text, re.DOTALL)
    if len(result) != 1:
        print "alarm in tagextractor", fili, result
    return result[0]
    
#thank you SO: https://stackoverflow.com/questions/464864/how-to-get-all-possible-combinations-of-a-list-s-elements/40986475#40986475
def powerset(iterable):
    #powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)
    s = list(set(iterable))  # doesn't allow duplicate elements
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))
    
#regexes and strings
punct= string.punctuation
metaregex= "({|<).*?(>|})"


#helper functions
def timer(func):
	def wrapper(*args, **kwargs):
		t = time.time()
		print "timer :: Running {}".format(func.func_name)
		res = func(*args, **kwargs)
		print "timer :: {} took us {}".format(func.func_name, (time.time()-t)/60)
		return res
	return wrapper


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

def dictbuilder(input_dir, output_json=False):
	"""
	Builds a dictionary of all texts in input_dir.
	Format: {word:count}
	"""
	dicti= {}
	for root, direct, filis in os.walk(input_dir):
		print "folder", root 
		for fili in [i for i in filis if i.endswith(".txt")]:
			text= CorpusText(os.path.join(input_dir, root, fili))
			for word in text.tokenizer(cleantext=True):
				word = word.lower()
				if word in dicti:
					dicti[word] = dicti[word] + 1
				else:
					dicti[word] = 1
	if output_json:
		with codecs.open(output_json+".json", "w") as jsonout:
			json.dump(dicti, jsonout, encoding= "utf-8")
		print "File written to", jsonout
	print "\n".join([":".join((i, str(dicti[i]))) for i in sorted(dicti, key= dicti.get, reverse=True)[:100]])
	return dicti


def dictbuilder_2(input_dir, meta_data, output_json=False):
	"""
	Builds a dictionary of all texts in input_dir.
	Builds on dictbuilder but adds functionality to collect by external factors such as date.
	Format: {word: {meta: count, meta:count, meta:count}, word: {}}
	"""
	dicti={}
	for w in os.walk(input_dir):
		folder=w[0]
		print "folder", folder 
		for fili in [i for i in w[2] if i.endswith(".txt")]:
			text= CorpusText(os.path.join(input_dir, folder, fili))
			#print os.path.join(input_dir, folder, fili)
 			if meta_data == 'pubdate':
 				meta= text.meta[meta_data].lstrip(" c")[:4]
 			else:
				meta= text.meta[meta_data]
			for word in text.tokenizer(cleantext=True):
				lword=word.lower()
				if not lword in dicti:
					dicti[lword]={}
					dicti[lword][meta]= 1
				elif not meta in dicti[lword]:
					dicti[lword][meta]= 1
				else:					
					dicti[lword][meta]= dicti[lword][meta]+1
	if output_json:
		with codecs.open(output_json+".json", "w") as jsonout:
			json.dump(dicti, jsonout, encoding= "utf-8")
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


@timer
def variantfinder_2(input_dict, meta_data, variant_one, variant_two):
	"""
	REMEMBER TO NICIFY THIS
	The variantfinder_2 identifies words in in the input_dict that exist with both variant_1 and variant_2.
	It builds on variantfinder but adds functionality to collect variants by external factors, such as time.
	I.e. if variant_one is "u" and variant_two is "v", this will pick up on "us" and "vs".
	It returns a dictionary with the counts for each variant, the key being variant_one.
	Totaldict gives word count by meta_data category
	"""
	print "running the variantfinder_2"
	metadict = defaultdict(dict)
	for entry in input_dict:
		print entry
		print input_dict[entry].keys()
		for key in input_dict[entry].keys():
			if not metadict[key].get(entry, None):
				metadict[key][entry] = input_dict[entry][key]
			else:
				print "Alarm this is weird"
	totaldict= defaultdict(int)
	for key in metadict:
		#add totals for each year
		totaldict[key] = sum(metadict[key].values())
	variantonedict= {key:{k:v for k,v in val.items() if variant_one in list(k)} for key,val in metadict.items()}
	#clean interior dictionary of non-varying items
	combineddict= {key:{k:v for k,v in val.items() if re.sub(variant_one, variant_two, k) in input_dict} for key,val in variantonedict.items()}
	outputdict= {}
	for entry in combineddict:
		#entry is a year
		print combineddict[entry]
		#format is {year1:{word1:{variant_one:X, variant_two:X}, word2:{}}, year2:{}}
		outputdict[entry]={k:{variant_one:v, variant_two:metadict[entry].get(re.sub(variant_one, variant_two, k), 0)} for k,v in combineddict[entry].items()}
	return outputdict, totaldict


@timer	
def findvariants(input_vocab, variant_one, variant_two, threshold = 0):
	"""
	ID words that vary by variant only
	Args : 
	input_vocab : dictionary of vocab to test for variants. Format {word:count} NOTE DO NOT FEED A DEFAULTDICT INTO THIS
	variant_one : String to be tested for variants with variant_two
	variant_two : String to be tested for variants with variant_two
	treshold : Int indicating the minimum tokens of both variants to be included in the output. 
	
	Examples:
	input_dict = {but:1 , bvt:1}
	variant_one = 1, variant_two = v
	will return but, bvt if threshold < 2, else nothing
	"""
	onedict = {VariantItem(k, variant_one, variant_two):v for k,v in input_vocab.viewitems() if variant_one in list(k)}
	#note that typedict.values[0] gives the list
	#show variants
	t=  {"+".join([i.word for i in VariantItem(k, variant_one, variant_two).typedict.values()[0]]):v for k,v in input_vocab.viewitems() if variant_one in list(k)}
	print [[i.yeardict(corpusdir, lower_case = True) for i in k.typedict.values()[0]] for k in onedict.viewkeys()]
	#print onedict


##classes

class CorpusText(object):
	"""
	The CorpusText object compiles all the relevant infos for individual corpus files/texts.
	Metadata outside of text are stored in dictionary 'meta'.
	"""
	def __init__(self, file_name):
		self.filename = file_name
		self.fullfile = codecs.open(file_name, "r", "utf-8").read()
		self.fulltext = self._adtextextractor(self.fullfile)
		self.cleantext= re.sub(metaregex, " ", self.fulltext)
		self.charcount = float(len(self.fulltext))
		#self.wordcount = float(len([i for i in nltk.word_tokenize(self.cleantext) if not i in punct]))
		self.metalist= [
		#'no', 
		#'corpusnumber', 
		#'corpus', 
		'title', 
		'author', 
		#'dialect', 
		#'authorage', 
		'pubdate', 
		'genre1' 
		#'genre2', 
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
	
	def tokenizer(self, cleantext=False, lemmatize=False):
		tokens = nltk.word_tokenize(self.cleantext)
		if cleantext:
			tokens = [i.strip(string.punctuation) for i in tokens if not i in string.punctuation]
		if lemmatize:
			#note that affixes are hardcoded above
			for a in affixes:
				tokens = [i.rstrip(a) for i in tokens]
		return tokens	
			
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
	
# a WORD with VARIANT_ONE is TYPE_ONE, WITH VARIANT_TWO it is TYPE_TWO. 
# all words in the corpus constitute the VOCAB

def pubdateconverter(pubdate):
	# normalize pubdate to 4 digit format
	# returns an int, 0 for empty string
	#print "converter go"
	pubdate = re.split(ur"(—|-|–)", pubdate)[0]
	#print "pubdate", pubdate
	pubdate = "".join([i for i in list(pubdate) if i.isdigit()][:4])
	#print "merged pubdate"
	if len(pubdate) > 4:
		print "Warning from pubdateconverter: {} is longer than 4 digits".format(pubdate)
	elif not pubdate:
		#print "PUBDATE IS NOT"
		pubdate = 0 
	return pubdate	

def CorpusVocabImporter(input_json):
	"""
	Read in json file created by Corpus_2 vocabbuilder to create dictionary of CorpusWord items.
	Format of input_json is 
	{word: {year:X, year2:Y}, word2:{}}
	Returns {word:CorpusWord(word), word2:Corpusword(word2), }
	"""
	print "Running the CorpusVocabImporter, getting data from ", input_json
	with codecs.open(input_json, "r", "utf-8") as inputjson:
		inputdict = json.load(inputjson)
	vocabdict = {}
	for word in inputdict:
		vocabdict[word] = CorpusWord(word, "VARIANT", "POSITION")
		vocabdict[word].yeardict = {int(k): int(v) for k,v in inputdict[word].viewitems()}
	return vocabdict

class CorpusWord(CorpusText):
	"""
	The CorpusWord object compiles all relevant info for a specific word.
	Args
	word : String of word
	variant : String of variant
	position : index of variant in word
	
	Example
	word : but
	variant : u  
	position : (1,3)
	"""
	def __init__(self, word, variant, position):
		self.word = word
		self.variant = variant
		self.position = position
		self.length = len(word)
		self.yeardict = {}
	#integrate variation by position
	# do we need?
	@timer
	def yeardictmaker(self, input_dir, lower_case = False):
		#yeardict compiles counts of self.word by year across all texts in input_dir
		#if lower_case, texts in input_dir will be lower cased. 
		#NOTE THAT THE DEFDICT WILL DEFAULT TO 0; I.E no EMPTY KEYS
		print "Running the yeardictmaker"
		tokensperyear = defaultdict(int)
		for root, direct, filis in os.walk(input_dir):
			print header, "working on", root, len(filis), "files"
			for fili in [i for i in filis if not i.startswith(".")]:
				inputtext = CorpusText(os.path.join(root, fili))
				if lower_case:
					inputtokens = [i.lower() for i in inputtext.tokenizer(cleantext = True)]
				else:
					inputtokens = inputtext.tokenizer(cleantext = True)
				if self.word in inputtokens:
					hits = [i for i in inputtokens if i == self.word]
					#clean the pubdates
					pubdate = pubdateconverter(inputtext.meta['pubdate'])
					if not pubdate:
						pubdate = 0
					tokensperyear[pubdate] = tokensperyear[pubdate] + 1
		return({k:v for k,v in tokensperyear.viewitems()})
		# we can model other flexible word counts on this: just give attribute to sort by as argument. 
		# smooth.
	
	def yeardictsetter(self, pubdate, count):
		#update function for yeardict
		#this is also used in the method above, we can make a separate function for this, just like for authors
		#print pubdate
		pubdate = pubdateconverter(pubdate)
		if not pubdate in self.yeardict:
			self.yeardict[pubdate] = count
		else:
			self.yeardict[pubdate] = self.yeardict[pubdate] + count	
			#print "updating ", self.word, "\n", self.yeardict		
	
	def positionsetter(self, position):
		#changes the position attribute
		#what is the input here - a tuple?
		self.position = position
		
	def totaltokens(self):
		#returns number of tokens of word contained in yeardict
		return sum(self.yeardict.viewvalues())

class VariantItem(object):
	"""
	This compiles the potential variants of a word
	The typedict returns {word : [variant 1, var 2, ...}  <- this is no longer accurate ; its typedict[word][position] = CorpusWord
	It extracts the CorpusWord objects from a dictionary given in input_vocab
	"""
	def __init__(self, word, variant_one, variant_two, input_vocab, word_list= False):
		self.word = word
		self.variant_one = variant_one
		self.variant_two = variant_two
		self.word_list = word_list
		self.typedict = self.typegenerator(input_vocab, word_list = self.word_list)

	def indexer(self):
		#finds instances of variant in self.word
		#return list of [(variant, index), (variant, index)]
		#NOTE THAT THIS WILL NOT SPLIT UP 3 CHAR STRETCHES WHEN LOOKING FOR 2 CHARS, e.g. "uuu" will be one instance of "uu", not 2
		word = self.word
		variant = self.variant_one
		indices = []
		index = 0
		while index < len(word):
			index = word.find(variant, index)
			#print word, index
			if index == -1:
				break			
			indices.append((variant, index))
			index = index + len(variant)
		return indices
	
	def typedictsetter(self, input_dict):
		print "setting dict"
		self.typedict = input_dict
		
	def typegenerator(self, input_vocab, word_list):
		# creates new types of the word by replacing characters at index with variant
		# when more than one substitution spot, create all permutations
		indices = self.indexer()
		#print header, "runnin the typegenerator"
		word = self.word
		typedict = {word : {}}
		#powerset combines the indices to unique combinations, e.g. [1,2] --> (1), (2), (1,2)
		for index_tuple in powerset(indices):
			#print "index_tuple", index_tuple
			if index_tuple: 
				#dang we used the same var name in the main script for a different concept
				wordlist = list(word)
				#error catching
				index_list = [position for variant, position in index_tuple]
				#we could keep this as a tuple: `tuple(i[1] for i in index_tuple)`
				for ind in index_list:
					if wordlist[ind] != self.variant_one:
						print "WARNING : ISSUE IN TYPEGENERATOR (tuples returned from indexer do not match variant_one)"
				#print "original", "".join(wordlist)
				#print index_list
					#print "ind:", ind 
					wordlist[ind] = self.variant_two
					#print "".join(wordlist)
					match = input_vocab.get("".join(wordlist), None)
					#match = True if "".join(wordlist) in input_vocab else None
					if not word_list: 
						if match:
							#note that match is a CorpusWord object
							#print "match: ", match
							match.positionsetter(tuple(index_list))
							#can there be more than one match per ind?
							typedict[word][ind] = match
					else:
						#here be the word_list functionality
						#Standard
						if match:
							#note that match is a CorpusWord object
							#print "match: ", match
							match.positionsetter(tuple(index_list))
							#can there be more than one match per ind?
							typedict[word][ind] = match
						#get variant_ones that don't have a variant_two in the corpus
						else:
							if "".join(wordlist) in word_list:
								#print "this is not in our vocab but the supplied word_list. Who knew", "".join(wordlist)
								entry = CorpusWord("DUMMY", self.variant_two, "POSITION")
								#print "set position"
								entry.positionsetter(tuple(index_list))
								#print "add to dict"
								typedict[word][ind] = entry
								#checking for variant_two happens in the variantfinder script
	
							else:
								pass
						#get variant_twos that don't have a variant_one in the corpus
					

		#print "VariantItems returning"	
		#TO DO this should not be a list as value. Right?					
		#self.typedict = {k: v for k,v in typedict.viewitems()}
		return {k: v for k,v in typedict.viewitems()}




class Corpus_2(object):
	"""
	The Corpus_2 object defines corpus-wide methods and attributes.
	"""
	def __init__(self, input_dir, name = "corpus"):
		self.name = name
		self.input_dir = input_dir
	
	@timer
	def vocabbuilder(self, lemmatize = False, output_json = False, use_word_list = False, noisy = False):
		"""
		Builds a dictionary of all texts in input_dir, updating the yeardict {} of Corpusword.
		Returns a dictionary like so : {word: CorpusWord(), ...}
		"""
		#TO DO: make this take a pre-defined vocabulary
		print "running the vocabbuilder from corpus_2"
		if not use_word_list:
			vocabdict = self._vocabbuilder_pure(lemmatize = lemmatize)
		else:
			vocabdict = self._vocabbuilder_from_list(word_list = use_word_list, lemmatize = lemmatize)
		if output_json:
			with codecs.open(output_json+".json", "w") as jsonout:
				json.dump({k:{int(year):int(count) for year, count in v.yeardict.viewitems()} for k,v in vocabdict.viewitems()}, jsonout, encoding= "utf-8")
			print "File written to", jsonout
		if noisy:
			print "\n++".join([":".join((i, "\n".join([":".join((str(k),str(v))) for k,v in vocabdict[i].yeardict.items()]))) for i in sorted(vocabdict, key= lambda x: sum(vocabdict[x].yeardict.values()), reverse=True)[:100]])
		return vocabdict

	def _vocabbuilder_from_list(self, word_list, lemmatize):
		# builds vocab based on word_list, some set-type thing to iterate over
		# called from vocabbuilder
		# note that the word_list needs to be a superset of words in corpus
		vocabdict = {}
		#word_list = set([k for k,v in word_list.viewitems()])
		print "running _vocabbuilder_from_list"
		print "List is {} items long".format(len(word_list))
		for root, direct, filis in os.walk(self.input_dir):
			print "working on folder", root 
			for fili in [i for i in filis if i.endswith(".txt")]:
				text= CorpusText(os.path.join(self.input_dir, root, fili))
				#print os.path.join(self.input_dir, root, fili), text.meta['pubdate']
				for word in text.tokenizer(lemmatize = lemmatize, cleantext=True):
					word = word.lower()
					#print "wordiword", word
					if word in vocabdict:
						vocabdict[word].yeardictsetter(text.meta['pubdate'], 1)
					elif word in word_list: 
						#print "adding", word
						vocabdict[word] = CorpusWord(word, "VARIANT", "POSITION")
						vocabdict[word].yeardictsetter(text.meta['pubdate'], 1)
					else:
						raise ValueError("Word '{}'from corpus not contained in the word_list supplied; make sure the list was built including the present corpus and lemmatization was identical".format(word))
		return vocabdict
		
	def _vocabbuilder_pure(self, lemmatize):
		# builds vocab from scratch; called from vocabbuilder
		print "running _vocabbuilder_pure"
		vocabdict = {}
		for root, direct, filis in os.walk(self.input_dir):
			print "working on folder", root 
			for fili in [i for i in filis if i.endswith(".txt")]:
				text= CorpusText(os.path.join(self.input_dir, root, fili))
				#print os.path.join(self.input_dir, root, fili), text.meta['pubdate']
				for word in text.tokenizer(lemmatize = lemmatize, cleantext=True):
					word = word.lower()
					if word in vocabdict:
						vocabdict[word].yeardictsetter(text.meta['pubdate'], 1)
					else:
						vocabdict[word] = CorpusWord(word, "VARIANT", "POSITION")
						vocabdict[word].yeardictsetter(text.meta['pubdate'], 1)
		return vocabdict
	
#vocab is the collection of all words in the corpus, for example stored in a dictionary
