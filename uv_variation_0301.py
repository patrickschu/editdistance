import emodcorpustools as emod
import re


dicti=emod.dictbuilder('/Users/ps22344/Desktop/extracted_corpora_02241')

print len(dicti)


#check out context
def variantfinder(input_dict, variant_one, variant_two):
	"""
	The variantfinder identifies words in in the input_dict that exist with both variant_1 and variant_2.
	I.e. if variant_one is "u" and variant_two is "v", this will pick up on "us" and "vs"
	"""
	print "running the variantfinder"
	tab = maketrans(variant_one, variant_two)
	outputdict= {k:v for k,v in input_dict if input_dict.get(k.translate(tab), None)} 
	
	
variantfinder(dicti, "u", "v")	
	
#def contextfinder(length)
