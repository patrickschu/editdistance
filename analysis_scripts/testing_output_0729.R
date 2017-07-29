

spread = read.csv(
  '/home/patrick/Downloads/editdistance/analysis_scripts/input_words.csv', 
  header = TRUE,
  encoding = "UTF-8")

# Lampeter Numbers
# Types in Vocab  43067
# Tokens in Vocab 1057348

#get the format right, with index etc
rownames(spread) = spread[['X']]
spread[['X']] = NULL
print(rownames(spread))
cat ("Rows in here:", nrow(spread), "; Columns in here:", ncol(spread))
cat("Total sum of counts is :", sum(colSums(spread, na.rm = TRUE)), "; mean is:", mean(colSums(spread, na.rm = TRUE)))

# Check top performers; note that "X" is the years
ordered = order(colSums(spread), decreasing = TRUE)
cat(names(spread[ordered][1:5]))
cat(colSums(spread[ordered][1:5], na.rm = TRUE))
#print (colnames(spread))