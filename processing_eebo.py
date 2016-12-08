import re
import shutil
import os
import codecs






def killer(input_dir, pattern):
	filecount=1
	pattern=re.compile(pattern)
	for folder in [i for i in os.listdir(input_dir) if not i.startswith(".")]:	
		for fili in [i for i in os.listdir(os.path.join(input_dir, folder)) if not i.startswith(".")]:
			#print '\n\n***', os.path.join(input_dir, folder, fili), "\n"
			with codecs.open(os.path.join(input_dir, folder, fili), "r", "utf-8") as inputfili:
				rawtext=inputfili.read()
			#print rawtext[200:400]
			result=pattern.findall(rawtext)
			if len(result) > 0:
				print '\n\n***', os.path.join(input_dir, folder, fili), result, "\n"
				print "all", re.findall("<TEXT(?: LANG=\".*\")", rawtext)
	 			filecount = filecount + 1
	 			#os.remove(os.path.join(input_dir, folder, fili))
	 			print "is gone"
	print "so many files", filecount		

killer("/Users/ps22344/Desktop/marcos_corpora/eebo", "<TEXT(?: LANG=\"lat\")")