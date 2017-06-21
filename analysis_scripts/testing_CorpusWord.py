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
def main(input_dir):
	v = emod.dictbuilder(input_dir)
	emod.findvariants(v, "u", "v")

#main(corpusdir)
	
def main(input_dir):
	t = "deppski"
	r = emod.VariantItem(t, "pp")
	print r.regex



#for word in ["uu", "sup", "suup", "uussuuu"]:
	#emod.VariantItem(word).indexer("u")

from itertools import chain, combinations

def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(set(iterable))  # doesn't allow duplicate elements
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))
    
for g in powerset([1]):
	print g
	

print header

for g in powerset([1,2, 2, 3,4]):
	print g
