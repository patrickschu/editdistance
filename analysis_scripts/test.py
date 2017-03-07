import emodcorpustools as emo
import os
import sys

# for spread in os.listdir("spread"):
# 	t= emo.Corpus(os.path.join("spread", spread))
# 	wordcount, worddict = t.wordcount('wordcount')
# 	print "\n***\nThe corpus named '{}' contains {} files for a total of {} words.".format(t.corpusname, t.filecount(), wordcount)
# 	print "{} different authors".format(len(t.categoryfeatures('author')['levels']))



# texti="meinei"
# length=3
# 
# #extract context for "i"
# #[(0, 'm'), (1, 'e'), (2, 'i'), (3, 'n'), (4, 'e')]
# #we just have to run this over the control letter
# #control and stimulus letter
# 
# letter="i"
# 
# 
# 
# print indices
# 
# ranges= [(range(i-length, i),range(i+1, i+1+length))  for i in indices]
# 
# print ranges



# for r in ranges:
# 	print r
# 	#for each entry in the two tuples in r, match to texti
# 	#r=[[1,2,3],[2,3,4]]
# 	output=[tuple((texti[x] for x in i if -1 < x < len(texti))) for i in r]


# def contextfinder(input_word, variant, context_window=2):
# 	"""
# 	The contextfinder finds all instances of variant in the input_word.
# 	It yields a number of characters preceding and folllowing it as specified in context_window.
# 	"""
# 	#establish position of variants in the word
# 	indices= [no for no,i in enumerate(list(input_word)) if i==variant]
# 	if len(indices) < 1:
# 		print "\nERROR in contextfinder: No instances of '{}' found in '{}'\n".format(variant, input_word)
# 	#establish the indices for context
# 	ranges= [(range(i-context_window, i),range(i+1, i+1+context_window))  for i in indices]
# 	for ran in ranges:
# 		output=[tuple((input_word[x] for x in i if -1 < x < len(input_word))) for i in ran]
# 		print output
# 		yield output
# 	
# 	
# 
# for g in contextfinder("muhu", "v", 3):
# 	print g
# def main(a,b):
# 	print "args are", a,b
# 
# if __name__ == '__main__':
#     # main should return 0 for success, something else (usually 1) for error.
#     print sys.argv[1:]
#     main(*sys.argv[1:])
    
for g in emo.contextfinder("muschibear", "u", 100, 5):
	print g
#input_word, variant, pre_window, post_window)

