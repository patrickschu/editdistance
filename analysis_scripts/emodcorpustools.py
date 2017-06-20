import os
import re
import codecs
import nltk.tokenize
#import pandas
import string
import time
import json
from collections import defaultdict

header = "\n+++++\n"

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
def timer(func):
	def wrapper(*args, **kwargs):
		t = time.time()
		print "Running {}".format(func.func_name)
		res = func(*args, **kwargs)
		print "{} took us {}".format(func.func_name, time.time()-t/60)
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
	
	def tokenizer(self, cleantext=False):
		if cleantext:
			return [i for i in nltk.word_tokenize(self.cleantext) if not i in string.punctuation]
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


class VariantItem(object):
	"""
	This compiles the potential variants of a word
	"""
	def __init__(self, word):
		self.word = word
		
	def indexer(self, variant):
		#finds instances of variant in self.word
		#NOTE THAT THIS WILL NOT SPLIT UP 3 CHAR STRETCHES WHEN LOOKING FOR 2 CHARS, e.g. "uuu" will be one instance of "uu", not 2
		word = self.word
		index = 0
		print word
		while index < len(word):
			index = word.find(variant, index)
			if index == -1:
				break
			print(variant, 'found at', index)
			index = index + len(variant)
		

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
	position : 1
	"""
	def __init__(self, word, variant, position):
		self.word = word
		self.variant = variant
		self.position = position
		self.length = len(word)
	#integrate variation by position
	# do we need?
	@timer
	def yeardict(self, input_dir, lower_case = False):
		#yeardict compiles counts of self.word by year across all texts in input_dir
		#if lower_case, texts in input_dir will be lower cased. 
		#NOTE THAT THE DEFDICT WILL DEFAULT TO 0; I.E no EMPTY KEYS
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
					pubdate = "".join([i for i in list(inputtext.meta['pubdate']) if i.isdigit()][:4])
					tokensperyear[pubdate] = tokensperyear[pubdate] + 1
		return(tokensperyear)
		# we can model other flexible word counts on this: just give attribute to sort by as argument. 
		# smooth. 			
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
	subregex = re.compile(variant_one)
	onedict = {k:v for k,v in input_vocab.viewitems() if variant_one in list(k)}
	#matches replacing all "u"s
	onetwodict = {CorpusWord(k, variant_one):v for k,v in onedict.viewitems() if input_vocab.get(re.sub(variant_one, variant_two, k), None)}
	#for key in onetwodict:
		
	#if threshold ! = 0:
		#outputdict = {k:v for k,v in onetwodict.viewitems if 
	#else:
		#outputdict = onetwodict
	print onetwodict
	
	
	
	
#class Dataset(object):
	#def __init__(self, input_dir):
		#self.name = input_dir
	
	##compute all words
	
	
	##compute mean etc
	
	
	##compute words by year, etc. 
	#def countbyexternality(self, input_dir, attribute ot CorpusText to groupBy, lower_case = False):
		#1


class Corpus(object):
	"""
	The Corpus object compiles all relevant info for an entire corpus. 
	It reads in a tab-separated spreadsheet. 
	WHAT KIND OF SPREADSHEET ETC
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


