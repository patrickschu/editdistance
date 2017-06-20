import emodcorpustools as emod

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
def main(input_dir):
	v = emod.dictbuilder(input_dir)
	emod.findvariants(v, "u", "v")

main(corpusdir)
	
def main(input_dir):
	t = "deppski"
	r = emod.VariantItem(t, "pp")
	print r.regex



#for word in ["uu", "sup", "suup", "uussuuu"]:
	#emod.VariantItem(word).indexer("u")
		
