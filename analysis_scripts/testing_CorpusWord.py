import emodcorpustools as emod
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

def main(input_dir, variant_one, variant_two, threshold = 0):
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
	# remove words with empty typedictionaries, i.e. that don't have any variant_2 tokens
	onedict = {k:v for k,v in onedict.viewitems() if k.typedict.values()[0]}
	print "len onedict ", len(onedict)
	# this will give us the total tokens for each word with variant_one
	# {v.word:v.totaltokens() for k,v in onedict.viewitems()}
	# filter for the ones above threshold
	for key in onedict:
		variant_one_count = onedict[key].totaltokens()
		print "word one", onedict[key].word, variant_one_count
		key.typedict = {k:[i.totaltokens() for i in v.values()] for k,v in key.typedict.viewitems()}
	print "len onedict ", len(onedict)
	print {k: k.typedict for k,v in onedict.viewitems()}
	#extract word counts over the years for each word over threshold
	#extract variation counts by year
	

	
main(corpusdir, "u", "v")
