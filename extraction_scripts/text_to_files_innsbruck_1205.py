

import re
import codecs
import os
#rtf file was converted to utf 8 text in word. header manually deleted. 

#second step: switch out file for unnormalized

textregex=re.compile("-{10,}(.*?)-{10,}", re.DOTALL)


with codecs.open("/Users/ps22344/Desktop/$I Letter Corpus Feb 08 with headers.txt","r", "utf-8") as inputi:
	rawtext=inputi.read()


count=1

for s in rawtext.split("--------------------------------------------------"):
	with codecs.open(os.path.join("innsbruck", str(count)+"_innsbruck.txt"), "w", "utf-8") as outputi:
		outputi.write(s)
	count=count+1

#result=textregex.findall(rawtext)

# for t in result:
# 	print len(t), "\n+++++++++++++++++++++++++++++\n", t
# 
# with codecs.open("testi.txt", "a", "utf-8") as outputi:
# 	outputi.write("+++++++\n".join(result))

#doc = Rtf15Reader.read(open('/Users/ps22344/Desktop/marcos_corpora/InnsbruckLetterCorpus/$N Letter Corpus Feb 08.rtf', "rb"))
#
#print [x.content for x in doc.content]


#print rawtext



# print len(result)
# for r in result:
# 	print "\n\n", len(r), r
	


# for no, text in enumerate(result):
# 	with codecs.open(os.path.join("outputfiles/helsinki", str(no))+".txt", "w", "utf-8") as outputi:
# 		outputi.write(text)
# 	print "written", outputi



