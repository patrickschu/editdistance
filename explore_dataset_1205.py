##INSPECTING

def tagextractor(text, tag, fili):
    regexstring="<"+tag+"=(.*?)>"
    result=re.findall(regexstring, text, re.DOTALL)
    if len(result) != 1:
        print "alarm in tagextractor", fili, result
    return result[0]
    







taggetter(input_dir, tag):
	for fili in [i for i in os.listdir(input_dir) if not i.startswith(".")]:
		print "\n\n", fili
		with codecs.open(os.path.join(input_dir, fili), "r", "utf-8") as inputfili:
			inputtext=inputfili.read()
			#print "raw text", inputtext[-100:]
			print len(inputtext)
			result=pattern.findall(inputtext)
			print "resi in", fili, "is", len(result)
			
taggetter("Users/ps22344/Downloads/editdistance/outputfiles/eec_extracted/", "title")