import codecs
import re
import os

##TEMPLATE
"""
We construct a specific meta_dict with corpus-specific search algos for metadata and text.
Then run thru the finder.
"""

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
# done and in /Users/ps22344/Downloads/editdistance/lampeter_extracted
# meta=[
# ("no",'X'), 
# ("corpusnumber",'<title>(.*?)</TITLE>') , 
# ("corpus", "lampeter_corpus"), 
# ("title",   '<(?:TITLEPART|titlePart)>(.*?)(?:TITLEPART|titlePart)>'), 
# ("author", '<PERSNAME>(.*?)</PERSNAME>'),
# ("dialect", "bre"),
# ("authorage", '<BIOGNOTE>(.*?)</BIOGNOTE>'),
# ("pubdate", '<DATE>(.*?)</DATE>'),
# ("genre1", '<KEYWORDS SCHEME="lamTop"><TERM>(.*?)</TERM></KEYWORDS>'), 
# ("genre2", 'X'),
# ("notes", '<DOCIMPRINT>(.*?)</DOCIMPRINT>'),
# ("extraction_notes", """Lots of tags in <> still in there, weird formatting e.g. &rehy;"""),
# ("encoding", 'utf-8'),
# ('text', r"</HEAD>(.*?)</TEXT>")
# ]
# 
# 
# for m in meta:
# 	if m[1] in ['X', 'bre'] or m[0] in ['corpus', "extraction_notes", 'encoding']:
# 		metadict[m[0]]=m[1]
# 	else:
# 		metadict[m[0]]=re.compile(m[1], re.DOTALL)


#STEP 3
# Lancaster Newsbooks
# /Users/ps22344/Desktop/marcos_corpora/The\ LancasterNewsbooksCorpus
#/Users/ps22344/Desktop/marcos_corpora/The\ LancasterNewsbooksCorpus/2531/1654_newsbooks
#and
#/Users/ps22344/Desktop/marcos_corpora/The\ LancasterNewsbooksCorpus/2531/mercurius_fumigosus
#these are normalized for spelling. pretty cool. like so: <reg orig="Merchants">
#note that the very last match on text is sometimes missed. but this seems to be "Finis" exclusively. 


# meta=[
# ("no",'X'), 
# ("corpusnumber",'<title>(.*?)</title>') , 
# ("corpus", "lancaster_newsbook_corpus"), 
# ("title",   '<title>(.*?)</title>'), 
# ("author", '<PERSNAME>(.*?)</PERSNAME>'),
# ("dialect", "bre"),
# ("authorage", '<BIOGNOTE>(.*?)</BIOGNOTE>'),
# ("pubdate", '<head level="2">.+[Pp]rinted.+ (\d{4}).</head>'),
# ("genre1", 'newsbook'), 
# ("genre2", 'X'),
# ("notes", '<notes>(.*?)</notes>'),
# ("extraction_notes", """All original tags left in; note the comments on normalized spelling"""),
# ("encoding", 'utf-8'),
# ('text', r"</head>(.*?)<head level=")
# ]
# 
# 
# for m in meta:
# 	if m[1] in ['X', 'bre'] or m[0] in ['corpus', "extraction_notes", 'encoding', 'genre1']:
# 		metadict[m[0]]=m[1]
# 	else:
# 		metadict[m[0]]=re.compile(m[1], re.DOTALL)



##STEP 4
# HELSINKI
#avail here /Users/ps22344/Desktop/marcos_corpora/helsinki_corpora
#all items in one file
# this would really be a lot better with xml parsing. 
# we break this up by writing individual texts to single files, here /Users/ps22344/Downloads/editdistance/text_to_files_hel_1123.py
# then appyly finder 

# 
# meta=[
# ("no",'X'), 
# ("corpusnumber",'<TEI n="(.*?)" xml:id="(.*?)">') , 
# ("corpus", "helsinki_corpus_xml_edition"), 
# ("title",   '<title key=(?:.*?) ref=(?:.*?) n="(.*?)">(?:.*?)</title>'), 
# ("author", '<author key="(.*?)" ref='),
# ("dialect", "<language ident=(?:.*?)>(.*?)<"),
# ("authorage", 'scheme="#author_age" target="#age_(.*?)"/>'),
# ("pubdate", '<date type="manuscript" from=".+?" to=".+?">(.*?)</date>'),
# ("genre1", ' scheme="#texttype" target="#(.*?)"/>'), 
# ("genre2", 'X'),
# ("notes", '<sourceDesc>(.*?) </sourceDesc>'),
# ("extraction_notes", """All formatting tags left in; it has these interesting  supplied resp= X  tags"""),
# ("encoding", 'utf-8'),
# ('text', r"<text>(.*?)</text>")
# ]

