import emodcorpustools as emod
import re
import json
import codecs
from string import maketrans


#dicti=emod.dictbuilder('/Users/ps22344/Desktop/extracted_corpora_02241', output_csv=True)



with codecs.open("dictbuilder_output.json", "r", "utf-8") as inputjson:
	dicti = json.load(inputjson)

print "lenght dicti", len(dicti)


tab = maketrans("u", "v")
for k in dicti.keys():
	print k,k.encode("utf-8").translate(tab)

#check out context
def variantfinder(input_dict, variant_one, variant_two):
	"""
	The variantfinder identifies words in in the input_dict that exist with both variant_1 and variant_2.
	I.e. if variant_one is "u" and variant_two is "v", this will pick up on "us" and "vs"
	"""
	print "running the variantfinder"
	variantonedict= {k:v for k,v in input_dict.items() if variant_one in list(k)}
	outputdict= {}
	for entry in variantonedict:
		if input_dict.get(re.sub(variant_one, variant_two, entry), None):
			outputdict[entry]={variant_one:variantonedict[entry], variant_two:input_dict[re.sub(variant_one, variant_two, entry)]}
	for i in outputdict:
		print i, outputdict[i]
			
	
variantfinder(dicti, "u", "v")	
	
#def contextfinder(length)
