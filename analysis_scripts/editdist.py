import nltk
from nltk import edit_distance
import codecs
from nltk.corpus import shakespeare
from xml.etree import ElementTree
import os
import re

t=nltk.edit_distance("are", "eee")


# variants=["commitmentte", "commitmente", "comitmentt"]
# 
# variants= ["comette", "comitte", "commyte", "comytte", "komytte", "commyt", "commytte", "committe", "commytt", "committ", "commit", "comite", "commete", "commite", "comyte", "conmit", "comit", "comitt", "comyt", "comytt", "comit", "comitt", "commett", "commite", "committe", "commyt", "commytt", "commytte", "conmit", "committ", "commit", "commytt", "commytte", "commite", "committe", "commytt", "commit", "commytte", "comit", "comitt", "committ"]
# variants=["enjoye", "enyoie", "enyoy", "enjoye", "enjoie", "enjoy", "injoy","injoye", "injoie"]
# #variants=["settle"]
# searchterms=["enjoyment"]
# 
# for item in variants:
# 	for ending in [""]:#["mentte", "mente", "mentt", "ment"]:
# 		dist=nltk.edit_distance('enjoy', item+ending)
# 		print item+ending, dist
# 		if dist < 5:
# 			searchterms.append(item+ending)
# 	
# 
# with codecs.open("lampeter.txt", "r", "Utf-8") as corpus:
# 	corpus=corpus.read().lower().split()
# print "we are working with {} words".format(len(corpus))
# 
# 
# 
# for thing in searchterms:
# 	if corpus.count(thing) > 0:
# 		print "\n\n", thing
# 		print corpus.count(thing)
# 		
with codecs.open("lampeter.txt", "r", "utf-8") as corpus:
 	corpus=re.split("\W", corpus.read().lower())
 	corpus=[i for i in corpus if i]

#with codecs.open('/Users/ps22344/Desktop/alllist_0622.txt', "r", "utf-8") as wordlist:
#	wordlist=wordlist.read().split("\n")

#variants=["emprowement","enpproument","enprowment","emproument","emprowment","enprouemente","emprouement","emprovment","emprovement","improwement"," improvment","improwment","improwmente","ymprovement","improouement","improuement","improument","improovement","inprovement","improvement",   "impruivement","impreuvement","impreevement"	]


def spellfinder(word, data_set, distance):
	"""
	word is a word string. 
	data_set is a tokenized list of words.
	distance is the longest edit distance to be returned>
	"""
	print "We have {} words in the corpus, distance is set to {}".format(len(data_set), distance)
	result=[i for i in data_set if nltk.edit_distance(word, i) <= distance]
	print result
	print data_set
	if len(result) > 0:
		result=set(result)
		print word, result
		print "{} matches".format(len(list(result)))
		
	
	
for w in ['improvement']: 
	spellfinder(w, corpus, 3)
	
	
	