##STEP5 
#Shakespeare 1st folio
# is here /Users/ps22344/Desktop/marcos_corpora/ShakespeareFirstFolio(MachineReadableTextFormat)/0119 
# First folio of Shakespeare: machine readable text format
#   </editorialDecl>
#       <refsDecl>
#         <p>&lt;A&gt; authorial attribution code</p>
#         <p>&lt;C&gt; compositor attribution</p>
#         <p>&lt;&gt; </p>
#         <p>&lt;P&gt; signature</p>
#         <p>&lt;T&gt; play title</p>
#         <p>&lt;Y&gt; when it appears indicates the probable type of copy: Q = quarto; M = foul papers</p>
#         <p>&lt;S&gt; speaker -- the name of the speaker appears between {}</p>
#         <p>&lt;Z&gt; Act/Scene, dramatis personae, etc.</p>
#         <p>&lt;D&gt; stage direction -- in some texts, stage directions are enclosed in double parentheses ((...)) in preference; this makes the text more easily processed by some software</p>
#  
#<T 2H4> title
# meta=[
# ("no",'X'), 
# ("corpusnumber",'<T (.*?)>') , 
# ("corpus", "first_folio_of_shakespeare_machine_readable_text_format"), 
# ("title",   '<T (.*?)>'), 
# ("author", 'shakespeare, william'),
# ("dialect", "bre"),
# ("authorage", '1564-1616'),
# ("pubdate", '1623'),
# ("genre1", 'play'), 
# ("genre2", 'X'),
# ("notes", 'This file contains embedded markers for use by Oxford Concordance Program, delimited by the usual characaters '),
# ("extraction_notes", """this has markup like so: X/*Y (hitherward/*so far) and so LAT_X (LAT_Item)"""),
# ("encoding", 'utf-8'),
# ('text', r">\n+(.*)<[A-Z] ")
# ]




##STEP 6
##INSBRUCK LETTERS
# is here
# /Users/ps22344/Desktop/marcos_corpora/InnsbruckLetterCorpus
# it is in RTF....
#




meta=[
("no",'X'), 
("corpusnumber",'<Quid: numerus currens: (\d*)') , #<Quid: numerus currens: 7
("corpus", "innsbruck_letter_corpus"), 
("title",   '<Quid: numerus currens: (\d*)'), 
("author", r"<Author\(s\)\/writer\(s\): (\D+?)(?:\r\n|,.*?|\(.*)"), #<Author(s)/writer(s)
("dialect", "bre"),
("authorage", '<Age of author: (.*?)\r\n'), #<Age of author: 30
("pubdate", '<Exact date: (.*?)\r\n'), #<Exact date:
("genre1", 'letter'), 
("genre2", 'X'),
("notes", 'The Innsbruck Corpus of English Letters from 1386 to 1698, (prepared by ICAMET, i.e. THE INNSBRUCK COMPUTER ARCHIVE OF MACHINE-READABLE ENGLISH TEXTS, second edition 2007'),
("extraction_notes", """this has markup like so: X/*Y (hitherward/*so far) and so LAT_X (LAT_Item)"""),
("encoding", 'utf-8'),
('text', r"^\$N(.*?)\r\n")
]


for m in meta:
	if m[1] in ['X', 'bre'] or m[0] in ['notes', 'genre1', 'corpus', "extraction_notes", 'encoding']:
		metadict[m[0]]=m[1]
	else:
		metadict[m[0]]=re.compile(m[1], re.MULTILINE)

def finder(input_dir, meta_dict):
	filecount=1
	for fili in [i for i in os.listdir(input_dir) if not i.startswith(".") and not i.startswith("shakdoc")]:
		print '\n\n***', os.path.join(input_dir, fili), "\n"
		with codecs.open(os.path.join(input_dir, fili), "r", "utf-8") as inputfili:
			rawtext=inputfili.read()
			#print rawtext[:100]
		for entry in metadict:
			if isinstance(metadict[entry], re._pattern_type):
				print entry, metadict[entry].findall(rawtext) ,# metadict[entry].findall(rawtext)

 		corpusstring=(
  		"<file> <no="+str(filecount)+"> "
  		"<corpusnumber="+meta_dict['corpusnumber'].findall(rawtext)[0]+"> "
   		"<corpus="+meta_dict['corpus']+"> " 
   		"<title="+re.sub("<.*?>", "", meta_dict['title'].findall(rawtext)[0])+"> "
   		"<author="+meta_dict['author'].findall(rawtext)[0]+"> "   #+" ".join([i for i in meta_dict['author'].findall(rawtext) if i])+"> "
   		"<dialect="+meta_dict['dialect']+"> "#+meta_dict['dialect'].findall(rawtext)[0]+"> "
   		"<authorage="+meta_dict['authorage'].findall(rawtext)[0]+"> " #" ".join([i for i in meta_dict['authorage'].findall(rawtext)])+"> "
   		"<pubdate="+meta_dict['pubdate'].findall(rawtext)[0]+"> "#" ".join(meta_dict['pubdate'].findall(rawtext))+"> "
   		"<genre1="+meta_dict['genre1']+"> "#.findall(rawtext)[0]+"> "
   		"<genre2="+meta_dict['genre2']+"> "
   		"<extraction_notes="+meta_dict['extraction_notes']+"> "
   		"<notes="+meta_dict['notes']+"> "#re.sub("(\s+|<.*?>)", " "," ".join(meta_dict['notes'].findall(rawtext)))+"> "
   		"<encoding="+meta_dict['encoding']+"> "
   		"<text>"+"\n".join(meta_dict['text'].findall(rawtext))+" </text> </file>"
  		)
		with codecs.open(os.path.join("outputfiles", str(fili.rstrip(".txt"))+"_extracted.txt"), "w", "utf-8") as outputfili:
			outputfili.write(corpusstring)
		filecount = filecount + 1
		print "file {} processed succesfully, written to {}.\n".format(os.path.join(input_dir, fili), outputfili)
			

finder("/Users/ps22344/Downloads/editdistance/innsbruck_formatting_fixed_1205", metadict)	
