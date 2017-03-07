import re
import codecs
import os




textregex=re.compile("<TEI n=.*?</TEI>", re.DOTALL)


with codecs.open("/Users/ps22344/Desktop/marcos_corpora/helsinki_corpora/HC_XML_Master_v9f.xml", "r", "utf-8") as inputi:
	rawtext=inputi.read()

result=textregex.findall(rawtext)

for no, text in enumerate(result):
	with codecs.open(os.path.join("outputfiles/helsinki", str(no))+".txt", "w", "utf-8") as outputi:
		outputi.write(text)
	print "written", outputi

