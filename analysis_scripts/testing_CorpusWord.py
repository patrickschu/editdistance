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
	
def main(input_dir):
	t = "deppski"
	r = emod.VariantItem(t, "pp")
	print r.regex

#main(corpusdir)

def indexer(word, variant):
	text = word
	index = 0
	while index < len(text):
		index = text.find(self.variant, index)
		if index == -1:
			break
		print('thing found at', index)
		index = index + len(variant)
		
indexer("spasst", "s")
