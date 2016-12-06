import sys
import shutil
import re
import os
from collections import defaultdict

def cleaner (input_dir, search_term):
	for folder in [i for i in os.listdir(input_dir) if not i.startswith(".")]:
		for fili in [i for i in os.listdir(os.path.join(input_dir, folder)) if not i.startswith(".")]:
			if search_term in fili:
				os.remove(os.path.join(input_dir, folder, fili))
				print "die", os.path.join(input_dir, folder, fili)
	

#cleaner("/Users/ps22344/Desktop/marcos_corpora/EMEMTFullCorpus/EMEMT_Corpus", "_comments.txt")


def mixer(input_dir, list_of_endings):
	filidict=defaultdict(list)
	for folder in [i for i in os.listdir(input_dir) if not i.startswith(".")]:
		for fili in [i for i in os.listdir(os.path.join(input_dir, folder)) if not i.startswith(".") and not i.endswith(".gif")]:
			if len([t for t in list_of_endings if fili.endswith(t)]) != 1:
				print [t for t in list_of_endings if fili.endswith(t)], fili
			else:
				filidict[fili].append(os.path.join(input_dir, folder, fili)))
	print filidict
			

mixer("/Users/ps22344/Desktop/marcos_corpora/EMEMTFullCorpus/EMEMT_Corpus", [".txt","_info.html"])