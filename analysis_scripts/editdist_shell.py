import nltk
from nltk import edit_distance
from collections import defaultdict
import codecs
import os
import re
import sys


header= "\n\n***\n"

def spellfinder(word, text, distance):
	"""
	word is a word string. 
	text is a tokenized list of words.
	distance is the longest edit distance to be returned>
	"""
	print "We have {} words in the text, distance is set to {} for '{}'".format(len(text), distance, word)
	#print text
	result=[i for i in text if (nltk.edit_distance(word, i) <= distance) and (nltk.edit_distance(word, i) > 0)]
	print "results", result
	print "number of items", len(result)
	if len(result) > 0:
		resultset=set(result)
		#print "result: ", result
		print "{} matches".format(len(list(resultset)))
	return result
		
	

def main(wordlist, input_dir, distance):
	countdict=defaultdict(float)
	worddict=defaultdict(list)
	#reading in the wordlist
	with codecs.open(wordlist, "r", "utf-8") as wordlist:
		wordlist=wordlist.read().split("\n")
	#iterate over files in data_set
	for w in os.walk(input_dir):
		folder=w[0]
		files=w[2]
 		for fili in [i for i in files if i.endswith(".txt")]:
			#catch encoding errors
			try:
				with codecs.open(os.path.join(folder, fili), "r", "utf-8") as text:
					text=re.split("\W", text.read().lower())
					text=[i for i in text if i]
				for w in wordlist: 
					variants= spellfinder(w, text, distance)
					worddict[w]=worddict[w]+list(set(variants))
					for v in variants:
						countdict[v]=countdict[v]+1
			except UnicodeError, e:
				print "WARNING: RETURNED ERROR:\n", e
	for w in wordlist:
		print "{}{} Variants for '{}':".format(header,len(set(worddict[w])), w)
		print ", ".join(sorted(list(set(worddict[w]))))
	print "{}Token counts for variants:".format(header)
	for v in sorted(countdict, key=countdict.get, reverse =True):
		print v, countdict[v]
	
	#ATTN this will fail when two items share variants. fix later
	
			
			
#main('/Users/ps22344/Downloads/chapter2/current/wordlist.txt', "/Users/ps22344/Desktop/Lampeter_txt", 2)
if __name__ == '__main__':
	main(sys.argv[1], sys.argv[2], int(sys.argv[3]))
	
