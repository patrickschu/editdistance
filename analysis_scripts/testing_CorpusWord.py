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

#test Dictbuilder
@emod.timer
def main(input_dir, variant_one, variant_two):
	vocab = emod.Corpus_2(corpusdir).vocabbuilder(output_json = "testvocab")
	print "len vocab ", len(vocab)
	onedict = {k:v for k,v in vocab.viewitems() if variant_one in list(k)}
	print "len onedict ", len(onedict)
	onedict = {emod.VariantItem(k, variant_one, variant_two, input_vocab = vocab) : v for k,v in onedict.viewitems()}
	print {k.word : k.typedict for k,v in onedict.viewitems() if k.typedict.values() != [set([])]}
	#check if set deletes non-ID CorpusWords -- apparently it does not
	print {k.word : k.typedict.values() for k,v in onedict.viewitems() if k.typedict.values() != [set([])]}
	
	
	#emod.findvariants(v, "u", "v")

main(corpusdir, "u", "v")
	

		
