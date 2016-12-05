

import re
import codecs
import os
#rtf file was converted to utf 8 text in word. header manually deleted. 



textregex=re.compile("<TEI n=.*?</TEI>", re.DOTALL)


with codecs.open("/Users/ps22344/Desktop/marcos_corpora/InnsbruckLetterCorpus/$N Letter Corpus Feb 08.txt", "r", "utf-8") as inputi:
	rawtext=inputi.read()

for line in rawtext.split("\r--------------------------------------------------\r"):
	print line

# with codecs.open("testi.txt", "w", "utf-8") as outputi:
# 	outputi.write(rawtext)

#print rawtext

result=rawtext.split("\n--------------------------------------------------\n")

# print len(result)
# for r in result:
# 	print "\n\n", len(r), r
	


# for no, text in enumerate(result):
# 	with codecs.open(os.path.join("outputfiles/helsinki", str(no))+".txt", "w", "utf-8") as outputi:
# 		outputi.write(text)
# 	print "written", outputi



