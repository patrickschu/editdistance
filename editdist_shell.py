import nltk
from nltk import edit_distance
import codecs
import os
import re
import sys



def spellfinder(word, text, distance):
	"""
	word is a word string. 
	text is a tokenized list of words.
	distance is the longest edit distance to be returned>
	"""
	print "We have {} words in the text, distance is set to {} for '{}'".format(len(text), distance, word)
	#print text
	result=[i for i in text if nltk.edit_distance(word, i) <= distance]
	print result
	print len(result)
	if len(result) > 0:
		result=set(result)
		#print "result: ", result
		print "{} matches".format(len(list(result)))
		
	

def main(wordlist, data_set, distance):
	#reading in the wordlist
	with codecs.open(wordlist, "r", "utf-8") as wordlist:
		wordlist=wordlist.read().split("\n")
	#iterate over files in data_set
	for fili in [i for i in os.listdir(data_set) if not i.startswith(".")]:
		print "\n---\nWorking on ", fili
		#catch encoding errors
		try:
			with codecs.open(os.path.join(data_set, fili), "r", "utf-8") as text:
 				text=re.split("\W", text.read().lower())
 				text=[i for i in text if i]
			for w in wordlist: 
				spellfinder(w, text, distance)
		except UnicodeError, e:
			print "WARNING: RETURNED ERROR:\n", e
			
			
#main('/Users/ps22344/Downloads/chapter2/current/wordlist.txt', "/Users/ps22344/Desktop/Lampeter_txt", 2)
if __name__ == '__main__':
	main(sys.argv[1], sys.argv[2], int(sys.argv[3]))
	
