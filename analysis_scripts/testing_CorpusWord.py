import emodcorpustools as emod
import codecs
import pandas

header = "\n\n+++\n\n"
corpusdir = '/Users/ps22344/Downloads/extracted_corpora_0420'
corpusdir = '/home/patrick/Downloads/editdistance/extracted_corpora_0420_small'
searchterm = "duke"



#test CorpusWord object
@emod.timer
def main(search_term, input_dir):
	t = emod.CorpusWord("terrible", "e")
	dicti = t.yeardict(input_dir, lower_case = True)
	print dicti
	print dicti.viewvalues()


	#check if set deletes non-ID CorpusWords -- apparently it does not
	
#main(corpusdir, "u", "v")

def main(input_dir, variant_one, variant_two, threshold, output_word, output_aggregate):
	# build vocab anew:
	vocab = emod.Corpus_2(corpusdir).vocabbuilder(output_json = "/home/patrick/Downloads/editdistance/testvocab")
	# read vocab from file:
	vocab = emod.CorpusVocabImporter('/home/patrick/Downloads/editdistance/testvocab.json')
	print "len vocab ", len(vocab)
	# extract all items that contain variant one
	# NOTE change from list to string to allow several chars--> will this still work? 
	onedict = {k:v for k,v in vocab.viewitems() if variant_one in k}
	print "number of items in vocab containing variant one ", len(onedict)
	# for each word, construct a VariantItem containing all possible types with variant_two
	# this only returns items that are contained in the corpus vocab
	# Resulting typedict looks like so: {CorpusWord : {position: CorpusWord, ..}}
	onedict = {emod.VariantItem(k, variant_one, variant_two, input_vocab = vocab) : v for k,v in onedict.viewitems()}
	# onedict looks like this: {VariantItem:CorpusWord, VariantItem:CorpusWord...} where CorpusWord is a representation of the original variant_one word
	print "len onedict ", len(onedict)
	# this will give us the total tokens for each word with variant_one
	# {v.word:v.totaltokens() for k,v in onedict.viewitems()}
	# filter for the ones above threshold in for loop
	for key in onedict:
		print "key", type(key), key.typedict
		variant_one_count = onedict[key].totaltokens()
		print "word one", onedict[key].word.encode("utf-8"), variant_one_count
		# note that typedict is {position: CorpusWord}}
		# we exclude all entries in typedict where type_one + type_two tokens don't exceed the threshold
		# key.typedict = {k:[i for i in v.values() if i.totaltokens() + variant_one_count > threshold] for k,v in key.typedict.viewitems()}
		key.typedict = {k:[i for i in v.values() if i.totaltokens() + variant_one_count > threshold] for k,v in key.typedict.viewitems()}
		print "keyi", key.typedict
	print "len onedict ", len(onedict)
	# remove words with empty typedictionaries, i.e. that don't have any variant_2 tokens
	onedict = {k:v for k,v in onedict.viewitems() if k.typedict.values()[0]}
	print "len onedict ", len(onedict)
	#print [i.word for i in onedict.values()]
	#print {k: [(i.word.encode("utf-8"), i.totaltokens()) for i in k.typedict.values()[0]] for k,v in onedict.viewitems()}
	#spread dict a.k.a. enter values for the words in the typedict
	#NOTE THAT ONEDICT KEYS ARE TYPE_TWO
	# really? they are variantItems and the word is always an u-type
	# update maybe it would be accurate to say they CONTAIN type 2
	for type_two in onedict:
		if len(type_two.typedict.values()) > 1:
			print "more than 1 variant for", onedict[type_two].word, type_two.typedict
			x=1
	fulldict_words = {}
	for type_two in onedict:
		# we iterate over VariantItems which are type_one: list of type 2s stored in typedict
		# typedict at this point looks like so: {type_1: [CorpusWord(type_2), ...]
		
		# make a key for the variant_one word first, which is stored in v
		fulldict_words[onedict[type_two].word + "baseform"] = onedict[type_two].yeardict
		# make keys for all the type 2s associated with it
		for typ in type_two.typedict[onedict[type_two].word]:
			# we can call this with the onedict value since this is the same type_1
			fulldict_words[onedict[type_two].word + "_" + str(typ.position)] = typ.yeardict
	print [(i, fulldict_words[i]) for i in sorted(fulldict_words)]
	df_fulldict_words = pandas.DataFrame.from_dict(fulldict_words)
	print df_fulldict_words
	print df_fulldict_words.index
	print type(df_fulldict_words.index)
	newindex = range (0,20000)
	gg = df_fulldict_words.reindex(newindex)
	print gg
	#df_fulldict_words.to_csv("testout.csv", encoding = 'utf-8')
	# our output is like so
	# 		word1, word1_2, word2
	# 1600  count  count
	# 1601  count
	#if output_word:
		#with codecs.open(output_word + ".csv", "w", "utf-8") as csvout:
			#onedict.to_csv(csvout)
	#if output_aggregate:
		#2
	#output csv
	#\tword_pos_variant\tword\word
	#year
	#year
	#extract variation counts by year
	#"each variable is a column, each observation is a row

	
main(corpusdir, "u", "v", threshold = 0, output_word = "testingcsvout", output_aggregate = False)
#TO DO : check if multiple variants in typedict are preserved or kicked out asp
