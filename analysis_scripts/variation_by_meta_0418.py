#uv by category
#
from collections import defaultdict
import codecs
import json
import os
import emodcorpustools as emod
import re
import time





	
	
	


t=emod.dictbuilder_2('/Users/ps22344/Downloads/extracted_corpora_0224', 'pubdate')
u, totaldict=emod.variantfinder_2(t, 'meta_data placeholder', 'u','v')
print u.values()

#reduce to 4 numbers
#deal with missing
#put into 20 year boxes
#output csv
#year:{word1:{u:x,v:x}, word2:{}}

u={k[:4]:v for k,v in u.items()}
print u.keys()


yeardict={}
for year in u:
# 	print u[year].keys()
# 	print [{k:v for k,v in h.items() if k == 'u'} for h in u[year].values()]
	#print [[v for k,v in h.items() if k == 'u'] for h in u[year].values()]
	us= [[v for k,v in h.items() if k == 'u'] for h in u[year].values()]
	usum= sum([image for menuitem in us for image in menuitem])
	vs= [[v for k,v in h.items() if k == 'v'] for h in u[year].values()]
	yeardict[year]= {'u':usum, 'v':vsum, 'types':len(u[year].keys())}

print yeardict
