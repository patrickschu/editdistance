import emodcorpustools as emod

corpusdir = '/Users/ps22344/Downloads/extracted_corpora_0420'
searchterm = "duke"


@emod.timer
def main(search_term, input_dir):
	t = emod.CorpusWord("terrible")
	dicti = t.yeardict(input_dir, lower_case = True)
	print len(dicti)
	print dicti.viewvalues()
	

main(searchterm, corpusdir)