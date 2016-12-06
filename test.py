import re


print re.sub("txt|html", "XXX", "fili.html")

meta=[
("no",'X'), 
("corpusnumber",'<L_(.*?_\d{3})>') , #<L_CONWAY_055>
("corpus", "parsed_corpus_of_early_english_correspondence"), 
("title",   '\{(?:ED|COM):(.*?)\}'), #<Q_\w{3}_.*?>
("author", r"<A_(.*?)>"), #<p><strong>Author:</strong> Hieronymus Braunschweig [Brunschwig; Jerome of Brunswick] </p>
("dialect", "bre"),
("authorage", '<A-DOB_(\d{4})>'), # <A-DOB_1602>, '<A-DOB_(\d{4})>
("pubdate", ':(?:E|M)\d:(\d{4})'), #E2:1593:
("genre1", 'letter'), 
("genre2", 'X'),
("notes", 'The conventions used to indicate editorial comments and other types of text markup are the same as used in the ../annotation/intro.htm#text_markup" PPCME2/PPCEME'),
("extraction_notes", """removed lines beginning with { or <; left all the capitalized comments in"""),
("encoding", 'utf-8'),
('text', "X")
]


m=[i[0] for i in meta]
print m