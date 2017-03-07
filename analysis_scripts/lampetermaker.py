import os
import codecs
import re

dir='/Users/ps22344/Desktop/Lampeter_txt'

for item in os.listdir(dir):
	outputfile= codecs.open("lampeter_txt_only.txt", "a", "utf-8")
	print item
	textregex= re.compile(r"<TEXT(.*?)</TEXT>", re.DOTALL)
	with codecs.open(os.path.join(dir, item) , "r", "utf-8") as inputtext:
		try:
			inputtext= inputtext.read()
			text= textregex.findall(inputtext)
			print len(text)
			for t in text:
				outputfile.write(t+"\n")
		except UnicodeDecodeError, err:
			print item, "would not decode: ", err
	
