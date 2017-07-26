import pandas

dd = {1600: 
	{"ut_('base',)": 0, "ut_(1,)": 100, "ut_(0,1)": 100000, "uttt_(1,)": 333, "fu_(1,1)": 2323}, 
	1601: 
	{"ut_('base',)": 1, "ut_(1,)": 200, "ut_(0,1)": 200000, "uttt_(1,)": 333, "fu_(1,1)": 2323},
	1603:
	{"ut_('base',)": 2, "ut_(1,)": 300, "ut_(0,1)": 300000, "uttt_(1,)": 333, "fu_(1,1)": 2323}
	}

dd = {k:v for k,v in dd.viewitems() if not v in ["fu_(1,1)"]} 
print dd.values()
df = pandas.DataFrame(dd).T

#splitcols = [i.split("_") for i in df.columns]	
#print splitcols
splitcols2 = [(w, eval(m)) for w,m in [i.split("_") for i in df.columns]]
print [(type(x), type(z)) for x,z in splitcols2]
print splitcols2
df.columns = splitcols2

print df

column_filter = [(word, attr) for word, attr in df.columns if not attr[0]]
column_filter = [attr for word, attr in df.columns]

word, attr = ('ut', (1,))
print "w", word
print "a", attr

def filti(x):
	print "tt", type(x)
	word, attr = x
	print "w", word
	print "a", attr
	return attr.__hash__(), attr


sel = df.columns.map(lambda x: filti(x))

g= df.groupby(lambda x: filti(x), axis = 1).sum()
g.columns = [i[1] for i in g.columns]

print g

#print g.columns
print [type(i) for i in g.columns]

#print "result", df[df.columns[sel]]



# get by position
# year, by position
# sum all with ID position
# "sum all columns where attr == attr, over rows
result = pandas.DataFrame()




#get per year: base vs all





