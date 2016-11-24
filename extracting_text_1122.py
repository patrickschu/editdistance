import codecs
import re
import os

##TEMPLATE


# <file> <no=> <corpusnumber=> <corpus=> <title=> <author=Unknown> <otaauthor=Unknown> <dialect=B> <authorage=> <pubdate=> <genre1=> <genre2=> <notes=> <text>  </text> </file>
metadict={}


meta=["no", "corpusnumber", "corpus", "title", "author", "dialect", "authorage", "pubdate", "genre1", "genre2", "notes", "encoding"]



print metadict


 
# STEP 1
# /Users/ps22344/Desktop/marcos_corpora/1_A\ Corpus\ of\ EDD_Full\ corpus
#done and saved to /Users/ps22344/Downloads/editdistance/corpus_of_early_english_dialogs_extracted 
#we need to add the encoding "utf-8" later
# meta=[
# ("no",'X'), 
# ("corpusnumber",'<filename>(.*?)</filename>') , 
# ("corpus", "corpus_of_early_english_dialogs"), 
# ("title",   '<title>(.*?)</title>'), 
# ("author", '<author>(.*?)</author>'),
# ("dialect", "bre"),
# ("authorage", 'X'),
# ("pubdate", '<speechPubDate>\d?: (.*?)</speechPubDate>'),
# ("genre1", '<textType \w+=".*?">(.*?)</textType>'), #<textType typeCode="COMEDY">Drama Comedy</textType>
# ("genre2", 'X'),
# ("notes", '<comment type=".*?">(.*?)</comment>'),
# ("extraction_notes", """Items along the lines of <font>Blanuel</font> or <pagebreak id="E2R" /> or <comment type="compiler">TWO COMMAS IN SOURCE      
# TEXT</comment> are left in"""),
# ("encoding", 'utf-8'),
# ('text', r"<dialogue>(.*?)</dialogue>")
# ]
# 
# 
# for m in meta:
# 	if m[1] in ['X', 'bre'] or m[0] in ['corpus', "extraction_notes"]:
# 		metadict[m[0]]=m[1]
# 	else:
# 		metadict[m[0]]=re.compile(m[1], re.DOTALL)




#STEP 2
# LAMPETER
# /Users/ps22344/Desktop/marcos_corpora/Lampeter 
#what about gender
meta=[
("no",'X'), 
("corpusnumber",'<title>(.*?)</TITLE>') , 
("corpus", "lampeter_corpus"), 
("title",   '<(?:TITLEPART|titlePart)>(.*?)(?:TITLEPART|titlePart)>'), 
("author", '<PERSNAME>(.*?)</PERSNAME>'),
("dialect", "bre"),
("authorage", '<BIOGNOTE>(.*?)</BIOGNOTE>'),
("pubdate", '<DATE>(.*?)</DATE>'),
("genre1", '<KEYWORDS SCHEME="lamTop"><TERM>(.*?)</TERM></KEYWORDS>'), 
("genre2", 'X'),
("notes", '<DOCIMPRINT>(.*?)</DOCIMPRINT>'),
("extraction_notes", """Lots of tags in <> still in there, weird formatting e.g. &rehy;"""),
("encoding", 'utf-8'),
('text', r"</HEAD>(.*?)</TEXT>")
]


for m in meta:
	if m[1] in ['X', 'bre'] or m[0] in ['corpus', "extraction_notes", 'encoding']:
		metadict[m[0]]=m[1]
	else:
		metadict[m[0]]=re.compile(m[1], re.DOTALL)


def finder(input_dir, meta_dict):
	filecount=1
	for fili in [i for i in os.listdir(input_dir) if not i.startswith(".")]:
		print '***', os.path.join(input_dir, fili), "\n"
		with codecs.open(os.path.join(input_dir, fili), "r", "latin") as inputfili:
			rawtext=inputfili.read()
		for entry in metadict:
			if isinstance(metadict[entry], re._pattern_type):
				print entry, len(metadict[entry].findall(rawtext)) , metadict[entry].findall(rawtext)

		corpusstring=(
		"<file> <no="+str(filecount)+"> "
		"<corpusnumber="+fili.rstrip(".tei")+"> "
		"<corpus="+meta_dict['corpus']+"> " 
		"<title="+re.sub("<.*?>", "", meta_dict['title'].findall(rawtext)[0])+"> "
		"<author="+" ".join([i for i in meta_dict['author'].findall(rawtext) if i])+"> "
		"<dialect="+meta_dict['dialect']+"> "
		"<authorage="+" ".join([i for i in meta_dict['authorage'].findall(rawtext)])+"> "
		"<pubdate="+meta_dict['pubdate'].findall(rawtext)[0]+"> "
		"<genre1="+meta_dict['genre1'].findall(rawtext)[0]+"> "
		"<genre2="+meta_dict['genre2']+"> "
		"<extraction_notes="+meta_dict['extraction_notes']+"> "
		"<notes="+re.sub("<.*?>", ""," ".join(meta_dict['notes'].findall(rawtext)))+"> "
		"<encoding="+meta_dict['encoding']+"> "
		"<text>"+"\n".join(meta_dict['text'].findall(rawtext))+" </text> </file>"

		)
		with codecs.open(os.path.join("outputfiles", fili+"_extracted.txt"), "w", "utf-8") as outputfili:
			outputfili.write(corpusstring)
		filecount = filecount + 1
		print "file {} processed succesfully, written to {}.\n".format(os.path.join(input_dir, fili), outputfili)
			
finder("/Users/ps22344/Desktop/marcos_corpora/Lampeter/2400/Texts/", metadict)	
#> <corpusnumber=> <corpus=> <title=> <author=Unknown> <otaauthor=Unknown> <dialect=B> <authorage=> <pubdate=> <genre1=> <genre2=> <notes=> <text>  </text> </file>
				

 