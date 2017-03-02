import emodcorpustools as emo
import os

# for spread in os.listdir("spread"):
# 	t= emo.Corpus(os.path.join("spread", spread))
# 	wordcount, worddict = t.wordcount('wordcount')
# 	print "\n***\nThe corpus named '{}' contains {} files for a total of {} words.".format(t.corpusname, t.filecount(), wordcount)
# 	print "{} different authors".format(len(t.categoryfeatures('author')['levels']))



texti="meine"
length=2

#extract context for "i"
#[(0, 'm'), (1, 'e'), (2, 'i'), (3, 'n'), (4, 'e')]
letter="i"

indices= [no for no,item in enumerate(list(texti)) if item==letter]

print indices

ranges= [range(i+1, i+1+length) + range(i-length, i)  for i in indices]

print ranges

#ranges= [item for sublist in ranges for item in sublist if item > 0]


for r in ranges:
	print r
	print [texti[i] for i in r if i > 0]
