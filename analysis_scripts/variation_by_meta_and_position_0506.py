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



#@timer
def variantfinder_3(input_dict, meta_data, variant_one, variant_two):
	"""
	REMEMBER TO NICIFY THIS
	The variantfinder_2 identifies words in in the input_dict that exist with both variant_1 and variant_2.
	It builds on variantfinder but adds functionality to collect variants by external factors, such as time.
	I.e. if variant_one is "u" and variant_two is "v", this will pick up on "us" and "vs".
	It returns a dictionary with the counts for each variant, the key being variant_one.
	Totaldict gives word count by meta_data category
	Add functionality for iding variation by position in word
	"""
	print "running the variantfinder_3"
	#input_dict is {word: {year1:x , year2:y ...}, word2: {}}
	#metadict collects data by meta cateogry, e.g. year
	#metadict = {year_X: {word_1: count, word_2:count, ...}, year_Y: {}}
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
			else:
				print "Alarm this is weird"
	totaldict= defaultdict(int)
	for key in metadict:
		#add totals for each year
		totaldict[key] = sum(metadict[key].values())
	# make variantonedict; variantonedict={'year':{1:{}, {2:{}}, {3:{}}
	# only non-final!
	# variantonedict = {1666 : {1:us, 2:{su:count, suu: count}, 3:suut: count, 
	variantonedict= {key:{k:v for k,v in val.items() if variant_one in list(k)} for key,val in metadict.items()}
	variantonedict= {k:v for k,v in variantonedict.items() if re.sub(variant_one, variant_two, k) in input_dict}
	varianttwodict= {key:{k:v for k,v in val.items() if variant_two in list(k)} for key,val in metadict.items()}
	varianttwodict= {k:v for k,v in varianttwodict.items() if re.sub(variant_two, variant_one, k) in input_dict}
	print "len one dict", len(variantonedict), "len two dict", len(varianttwodict)
	combineddict= defaultdict(dict)
	#clean interior dictionary of non-varying items
	#
	for entry in variantonedict:
		#print entry
		for word in variantonedict[entry]:
			print "wordiword", word
			#note that were doing len - 1 here to exclude final chars
			for pos in [i for i in range(0,len(word)-1) if word[i] == variant_one]:
				print "listi", [i for i in range(0,len(word)) if word[i] == variant_one]
				wordlist=list(word)
				variantwordlist= list(word)
				variantwordlist[pos]= variant_two
				print "word", word, "varwords", "".join(variantwordlist)
				if wordlist[pos]== variant_one and input_dict.get("".join(variantwordlist), None):
					#combineddict= {key:{pos:v for k,v in val.items()} for key,val in variantonedict.items()}
					print "here we go, word:", wordlist, "var 2", input_dict.get("".join(variantwordlist))
					#note that a missing entry in the input_dict returns a zero cause it was initialized as an int defaultdict
					if not entry in combineddict:
						combineddict[entry]={pos:{word:{"variant_one": variantonedict[entry][word], "variant_two":metadict[entry].get("".join(variantwordlist), 0)}}}
					else:
						combineddict[entry][pos] = {word:{"variant_one": variantonedict[entry][word], "variant_two":metadict[entry].get("".join(variantwordlist), 0)}}
					print "entry were making", combineddict[entry], "key:", entry
					#combineddict is : {year : {positionX : {{word: {variant_one: count, variant_two:  count}, word2 : {}}}
					#make u and v counts per year

	#k:{pos1:{var1:X, var2:X}, pos2:{}}
	yeardict= {key:{k:v.values() for k,v in value.items()} for key,value in combineddict.items()}
	#yeardict is {year:{pos: [{var1:X, var2:Y}], pos2:[]}, ...}
	finaldict= {}
	for year in yeardict:
		finaldict[year]={}
		for pos in yeardict[year]:
			#finaldict[year][pos]={}
			finaldict[year][str(pos)+'_u']=yeardict[year][pos][0]['variant_one']
			finaldict[year][str(pos)+'_v']=yeardict[year][pos][0]['variant_two']
	print "yes lets do it"
	print finaldict
	print "test on vnderstand", input_dict['vnderstand']
	print "test in understand", input_dict['understand']
	#outputdict needs to be like so: year: {position1:{variant_one: count, variant_two:count}, position2: {}}
	outputdict= defaultdict(dict)
# 	for key in combineddict:
# 		print "key", key
# 		print "vals", combineddict[key]
		
		
	
	
	#for entry in combineddict:
		
		# or do in combineddict??
		# like so:
		# combineddict = {1666 : {1:us, 2:{su:count, suu: count}, 3:suut: count, 
		#data from input_dcit comes in like so: word:{year:count}
		# ?
		
		#entry is a year
		#print combineddict[entry]
		#format is {year1:{word1:{variant_one:X, variant_two:X}, word2:{}}, year2:{}}
		#outputdict[entry]={k:{variant_one:v, variant_two:metadict[entry].get(re.sub(variant_one, variant_two, k), 0)} for k,v in combineddict[entry].items()}
	return finaldict, totaldict


		
#note that helsinki is ball parked; os are unknown
	
input_dir= '/Users/ps22344/Downloads/extracted_corpora_0420'
output_file= "xzx"

t=emod.dictbuilder_2(input_dir, 'pubdate')
u, totaldict=variantfinder_3(t, 'meta_data placeholder', 'u','v')


#reduce to 4 numbers
#deal with missing
#put into 20 year boxes
#output csv
#year:{word1:{u:x,v:x}, word2:{}}

# u={k[:4]:v for k,v in u.items()}
#print u.keys()

# for key in u:
# 	print "key", key
# 	print "vals", u[key]
# 
# yeardict={}
# for year in u:
#  	#print u[year].keys()
# # 	print [{k:v for k,v in h.items() if k == 'u'} for h in u[year].values()]
# 	#yeardict needs to look like this: year:{position:{u:count, v:count}}
# 	#ie for each year and position, sum the variant_ones to 'u', the variant_twos to 'v'
# 	#step 1
# 	#WERE HERE
# 	for word in u[year]:
# 		yeardict[year] = [counts for counts in u[year].values()]
# 	
# 	#print [[v for k,v in h.items() if k == 'u'] for h in u[year].values()]
# 	#us= [[v for k,v in h.items() if k == 'u'] for h in u[year].values()]
# 	#usum= sum([image for menuitem in us for image in menuitem])
# 	#vs= [[v for k,v in h.items() if k == 'v'] for h in u[year].values()]
# 	#vsum= sum([image for menuitem in vs for image in menuitem])
# 	#yeardict[year]= {'u':usum, 'v':vsum, 'types':len(u[year].keys()), 'totalwords': totaldict[year]}
# 
# for key in yeardict:
# 	print "key", key
# 	print "vals", yeardict[key]

df=pandas.DataFrame.from_dict(u, orient='index')

print df.columns

print list(df.columns)

print len(list(df.columns))
with codecs.open(output_file+".csv", "w") as csvout:
	df.to_csv(csvout, index_label= 'year', encoding="utf-8", na_rep="NA")

#print yeardict
print "written to", output_file