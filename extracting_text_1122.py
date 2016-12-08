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
# omg that was terrible. but now done 

# 
# meta=[
# ("no",'X'), 
# ("corpusnumber",'<Quid: numerus currens: (\d*)') , #<Quid: numerus currens: 7
# ("corpus", "innsbruck_letter_corpus"), 
# ("title",   '<Quid: numerus currens: (\d*)'), 
# ("author", r"<Author\(s\)\/writer\(s\): (\D+?)(?:\r\n|,.*?|\(.*)"), #<Author(s)/writer(s)
# ("dialect", "bre"),
# ("authorage", '<Age of author: (.*?)\r\n'), #<Age of author: 30
# ("pubdate", '<Exact date: (.*?)\r\n'), #<Exact date:
# ("genre1", 'letter'), 
# ("genre2", 'X'),
# ("notes", 'The Innsbruck Corpus of English Letters from 1386 to 1698, (prepared by ICAMET, i.e. THE INNSBRUCK COMPUTER ARCHIVE OF MACHINE-READABLE ENGLISH TEXTS, second edition 2007'),
# ("extraction_notes", """this has markup like so: X/*Y (hitherward/*so far) and so LAT_X (LAT_Item)"""),
# ("encoding", 'utf-8'),
# ('text', r"^\$N(.*?)\r\n")
# ]

# 
# for m in meta:
# 	if m[1] in ['X', 'bre'] or m[0] in ['notes', 'genre1', 'corpus', "extraction_notes", 'encoding']:
# 		metadict[m[0]]=m[1]
# 	else:
# 		metadict[m[0]]=re.compile(m[1], re.MULTILINE)


##STEP 7
#EMEMT second to last
##/Users/ps22344/Desktop/marcos_corpora/EMEMTFullCorpus/
##in EMEMT _CORPUS, we have several categories. 
## wihtin, its NUMBER_NAME _TITLE
#_info.html for metadata
#.txt for text
# we need to combine those
#disregard all NORM files
#we delete a lot of stuff
#we compile html and text into one file, then combine metadata. 
#this is done. 
#note the wacky encoding on this one. 

# meta=[
# ("no",'X'), 
# ("corpusnumber",'X') , #Filename
# ("corpus", "early_modern_english_medical_texts"), 
# ("title",   '<title>\d{4} .+: (.*?)</title>'), #<title>1525 Braunschweig: Handy warke of surgeri</title>
# ("author", r"<p><strong>Author:(.*?)</p>"), #<p><strong>Author:</strong> Hieronymus Braunschweig [Brunschwig; Jerome of Brunswick] </p>
# ("dialect", "X"),
# ("authorage", '<p><strong>Dates of birth and death:(.*?) </p>'), # <p><strong>Dates of birth and death:</strong> 1450&ndash;c. 1512 </p>
# ("pubdate", '<p><strong>Year of publication:(.*?) </p>'), #<p><strong>Year of publication:</strong> 1525 </p>
# ("genre1", 'medical'), 
# ("genre2", 'X'),
# ("notes", 'The corpus of Early Modern English Medical Texts (EMEMT, 1500-1700) is a register-specific corpus containing a representative  selection of texts across the entire field of English medical writing of the  period, ranging from theoretically-oriented texts rooted in academic traditions  of medicine to popularized and utilitarian texts verging on household  literature'),
# ("extraction_notes", """comments in square brackets removed bec there was so much of it; original text in ascii"""),
# ("encoding", 'utf-8'),
# ('text', r"<text>(.*?)</text>")#replace everything in "["
# ]

