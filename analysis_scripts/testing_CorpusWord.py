import emodcorpustools as emod
import codecs
import pandas

header = "\n\n+++\n\n"
corpusdir = '/home/patrick/Downloads/editdistance/extracted_corpora_0420'
corpusdir = '/home/patrick/Downloads/editdistance/extracted_corpora_0420_small'
searchterm = "duke"

exclude_words = [] # ["u"]

#test CorpusWord object
@emod.timer
def main(search_term, input_dir):
	t = emod.CorpusWord("terrible", "e")
	dicti = t.yeardict(input_dir, lower_case = True)
	print dicti
	print dicti.viewvalues()


	
#main(corpusdir, "u", "v")

def main(input_dir, 
variant_one, 
variant_two,
threshold,
output_words = "testout_0711.csv",
output_aggregate = 1, 
sum_output = "True",
read_corpus_file = False):
	print "var 1", variant_one
	print "var 2", variant_two
	if read_corpus_file:
		vocab = emod.CorpusVocabImporter('/home/patrick/Downloads/editdistance/testvocab.json')
	else:
		vocab = emod.Corpus_2(input_dir).vocabbuilder(output_json = "/home/patrick/Downloads/editdistance/testvocab")
	print "len vocab ", len(vocab)
	# extract all items that contain variant one
	# NOTE change from list to string to allow several chars--> will this still work? 
	onedict = {k:v for k,v in vocab.viewitems() if variant_one in k}
	print "number of items in vocab containing variant one ", len(onedict)
	# for each word, construct a VariantItem containing all possible types with variant_two
	# this only returns items that are contained in the corpus vocab
	# Resulting typedict looks like so: {CorpusWord : {position: CorpusWord, ..}}
	onedict = {emod.VariantItem(k, variant_one, variant_two, input_vocab = vocab) : v for k,v in onedict.viewitems()}
	# onedict looks like this: {VariantItem:CorpusWord, VariantItem:CorpusWord...} where CorpusWord is a representation of the original variant_one word
	print "len onedict ", len(onedict)
	# this will give us the total tokens for each word with variant_one
	# {v.word:v.totaltokens() for k,v in onedict.viewitems()}
	# filter for the ones above threshold in for loop
	for key in onedict:
		#print "key", type(key), key.typedict
		variant_one_count = onedict[key].totaltokens()
		#print "word one", onedict[key].word.encode("utf-8"), variant_one_count
		# note that typedict is {position: CorpusWord}}
		# we exclude all entries in typedict where type_one + type_two tokens don't exceed the threshold
		# key.typedict = {k:[i for i in v.values() if i.totaltokens() + variant_one_count > threshold] for k,v in key.typedict.viewitems()}
		key.typedict = {k:[i for i in v.values() if i.totaltokens() + variant_one_count > threshold] for k,v in key.typedict.viewitems()}
		#print "keyi", key.typedict
	print "len onedict ", len(onedict)
	# remove words with empty typedictionaries, i.e. that don't have any variant_2 tokens
	onedict = {k:v for k,v in onedict.viewitems() if k.typedict.values()[0]}
	print "len onedict", len(onedict)
	# apply exclusion criteria
	onedict = {k:v for k,v in onedict.viewitems() if not any ([v.word in exclude_words])}
	print "len onedict", len(onedict)
	
	
	#print "oni", onedict
	
	print "len onedict ", len(onedict)
	print "\n".join([":".join((onedict[i].word, str(onedict[i].totaltokens()))) for i in sorted(onedict, key = lambda x : onedict[x].totaltokens(), reverse = True)][:100])
	print "\n".join([":".join((",".join([str(x) for x in i.typedict.keys()]), ",".join([",".join([",".join((y.word, str(vocab[y.word].yeardict))) for y in x]) for x in i.typedict.values()]))) for i in sorted(onedict, key = lambda x : onedict[x].totaltokens(), reverse = True)][:100])
	
	#print [i.word for i in onedict.values()]
	#print {k: [(i.word.encode("utf-8"), i.totaltokens()) for i in k.typedict.values()[0]] for k,v in onedict.viewitems()}
	#spread dict a.k.a. enter values for the words in the typedict
	#NOTE THAT ONEDICT KEYS ARE TYPE_TWO
	# really? they are variantItems and the word is always an u-type
	# update maybe it would be accurate to say they CONTAIN type 2
	for type_two in onedict:
		if len(type_two.typedict.values()) > 1:
			print "more than 1 variant for", onedict[type_two].word, type_two.typedict
	if output_words: 
		# we might consider making this into a more generalizable func
		fulldict_words = {}
		for type_two in onedict:
			# we iterate over VariantItems which are type_one: list of type 2s stored in typedict
			# typedict at this point looks like so: {type_1: [CorpusWord(type_2), ...]
			# make a key in fulldict_words for the variant_one word first, which is stored in v
			fulldict_words[onedict[type_two].word + "_base"] = onedict[type_two].yeardict
			# make keys for all the type 2s associated with it
			for typ in type_two.typedict[onedict[type_two].word]:
				# we can call this with the onedict value since this is the same type_1
				fulldict_words[onedict[type_two].word + "_" + "_".join([str(i) for i in typ.position])] = typ.yeardict
		#print [(i, fulldict_words[i]) for i in sorted(fulldict_words)][:20]
		df_fulldict_words = pandas.DataFrame.from_dict(fulldict_words)
		# note that this should include 0 if you want to have values with missing data
		# TODO: add start / end date input
		#outputindex = range (1500,1800)
		#df_fulldict_words = df_fulldict_words.reindex(outputindex)
		df_fulldict_words.to_csv(output_words + ".csv", na_rep = "NA", encoding = 'utf-8')
		print "word dict", fulldict_words
		print "Written by word counts to", output_words 
		print "DOIT", sum(df_fulldict_words.sum())
		#print "result words", fulldict_words
		# our output is like so
		# 		word1, word1_2, word2
		# 1600  count  count
		# 1601  count
		#if output_word:
			#with codecs.open(output_word + ".csv", "w", "utf-8") as csvout:
				#onedict.to_csv(csvout)
		#if output_aggregate:
			#2
		#output csv
		#\tword_pos_variant\tword\word
		#year
		#year
		#extract variation counts by year
		#"each variable is a column, each observation is a row
	if output_aggregate:
		fulldict_agg = {}
		# output:
		#	 u_0, v_0, u_1, etc
		#1600	1	2	3
		#1601	
		#{1600: {var_one : {pos1: count, pos2: count, ...}, var_two : {pos1: count,...}}
		for type_two in onedict:
			#print header, onedict[type_two].word, onedict[type_two].position
			onedict[type_two].positionsetter(tuple([ind for ind, char in enumerate(list(onedict[type_two].word)) if char == variant_one]))
			var_one_pos = "_".join(str(i) for i in onedict[type_two].position)
			# we iterate over VariantItems which are {type_one: list of type 2s} stored in `typedict`
			# cause typedict at this point looks like so: {type_1: [CorpusWord(type_2), ...]
			# make a key for the variant_one word first, which is stored in v of onedict
			#print "\n--\n"
			#print onedict[type_two].word
			#print onedict[type_two].yeardict
			for year in onedict[type_two].yeardict:
				if not year in fulldict_agg:
					# setup the year for all variants
					fulldict_agg[year] = {'base_' + var_one_pos : onedict[type_two].yeardict[year]}
					#print "set up", {variant_one : onedict[type_two].yeardict[year], variant_two : 0}
				elif not 'base_' + var_one_pos in fulldict_agg:
					fulldict_agg[year]['base_' + var_one_pos] = onedict[type_two].yeardict[year]
				else:
					#print "add to ", fulldict_agg[year]
					fulldict_agg[year]['base' + var_one_pos] += onedict[type_two].yeardict[year]
					#print "new entry", fulldict_agg[year]
					#print "from", onedict[type_two].yeardict
			for entry in type_two.typedict[onedict[type_two].word]:
				## this will give us a list of lists
				## why tf is this entry in typedict a list of lists?
				## is this necessary?
				#print "pos 2", entry.position
				var_two_pos = "_".join(str(i) for i in entry.position)
				#print var_two_pos
				for year in entry.yeardict:
					#print entry.yeardict
					if not year in fulldict_agg:
						## setup the year for all variants
						fulldict_agg[year] = {var_two_pos: 0}
						fulldict_agg[year][var_two_pos] = entry.yeardict[year]
						#print "set up", {variant_one : 0, variant_two : entry.yeardict[year]}
					elif not var_two_pos in fulldict_agg[year]:
						fulldict_agg[year][var_two_pos] =  entry.yeardict[year]
					else:
						fulldict_agg[year][var_two_pos] += entry.yeardict[year]
		#print "result", fulldict_agg
		if not sum_output: 
			df_fulldict_agg = pandas.DataFrame(fulldict_agg)
			df_fulldict_agg = df_fulldict_agg.T
			#print "result", df_fulldict_agg
			#outputindex = range (1500,1700)
			#df_fulldict_agg = df_fulldict_agg.reindex(outputindex)
			df_fulldict_agg.to_csv(output_aggregate + ".csv", na_rep = "NA", encoding = 'utf-8')
			#print df_fulldict_agg
		else:
			fulldict_agg = {k:{
				variant_one: sum([val for key, val in v.viewitems() if key.startswith("base")]),
				variant_two: sum([val for key, val in v.viewitems() if not key.startswith("base")])
				} for k,v in fulldict_agg.viewitems()}
			df_fulldict_agg = pandas.DataFrame(fulldict_agg).T
			#print df_fulldict_agg
			
		
	
	
main(corpusdir, "v", "u", threshold = 0, output_words = "output_words_VU", sum_output = False, output_aggregate = "aggout_0711")
#TO DO : check if multiple variants in typedict are preserved or kicked out asp
#numbers don't match CSV output fails, too many NAs
