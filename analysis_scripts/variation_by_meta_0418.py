#uv by category
#
from collections import defaultdict
import codecs
import json
import os
import emodcorpustools as emod
import re
import time
import pandas




	
	#note that helsini is ball parked; os are unknown
	
input_dir= '/Users/ps22344/Downloads/extracted_corpora_0224'
output_file= "firstfolio"

t=emod.dictbuilder_2(input_dir, 'pubdate')
u, totaldict=emod.variantfinder_2(t, 'meta_data placeholder', 'u','v')


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
	vsum= sum([image for menuitem in vs for image in menuitem])
	yeardict[year]= {'u':usum, 'v':vsum, 'types':len(u[year].keys()), 'totalwords': totaldict[year]}

df=pandas.DataFrame.from_dict(yeardict, orient='index')

print df.columns

print list(df.columns)

print len(list(df.columns))
with codecs.open(output_file+".csv", "w") as csvout:
	df.to_csv(csvout, index_label= 'year', encoding="utf-8")

#print yeardict
print "written to", output_file