##STEP 8
##Eraly English Correspondence, parsed
#this is the last one. not counting EEBO, that is..
#/Users/ps22344/Desktop/marcos_corpora/EarlyEnglishCorrespondence
# we go in and change more letter "03" to "033"
# we keep all the weird capital letters markup. who knows when we might need it. 
# 
# meta=[
# ("no",'X'), 
# ("corpusnumber",'<L_(.*?_\d{3})>') , #<L_CONWAY_055>
# ("corpus", "parsed_corpus_of_early_english_correspondence"), 
# ("title",   '\{(?:ED|COM):(.*?)\}'), #<Q_\w{3}_.*?>
# ("author", r"<A_(.*?)>"), #<p><strong>Author:</strong> Hieronymus Braunschweig [Brunschwig; Jerome of Brunswick] </p>
# ("dialect", "bre"),
# ("authorage", '<A-DOB_(\d{4})>'), # <A-DOB_1602>, '<A-DOB_(\d{4})>
# ("pubdate", ':(?:E|M)\d:(\d{4})'), #E2:1593:
# ("genre1", 'letter'), 
# ("genre2", 'X'),
# ("notes", 'The conventions used to indicate editorial comments and other types of text markup are the same as used in the ../annotation/intro.htm#text_markup" PPCME2/PPCEME'),
# ("extraction_notes", """removed lines beginning with { or <; left all the capitalized comments in"""),
# ("encoding", 'utf-8'),
# ('text', "X")
# ]
# 
# 
# 
# 
# for m in meta:
# 	if m[1] in ['X', 'bre'] or m[0] in [ 'notes', 'genre1', 'corpus', "extraction_notes", 'encoding']:
# 		metadict[m[0]]=m[1]
# 	else:
# 		metadict[m[0]]=re.compile(m[1], re.DOTALL)



##STEP 9
##EEBO
# we learn this from SO: for file in *.tar.gz; do tar -zxf $file; done
# we learn this from SO: if 1 in {x, y, z}:
# its here, 5gb of it
# /Users/ps22344/Desktop/marcos_corpora/eebo
# lots of markup in here; lets delete anythin



meta=[
("no",'X'), 
("corpusnumber",'X') , #file name
("corpus", "early_english_books_online"), 
("title",   '<TITLE TYPE=.*?>(.*?)</TITLE>'), #<TITLE TYPE="245" I2="0">Fennors defence: or, I am your first man VVherein the VVater-man, Iohn Taylor, is dasht, sowst, and finally fallen into the Thames: With his slanderous taxations, base imputations, scandalous accusations and foule abhominations, against his maiesties ryming poet: who hath answered him without vexatione, or [...] bling recantations. The reason of my not meeting at the Hope with Taylor, is truly demonstrated in the induction to the [...] udger. Thy hastie gallop my milde muse shall checke, that if thou sit not sure, will breake thy necke.</TITLE>
("author", r"<AUTHOR>(.*?)</AUTHOR>"), #<AUTHOR>Fennor, William.</AUTHOR></p> #limit to name only, ignore dates
("dialect", "bre"),
("authorage", "<AUTHOR>.*?((?:d\. |b\. )?\d{4}(?:-\d{2,4})?)\.?</AUTHOR>"), # we can get this from after author names  [i.e. 1645]
("pubdate", '<DATE>.*?(?:ca. |the yeare?\.? |between |\D \. |Anno Dom. |.*? anno |.*?, |\[|\[i.e. |\[.*?|\D+ \[)?(1[2-8][0-9][0-9]).*?</DATE>'), #"#<DATE>1615.</DATE> #[between 1695 and 1700] #<DATE>(?:between |\D \. |Anno Dom. |.*? anno |.*?, |\[|\[i.e. |\[.*?|\D+ \[)?([0-1][0-9][0-9][0-9]).+</DATE>'
("genre1", '<TERM TYPE=.*>(.*?)\.?</TERM>'), #<TERM TYPE="geographic name">Gambia River --  Description and travel --  Early works to 1800.</TERM><TERM TYPE="geographic name">Africa, West --  Description and travel --  To 1850.</TERM>
("genre2", 'X'),
("notes", '<NOTE>(.*?)</NOTE>'),
("extraction_notes", """removed all markup in triangle brackets. 286 files with TEXT tag lat deleted"""),
("encoding", 'utf-8'),
('text', "<TEXT(?: LANG=\"(?:eng|eng lat|lat eng)\")?>.*?</TEXT>")#, <TEXT LANG="eng"> <TEXT LANG="lat eng">
]

 


