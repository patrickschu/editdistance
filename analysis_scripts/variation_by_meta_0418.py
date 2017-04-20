#uv by category
#
from collections import defaultdict
import codecs
import json
import os
import emodcorpustools as emod
import re

def variantfinder_2(input_dict, meta_data, variant_one, variant_two):
	"""
	The variantfinder_2 identifies words in in the input_dict that exist with both variant_1 and variant_2.
	It builds on variantfinder but adds functionality to collect variants by external factors, such as time.
	I.e. if variant_one is "u" and variant_two is "v", this will pick up on "us" and "vs".
	It returns a dictionary with the counts for each variant, the key being variant_one.
	"""
	print "running the variantfinder_2"
	metadict = defaultdict(dict)
	for entry in input_dict:
		print entry
		print input_dict[entry].keys()
		for key in input_dict[entry].keys():
			if not metadict[key].get(entry, None):
				metadict[key][entry] = input_dict[entry][key]
			else:
				#can this ever happen? No. 
				metadict[key][entry] = metadict[key][entry] + input_dict[entry][key]
			
			
			
	#print [i.values() for i in metadict.values()]
	print metadict
	variantonedict= {k:v for k,v in input_dict.items() if variant_one in list(k)}
	#print variantonedict
	outputdict= {}
	for entry in variantonedict:
		if input_dict.get(re.sub(variant_one, variant_two, entry), None):
			outputdict[entry]={variant_one:variantonedict[entry], variant_two:input_dict[re.sub(variant_one, variant_two, entry)]}
	return outputdict
	
	
	


t=emod.dictbuilder_2('/Users/ps22344/Downloads/extracted_corpora_0224', 'pubdate')
t['ulli']={1700:10}
u=variantfinder_2(t, 'meta_data placeholder', 'u','v')
#print u.values()