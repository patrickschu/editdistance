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
	#vocab = emod.Corpus_2(corpusdir).vocabbuilder(output_json = "testvocab")
	vocab = emod.CorpusVocabImporter('/home/patrick/Downloads/editdistance/testvocab.json')
	print "len vocab ", len(vocab)
	onedict = {k:v for k,v in vocab.viewitems() if variant_one in list(k)}
	print "len onedict ", len(onedict)
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
		print type(key), key.typedict
		variant_one_count = onedict[key].totaltokens()
		#print "word one", onedict[key].word.encode("utf-8"), variant_one_count
		# note that typedict is {position: CorpusWord}}
		# we exclude all entries in typedict where type_one + type_two tokens don't exceed the threshold
		#key.typedict = {k:[i for i in v.values() if i.totaltokens() + variant_one_count > threshold] for k,v in key.typedict.viewitems()}
		key.typedict = {k:[i for i in v.values() if i.totaltokens() + variant_one_count > threshold] for k,v in key.typedict.viewitems()}
		print "keyi", key.typedict
	print "len onedict ", len(onedict)
	# remove words with empty typedictionaries, i.e. that don't have any variant_2 tokens
	onedict = {k:v for k,v in onedict.viewitems() if k.typedict.values()[0]}
	print "len onedict ", len(onedict)
	#print {k: [(i.word.encode("utf-8"), i.totaltokens()) for i in k.typedict.values()[0]] for k,v in onedict.viewitems()}
	#spread dict a.k.a. enter values for the words in the typedict
	#NOTE THAT ONEDICT KEYS ARE TYPE_TWO
	for type_two in onedict:
		# print "typpi 2", type_two.typedict
		x=1
	onedict = pandas.DataFrame.from_dict(onedict)
	if output_word:
		with codecs.open(output_word + ".csv", "w", "utf-8") as csvout:
			onedict.to_csv(csvout)
	if output_aggregate:
		2
	#output csv
	#\tword_pos_variant\tword\word
	#year
	#year
	#extract variation counts by year
	#"each variable is a column, each observation is a row

	
main(corpusdir, "u", "v", threshold = 0, output_word = "testingcsvout", output_aggregate = False)