for m in meta:
	if m[1] in ['X', 'bre'] or m[0] in ['corpus', "extraction_notes", 'encoding']:
		metadict[m[0]]=m[1]
	else:
		metadict[m[0]]=re.compile(m[1], re.DOTALL)



def finder(input_dir, meta_dict):
	filecount=1
	for folder in [i for i in os.listdir(input_dir) if not i.startswith(".")]:	
		for fili in [i for i in os.listdir(os.path.join(input_dir, folder)) if not i.startswith(".")]:
			print '\n\n***', os.path.join(input_dir, folder, fili), "\n"
			with codecs.open(os.path.join(input_dir, folder, fili), "r", "utf-8") as inputfili:
				rawtext=inputfili.read()
			#print rawtext[200:400]
			for entry in [i for i in metadict.keys() if i not in {'text'}]:
				if isinstance(metadict[entry], re._pattern_type) and len(metadict[entry].findall(rawtext)) == 0:
					print '\n\n***ALARM', os.path.join(input_dir, folder, fili), "\n"
					print entry, len(metadict[entry].findall(rawtext)),metadict[entry].findall(rawtext)
			if len(metadict['author'].findall(rawtext)) == 0:
				author="unknown"
			else:
				author=re.sub("(\d+(st|th|rd)(/\d+(st|th|rd))?( Ccent)?|\d+,?| b\. | d\. |-|\?|,? fl\.? |,?\Wca\.?|\.| or )", "", metadict['author'].findall(rawtext)[0])
				print "ottiotti", author.rstrip(", ")
			if len(meta_dict['authorage'].findall(rawtext)) > 0:
				authorage=meta_dict['authorage'].findall(rawtext)[0]
				print authorage
			else:
				authorage="unknown"
			if len(meta_dict['genre1'].findall(rawtext)) > 0:
				genre=meta_dict['genre1'].findall(rawtext)[0]
				print genre
			else:
				genre="unknown"
				
			corpusstring=(
				"<file> <no="+str(filecount)+"> "
	 			"<corpusnumber="+fili.rstrip(".headed.xml")+"> "
	 			"<corpus="+meta_dict['corpus']+"> " 
	 			"<title="+meta_dict['title'].findall(rawtext)[0]+"> " # 
	 			"<author="+author.rstrip(", ")+"> "   #<AUTHOR>Fennor, William.</AUTHOR>
	 			"<dialect="+meta_dict['dialect']+"> "#+meta_dict['dialect'].findall(rawtext)[0]+"> "
	 			"<authorage="+authorage+"> " #" ".join([i for i in meta_dict['authorage'].findall(rawtext)])+"> "
	 			"<pubdate="+re.sub("<.*?>", "", meta_dict['pubdate'].findall(rawtext)[0])+"> "
	 			"<genre1="+genre+"> "
	 			"<genre2="+meta_dict['genre2']+"> "
	 			"<extraction_notes="+meta_dict['extraction_notes']+"> "
	 			"<notes="+meta_dict['notes'].findall(rawtext)[0].strip("()")+"> "#re.sub("(\s+|<.*?>)", " "," ".join(meta_dict['notes'].findall(rawtext)))+"> " #<NOTE>Transcribed from: (Early English Books Online ; image set 15207)</NOTE> -- there can be several
	 			"<encoding="+meta_dict['encoding']+"> "
	 			"<text>"+"\n".join([re.sub("<.*?>", "", i) for i in meta_dict['text'].findall(rawtext)])+" </text> </file>"
				)
	 		with codecs.open(os.path.join("outputfiles",  str(fili)+"_extracted.txt"), "w", "utf-8") as outputfili:
	 			outputfili.write(corpusstring)
	 		filecount = filecount + 1
 			print "file {} processed succesfully, written to {}.\n".format(os.path.join(input_dir, folder, fili), outputfili)
			

finder("/Users/ps22344/Desktop/marcos_corpora/eebo", metadict)	






