lampeter_wordlist = '/home/patrick/Downloads/editdistance/analysis_scripts/wordlist_words.csv'
lampeter_inputdir =   '/home/patrick/Downloads/editdistance/analysis_scripts/input_words.csv' 

supercorpus_uv = '/home/patrick/Downloads/editdistance/analysis_scripts/uvwords.csv'
supercorpus_vu = '/home/patrick/Downloads/editdistance/analysis_scripts/vuwords.csv'

step1rs = '/home/patrick/Downloads/editdistance/analysis_scripts/step1rswords.csv'
step1sr = '/home/patrick/Downloads/editdistance/analysis_scripts/step1srwords.csv'

sinki = FALSE
spread = read.csv(
  supercorpus_vu, 
  header = TRUE,
  encoding = "UTF-8")

# Lampeter Numbers
# Types in Vocab  43067
# Tokens in Vocab 1057348
if (sinki == TRUE) {sink(file = 'vu_words.txt'); print ('start the sinking')}
#get the format right, with index etc
rownames(spread) = spread[['X']]
#print (class(spread[['X']]))
#print (class(rownames(spread)))
#spread[['X']] = NULL
print(rownames(spread))
cat ("Rows in here:", nrow(spread), "; Columns in here:", ncol(spread))
cat("Total sum of counts is :", sum(colSums(spread, na.rm = TRUE)), "; mean is:", mean(colSums(spread, na.rm = TRUE)))

# Check top performers; note that "X" is the years
ordered = order(colSums(spread, na.rm = TRUE), decreasing = TRUE)
cat(names(spread[ordered][1:5]))
cat(colSums(spread[ordered][1:5], na.rm = TRUE))
#print (colnames(spread))
cat("Values per year", rowSums(spread[1:10,], na.rm = TRUE))
if (sinki == TRUE) {sink(file = NULL); print("stopped the sinking")}

#THIS IS UV
sink('supercorpus_vu_1759.txt')
spread[, !is.na(spread['1759',])]['1759',]
sink()
