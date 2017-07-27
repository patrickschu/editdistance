#!/usr/bin/env python

import emodcorpustools as emod
import codecs
import pandas
import argparse
import json


def get_input():
	parser = argparse.ArgumentParser()
	#add args
	parser.add_argument("variant_one", type=str, help="Enter character(s) representing the first variant")
	parser.add_argument("variant_two", type=str, help="Enter character(s) representing the second variant")
	parser.add_argument("--read_corpusfile", type=str, 
		help="Enter name of json file containing wordcounts created previously")
	parser.add_argument("--read_wordlist", type=str, 
		help="Enter name of JSON file containing a dictionary of words to check for, i.e. a pre-defined vocabulary")
	parser.add_argument("--input_dir", type=str, help="Enter the directory containing a corpus of .txt files to read")
	parser.add_argument("--write_corpusfile", type=str, help="Enter name of file to write word counts per year to (in JSON), created from input_directory")
	#OPTIONAL ARGS
	#note that we can do the file input options as actions in one variable
	parser.add_argument("--lemmatize", action="store_true", dest = 'lemmatize', help = "OPTIONAL: Remove suffixes from words. Right now, word-final 's' is removed")
	#parser.add_argument('-w', action='store_true')
	parser.add_argument("--threshold", type=int, 
		help="OPTIONAL: Enter the minimum number of tokens varying between variant_one and variant_two that need to be present to be included in the output. Defaults to '0'")
	parser.add_argument("--timespan", type=str, help="OPTIONAL: Enter a start and end year for the output, seperated by a comma. Format: 'beginning,end'")
	parser.add_argument("--verbose", action="store_true", type=bool, help="OPTIONAL: Set to 'True' for complete printout")
	#output options
	parser.add_argument("--output_words", type=str, help="Enter file name to write csv of token counts per word and position")
	parser.add_argument("--output_position", type=str, help="Enter file name to write csv of token counts per position in the word")
	parser.add_argument("--output_aggregate", type=str, help="Enter file name to write csv of token counts per variant and year")
	#read input
	args = parser.parse_args()
	return args



header = "\n\n+++\n\n"
corpusdir = '/home/patrick/Downloads/editdistance/extracted_corpora_0420'
corpusdir = '/home/patrick/Downloads/editdistance/extracted_corpora_0420_small'
searchterm = "duke"

exclude_words = [] # ["u"]

#test CorpusWord object

def filti(x):
	# returns hash, and attributes for groupby by word positions for output_agg
	word, attr = x
	return attr.__hash__(), attr

def csvwriter(data_frame, file_name, new_index = False):
	# write DataFrame to csv
	if new_index:
		print "Output data limited to {} - {}".format(str(new_index[0]), str(new_index[1]))
		new_index = range(new_index[0], new_index[1])
		data_frame = data_frame.reindex(new_index)
	data_frame.to_csv(file_name + ".csv", na_rep = "NA", encoding = 'utf-8')
	print "File written to {}".format(file_name + ".csv")

	
#main(corpusdir, "u", "v")

