#!/usr/bin/env python

import emodcorpustools as emod
import re
import json
import codecs
from collections import defaultdict
import sys

#building a dict
#dicti=emod.dictbuilder('/Users/ps22344/Desktop/extracted_corpora_02241', output_csv=True)

	

def main(variant_one, variant_two, input_dict, pre_window, post_window, differential_cutoff=100):
	"""
	Takes the two variants plus an input_dict (json file) with the vocab to go over.
	"""
	pre_window = int(pre_window)
	post_window = int(post_window)
	
	
	with codecs.open(input_dict, "r", "utf-8") as inputjson:
		dicti = json.load(inputjson)
	print "length dicti", len(dicti)
	print "running with differential_cutoff at", differential_cutoff
	#find all variants
	variantdict= emod.variantfinder(dicti, variant_one, variant_two)	

	#establish their context, compile in dict
	#{((u'a',), (u'e',)): {'count': 2, 'u': 1, 'v': 1}
	contextdict=defaultdict(dict)
	for entry in variantdict:
		for g in emod.contextfinder(entry, variant_one, pre_window, post_window):
			if not contextdict.get(g, None):
				contextdict[g]={
				variant_one: variantdict[entry][variant_one],
				variant_two: variantdict[entry][variant_two],
				'count': variantdict[entry][variant_one]+variantdict[entry][variant_two]
				}

	total= float(sum([v['count'] for v in contextdict.values()]))
	print "contextdict has {} different contexts, with a total of {} tokens".format(len(contextdict), total)
	
	#print most frequent contexts
	#how they split up over variants 	
	header="\n****\n"
	
	contextdict = {k:v for k,v in contextdict.items() if abs(contextdict[k][variant_one]/float(contextdict[k]['count']) - contextdict[k][variant_two]/float(contextdict[k]['count'])) < float(differential_cutoff)/100}
	print contextdict
	print header, "MOST FREQUENT CONTEXTS of {} - {} variation (token counts < 10 excluded)".format(variant_one, variant_two), header
	for item in sorted({k:v for k,v in contextdict.items() if v['count'] > 9}, key= lambda x : contextdict[x]['count'], reverse=True):
		print "{context}\ttokens: {count}\t{percentoverall:.4}% of total,{var1}: {percentvar1:.4}%, {var2}: {percentvar2:.4}%".format(
		context= "_".join("".join(i) for i in item).encode('utf-8'), 
		count= contextdict[item]['count'], 
		percentoverall= contextdict[item]['count']/total*100,
		percentvar1= contextdict[item][variant_one]/float(contextdict[item]['count'])*100, 
		var1=variant_one.encode('utf-8'), 
		percentvar2= contextdict[item][variant_two]/float(contextdict[item]['count'])*100, 
		var2= variant_two.encode('utf-8')) 
	
	#print most one-sided contexts
	#how they split up over variants 
	print header, "HIGHEST DIFFERENTIAL IN VARIANT USE of {} - {} variation (token counts < 10 excluded)".format(variant_one, variant_two)		
	for item in sorted({k:v for k,v in contextdict.items() if v['count'] > 9}, key= lambda x : abs(contextdict[x][variant_one]/float(contextdict[x]['count']) - contextdict[x][variant_two]/float(contextdict[x]['count'])), reverse=True):
		print "{context}\ttokens: {count}\t{percentoverall:.4}% of total,{var1}: {percentvar1:.4}%, {var2}: {percentvar2:.4}%".format(
		context= "_".join("".join(i) for i in item).encode('utf-8'), 
		count= contextdict[item]['count'], 
		percentoverall= contextdict[item]['count']/total*100,
		percentvar1= contextdict[item][variant_one]/float(contextdict[item]['count'])*100, 
		var1=variant_one.encode('utf-8'), 
		percentvar2= contextdict[item][variant_two]/float(contextdict[item]['count'])*100, 
		var2= variant_two.encode('utf-8')) 


if __name__ == '__main__':
    main(*sys.argv[1:])
    
    
    
#main("u", "v", 'dictbuilder_output.json')

