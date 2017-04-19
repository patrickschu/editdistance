#uv by category
#
from collections import defaultdict
import codecs
import json
import os
import emodcorpustools as emod

def variantfinder_2(input_dict, variant_one, variant_two):
	"""
	The variantfinder_2 identifies words in in the input_dict that exist with both variant_1 and variant_2.
	It builds on variantfinder but adds functionality to collect variants by external factors, such as time.
	I.e. if variant_one is "u" and variant_two is "v", this will pick up on "us" and "vs".
	It returns a dictionary with the counts for each variant, the key being variant_one.
	"""
	print "running the variantfinder"
	variantonedict= {k:v for k,v in input_dict.items() if variant_one in list(k)}
	outputdict= {}
	for entry in variantonedict:
		if input_dict.get(re.sub(variant_one, variant_two, entry), None):
			outputdict[entry]={variant_one:variantonedict[entry], variant_two:input_dict[re.sub(variant_one, variant_two, entry)]}
	return outputdict
	
	
	
def dictbuilder_2(input_dir, meta_data, output_json=False):
	"""
	Builds a dictionary of all texts in input_dir.
	Builds on dictbuilder but adds functionality to collect by external factors such as date.
	Format: {word: {year: count, year:count, year:count}, word: {}}
	"""
	dicti=defaultdict(dict)
	for w in os.walk(input_dir):
		folder=w[0]
		print "folder", folder 
		for fili in [i for i in w[2] if i.endswith(".txt")]:
			text= emod.CorpusText(os.path.join(input_dir, folder, fili))
			meta= text.meta[meta_data]
			for word in text.tokenizer(cleantext=True):
				#dicti[word.lower()]= dicti[word.lower()]+1
				x=1
	if output_json:
		with codecs.open(output_json+".json", "w") as jsonout:
			json.dump(dicti, jsonout, encoding= "utf-8")
		print "File written to", jsonout
	print "\n".join([":".join((i, str(dicti[i]))) for i in sorted(dicti, key= dicti.get, reverse=True)[:100]])
	return dicti
	

dictbuilder_2('/Users/ps22344/Downloads/extracted_corpora_0224', 'pubdate')