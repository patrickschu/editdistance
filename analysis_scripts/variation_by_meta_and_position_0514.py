#uv by category
#
from collections import defaultdict
import codecs
import json
import os
import emodcorpustools as emod
import re
import time
import pandas


#Yes, perhaps "non-initial" could be expanded into: 
#letter 2 (number of tokens), letter 3(number of tokens), letter 4(number of tokens), letter 5(number of tokens) etc., d
#depending on how feasible this is.
#today we add word output



#@timer
def variantfinder_words(input_dict, meta_data, variant_one, variant_two, token_threshold= 10):
	"""
	REMEMBER TO NICIFY THIS
	BUILT ON VARIANFIRDER 3, BUT OUTPUTS BY WORD
	The variantfinder_2 identifies words in in the input_dict that exist with both variant_1 and variant_2.
	It builds on variantfinder but adds functionality to collect variants by external factors, such as time.
	I.e. if variant_one is "u" and variant_two is "v", this will pick up on "us" and "vs".
	It returns a dictionary with the counts for each variant, the key being variant_one.
	Totaldict gives word count by meta_data category
	Add functionality for iding variation by position in word
	"""
	print "running the variantfinder_3"
	#input_dict is {word: {year1:x , year2:y ...}, word2: {}}
	variantonedict= {k:v for k,v in input_dict.items() if variant_one in list(k)}
	print "var one dict", variantonedict
	#variantonedict= {k:v for k,v in variantonedict.items() if re.sub(variant_one, variant_two, k) in input_dict}
	#we extract both vars in case input_dict is a default i.e. will return a zero 
	varianttwodict= {k:v for k,v in input_dict.items() if variant_two in list(k)}
	#print "var two dict", varianttwodict
	print "len one dict", len(variantonedict), "len two dict", len(varianttwodict)
	#totaldict is {year:totalwords, year2: totalwords,}
	#we just need it for the years
	totaldict= defaultdict(int)
	#metadict see variation_by_meta_and_position file
	metadict = {}
	#iterate over input_dict, which was produced by dictbuilder_2
	for entry in input_dict:
		#print entry
		#print input_dict[entry].keys()
		for key in input_dict[entry].keys():
			if not key in metadict:
				metadict[key]= {}
				metadict[key][entry]= input_dict[entry][key]
			elif not metadict[key].get(entry, None):
				metadict[key][entry] = input_dict[entry][key]
	for key in metadict:
		#add totals for each year
		totaldict[key] = sum(metadict[key].values())
	
	combineddict= {}
	#combineddict is {word_pos :{variant_one:{year:count, year:count, }, variant_two:{year:count, year:count}}, word2_pos:{}, word2_pos2:{}}
	for word in variantonedict:
		print "wordiword", word
		#iterate over variant in words
		for pos in [i for i in range(0,len(word)-1) if word[i] == variant_one]:
			print "this has a pos", pos, "****\n"
			#wordlist=list(word)
			variantwordlist= list(word)
			variantwordlist[pos]= variant_two
			print word, "and:", "".join(variantwordlist)
			if varianttwodict.get("".join(variantwordlist), None):
				#is this accurate???
				combineddict[word+"_"+str(pos)]= {'variant_one':variantonedict[word], 'variant_two':varianttwodict.get("".join(variantwordlist), "depp")}
	mergeddict= {}
	for word in combineddict:
		print word, combineddict[word]
		mergeddict[word+str(variant_one)]= {}
		mergeddict[word+str(variant_two)]= {}
		#add all years present in the corpus
		for year in totaldict:
			#print year
			mergeddict[word+str(variant_one)][year]= combineddict[word]['variant_one'].get(year, 0)
			mergeddict[word+str(variant_two)][year]= combineddict[word]['variant_two'].get(year, 0)
			#if combineddict[word]['variant_one'].get(year, None):
				# print "yessire", year, combineddict[word]['variant_one'].get(year, None)
				# print "in merge", mergeddict[word]['variant_one']
	finaldict= {}
	for entry in mergeddict:
		if (
		entry.endswith(variant_one)
		) and (
		sum(mergeddict[entry].values()) + sum(mergeddict[entry.rstrip(variant_one)+variant_two].values()) > token_threshold):
			print "yiipi", "***", entry
			print "sum 1", sum(mergeddict[entry].values()) , "sum 2", sum(mergeddict[entry.rstrip(variant_one)+variant_two].values())
			finaldict[entry]= mergeddict[entry]
			finaldict[entry.rstrip(variant_one)+variant_two]= mergeddict[entry.rstrip(variant_one)+variant_two]
		
	#print finaldict	
	return finaldict, totaldict
#note that helsinki is ball parked; os are unknown
	
input_dir= '/home/ps22344/Downloads/extracted_corpora_0420'
output_file= "innsbruck_test"

t=emod.dictbuilder_2(input_dir, 'pubdate')
#print "t keys", t.keys()
u, totaldict=variantfinder_words(t, 'meta_data placeholder', 'u','v', 1000)


df=pandas.DataFrame.from_dict(u)

#print df.columns

#print list(df.columns)

print len(list(df.columns))
df.to_csv(output_file+".csv", encoding="utf-8", na_rep="NA")

#print yeardict
print "written to", output_file