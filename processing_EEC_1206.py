import sys
import shutil
import re
import os
from collections import defaultdict
import codecs


def cleaner (input_dir, search_term):
	for folder in [i for i in os.listdir(input_dir) if not i.startswith(".")]:
		for fili in [i for i in os.listdir(os.path.join(input_dir, folder)) if not i.startswith(".")]:
			if search_term in fili:
				os.remove(os.path.join(input_dir, folder, fili))
				print "die", os.path.join(input_dir, folder, fili)
	
	
def mixer(input_dir, list_of_endings):
	filidict=defaultdict(list)
	for folder in [i for i in os.listdir(input_dir) if not i.startswith(".")]:
		for fili in [i for i in os.listdir(os.path.join(input_dir, folder)) if not i.startswith(".") and not i.endswith(".gif")]:
			if len([t for t in list_of_endings if fili.endswith(t)]) != 1:
				print [t for t in list_of_endings if fili.endswith(t)], fili
			else:
				#print re.sub("txt|html", "XXX", "fili.html")
				filidict[re.sub("("+"|".join(list_of_endings)+")", "", fili)].append(os.path.join(input_dir, folder, fili))
	for k in [i for i in filidict.keys() if i not in ["1687_Barbette_ThesaurusChirurgiae", "1655_Hartlib_ChymicalAddresses", "1640_Bartlet_WarmingStone"]]:
		print k
				
		print "workin on", filidict[k][0][-4:]
		with codecs.open(filidict[k][0], "r", "latin-1") as input_1:
			input_1=input_1.read()
		print "workin on", filidict[k][1][-4:]
 		with codecs.open(filidict[k][1], "r", "utf-8") as input_2:
 			input_2=input_2.read()
 		with codecs.open(os.path.join("outputfiles", k+"_consolidated.txt"), "w", "utf-8") as output:
 			output.write("<text>"+input_1+"</text>--------------<html>"+input_2+"</html>")
 		print "written to:", os.path.join("outputfiles", k+"_consolidated.txt")
		
#is there metadata for 1687_Barbette_ThesaurusChirurgiae.txt. no, that is not a thing
# not text on the other hand for 1655_Hartlib_ChymicalAddresses_info.html
#see the rest above in the list

#mixer("/Users/ps22344/Desktop/marcos_corpora/EMEMTFullCorpus/EMEMT_Corpus", [".txt","_info.html"])	
	
	
	
	

#plan: extract each <L_ > section to its own file


def splitter(input_dir, pattern):
	pattern=re.compile(pattern, re.DOTALL)
	for fili in [i for i in os.listdir(input_dir) if not i.startswith(".")]:
		print "\n\n", fili
		with codecs.open(os.path.join(input_dir, fili), "r", "utf-8") as inputfili:
			inputtext=inputfili.read()
			#print "raw text", inputtext[-100:]
			print len(inputtext)
			result=pattern.findall(inputtext)
			print "resi in", fili, "is", len(result)
			for res in result:
				if not len(res) == 2:
					print  "Alarm, res in ", fili, "is ", len(result), "not two"
				with codecs.open(os.path.join("outputfiles", res[0].strip("<>")+"_processed.txt"), "w", "utf-8") as outi:
					outi.write(res[0]+res[1])
				print "file written to" , os.path.join("outputfiles", res[0].strip("<>")+"_processed.txt"), "thank you very much"
			#use res[0] for file name, dump the rest into file

splitter("/Users/ps22344/Desktop/marcos_corpora/EarlyEnglishCorrespondence/2510/PCEEC/corpus/txt", "(<L_.*?_\d{3}>)(.*?)(?:<Q_\w{3}_.*?>|$)")

r="<Q_\w+_.*?>(.*?)<Q_\w+_.*?>"

