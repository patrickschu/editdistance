#uv by category
#
from collections import defaultdict
import codecs
import json
import os
import emodcorpustools as emod
import re
import time


def timer(func):
	def wrapper(*args, **kwargs):
		t = time.time()
		res = func(*args, **kwargs)
		print "{} took us {}".format(func.func_name, time.time()-t)
		return res
	return wrapper

@timer
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
				print "Alarm this is weird"
	for key in metadict:
		#add totals for each year
		metadict[key]['total'] = sum(metadict[key].values())
	variantonedict= {key:{k:v for k,v in val.items() if variant_one in list(k)} for key,val in metadict.items()}
	#clean interior dictionary of non-varying items
	combineddict= {key:{k:v for k,v in val.items() if re.sub(variant_one, variant_two, k) in input_dict} for key,val in variantonedict.items()}
	for key in t:
		print key, t[key]
# 	print input_dict.keys()
	outputdict= {}
	for entry in combineddict:
		#entry is a year
		print combineddict[entry]
		#outputdict[entry]={variant_one:variantonedict[entry], variant_two:input_dict[re.sub(variant_one, variant_two, entry)]}
		outputdict[entry]={k:{variant_one:v, variant_two:metadict[entry].get(re.sub(variant_one, variant_two, k), 0)} for k,v in combineddict[entry].items()}
	print outputdict	
	return outputdict
	
	
	


t=emod.dictbuilder_2('/Users/ps22344/Downloads/extracted_corpora_0224', 'pubdate')
u=variantfinder_2(t, 'meta_data placeholder', 'u','v')
print u.values()