def main():

	args = get_input()
	# checking input
	if not args.input_dir:
		raise IOError("No corpus provided. You need specify a directory of text files with --input_dir")
	#if all([not args.read_corpusfile, not args.read_wordlist]):
		#raise IOError("No input data. You need to either specify a word list '--read_wordlist' or a file with word counts as '--read_file'")
	# note that timespan should include 0 if you want to have values with missing data
	if args.timespan:
		# turns input into [str, str] list
		timespan = [int(i) for i in args.timespan.split(",")]
	elif not args.timespan:
		timespan = args.timespan
	
	# set up vars
	# maybe improve to: var1, var2, output_method, ... = args.x,args.y
	variant_one = args.variant_one
	variant_two = args.variant_two
	threshold = args.threshold
	verbose = args.verbose
	input_dir = args.input_dir
	lemmatize = args.lemmatize
	print "Working with variant_one: '{}', variant_two: '{}'".format(variant_one,variant_two)
	print "Lemmatize is set to", lemmatize
	
	# pick data input method
	if args.read_corpusfile:
		vocab = emod.CorpusVocabImporter(args.read_corpusfile)
	if args.read_wordlist:
		with codecs.open(args.read_wordlist, "r", "utf-8") as wordlist_in:
			#use the CorpusVocabImporter here instead
			wordlist = emod.CorpusVocabImporter(args.read_wordlist)
			#Importer returns {word:CorpusWord(word), ...}
		# do we really need the extra list setting if we just import it as a VocabImporter
		vocab = emod.Corpus_2(input_dir).vocabbuilder(use_word_list = wordlist, lemmatize = lemmatize, output_json = args.write_corpusfile)
		print "Reading data from wordlist {}, length: {}".format(args.read_wordlist, len(vocab))
	else:
		print "Building vocab from", input_dir
		vocab = emod.Corpus_2(input_dir).vocabbuilder(lemmatize = lemmatize, output_json = args.write_corpusfile)
		
	print "Length corpusfile ", len(vocab)
	# extract all items that contain variant one
	# note that we could do this during extraction if we had been smart; but vocab output would break
	onedict = {k:v for k,v in vocab.viewitems() if variant_one in k}
	print "Number of items in corpusfile containing variant one ", len(onedict)
	# for each word, construct a VariantItem containing all possible types with variant_two
	# this only returns items that are contained in the corpus vocab
	# Resulting typedict looks like so: {CorpusWord : {position: CorpusWord, ..}}
	
	
	###
	if args.read_wordlist:
		#we run the variants against wordlist, setting input to the wordlist
		print "asissis"
		onedict = {emod.VariantItem(k, variant_one, variant_two, input_vocab = vocab, word_list = wordlist) : v for k,v in onedict.viewitems()}
	###
	
	else:
		# we run the variants against the corpus vocab, setting input the vocab previously constructed
		onedict = {emod.VariantItem(k, variant_one, variant_two, input_vocab = vocab) : v for k,v in onedict.viewitems()}
	# onedict looks like this: {VariantItem:CorpusWord, VariantItem:CorpusWord...} where CorpusWord is a representation of the original variant_one word
	print "we done making variantitems"

	# this will give us the total tokens for each word with variant_one
	# {v.word:v.totaltokens() for k,v in onedict.viewitems()}
	# filter for the ones above threshold in for loop
	print "run key loop"
	for key in onedict:
		#print "key", type(key), key.typedict
		variant_one_count = onedict[key].totaltokens()
		#print "word one", onedict[key].word.encode("utf-8"), variant_one_count
		# note that typedict is {position: CorpusWord}}
		# we exclude all entries in typedict where type_one + type_two tokens don't exceed the threshold
		# key.typedict = {k:[i for i in v.values() if i.totaltokens() + variant_one_count > threshold] for k,v in key.typedict.viewitems()}
		key.typedict = {k:[i for i in v.values() if i.totaltokens() + variant_one_count > threshold] for k,v in key.typedict.viewitems()}
		#print "keyi", key.typedict
	print "len onedict ", len(onedict)
	# remove words with empty typedictionaries, i.e. that don't have any variant_2 tokens
	if not args.read_wordlist:
		onedict = {k:v for k,v in onedict.viewitems() if k.typedict.values()[0]}
	else:
		onedict = {k:v for k,v in onedict.viewitems() if k.typedict.values()[0]}
	print "len onedict after removing zero counts", len(onedict)
	print "Number of items in corpusfile containing variant one and variant two", len(onedict)
	# apply exclusion criteria
	onedict = {k:v for k,v in onedict.viewitems() if not any ([v.word in exclude_words])}
	print "len onedict", len(onedict)
	print "len onedict ", len(onedict)
	if verbose:
		print "Summary dictionary"
		print "\n".join([":".join((onedict[i].word, str(onedict[i].totaltokens()))) for i in sorted(onedict, key = lambda x : onedict[x].totaltokens(), reverse = True)][:20])
		print "\n".join([":".join((",".join([str(x) for x in i.typedict.keys()]), ",".join([",".join([",".join((y.word, str(vocab[y.word].yeardict))) for y in x]) for x in i.typedict.values()]))) for i in sorted(onedict, key = lambda x : onedict[x].totaltokens(), reverse = True)][:20])
	# catch oddities
	for type_two in onedict:
		if len(type_two.typedict.values()) > 1:
			print "more than 1 variant for", onedict[type_two].word, type_two.typedict
	# we set up the entire shenanigan
	fulldict_words = {}
	for type_two in onedict:
		# we iterate over VariantItems which are type_one: list of type 2s stored in typedict
		# typedict at this point looks like so: {type_1: [CorpusWord(type_2), ...]
		# make a key in fulldict_words for the variant_one word first, which is stored in v
		fulldict_words[onedict[type_two].word + "_('base',)"] = onedict[type_two].yeardict
		# make keys for all the type 2s associated with it
		for typ in type_two.typedict[onedict[type_two].word]:
			# we can call this with the onedict value since this is the same type_1
			fulldict_words[onedict[type_two].word + "_" + str(typ.position)] = typ.yeardict
	# print [(i, fulldict_words[i]) for i in sorted(fulldict_words)][:20]
	df_fulldict_words = pandas.DataFrame.from_dict(fulldict_words)
	df_fulldict_words.index = df_fulldict_words.index.map(int)

	# our output is like so
	# 		word_(1,) word_(1,2), word2
	# 1600  count  count
	# 1601  count
	if args.output_words: 
		df_fulldict_words_out = df_fulldict_words.copy()
		#print "cols", df_fulldict_words.columns
		newcols = ["_".join((unicode(w), "_".join(str(pos) for pos in eval(m)))) for w,m in [i.rsplit("_", 1) for i in df_fulldict_words_out.columns]]
		print newcols
		df_fulldict_words_out.columns = newcols
		csvwriter(df_fulldict_words_out, args.output_words, new_index = timespan)

	# set up for indexing columns
	splitcols = [(w, eval(m)) for w,m in [i.rsplit("_", 1) for i in df_fulldict_words.columns]]
	df_fulldict_words.columns = splitcols
	
	# transform to other ends
	if args.output_position:
		# this outputs like so:
		#       (base,)  (0,)  (1,)   (2,)  (3,)  (5,)
		#1641     20.0  13.0   1.0   99.0   NaN   NaN
		#1642     20.0   5.0   NaN   90.0   1.0   NaN
		#1643      8.0  10.0  11.0   23.0   4.0   NaN
		#1644     44.0  27.0   NaN   99.0   NaN   4.0
		df_agg_by_year_and_pos_out = df_fulldict_words.copy()
		df_agg_by_year_and_pos = df_agg_by_year_and_pos_out.groupby(lambda x: filti(x), axis = 1).sum()
		df_agg_by_year_and_pos.columns = ["_".join((str(pos) for pos in i[1])) for i in df_agg_by_year_and_pos.columns]
		if verbose:
			print df_agg_by_year_and_pos
		csvwriter(df_agg_by_year_and_pos, args.output_position, new_index = timespan) 
	
	if args.output_aggregate:
		# this outputs like so:
		#         u      v
		#	1641  20.0  113.0
		#	1642  20.0   96.0
		#	1643   8.0   48.0
		#	1644  44.0  130.0
		df_agg_by_year_out = df_fulldict_words.copy()
		df_agg_by_year = df_agg_by_year_out .groupby(lambda x: isinstance(filti(x)[1][0], str), axis = 1).sum()
		df_agg_by_year.columns = [variant_one if i else variant_two for i in df_agg_by_year.columns]
		if verbose:
			print df_agg_by_year
		csvwriter(df_agg_by_year, args.output_aggregate, new_index = timespan)
	
	
#main(corpusdir, "v", "u", read_corpus_file = False, threshold = 0, output_words = "output_words_VU", sum_output = "deppski", output_aggregate = "aggout_0711")

if __name__ == "__main__":
    main()
