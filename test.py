import emodcorpustools as emo
import os

for spread in os.listdir("spread"):
	t= emo.Corpus(os.path.join("spread", spread))
	wordcount, worddict = t.wordcount('wordcount')
	print "\n***\nThe corpus named '{}' contains {} files for a total of {} words.".format(t.corpusname, t.filecount(), wordcount)
	print "{} different authors".format(len(t.categoryfeatures('author')['levels']))