import argparse



def main():
	parser = argparse.ArgumentParser()
	#add args
	parser.add_argument("variant_one", type=str, help="Enter character(s) representing the first variant")
	parser.add_argument("variant_two", type=str, help="Enter character(s) representing the second variant")
	
	
	parser.add_argument("--read_corpusfile", type=str, 
		help="Enter name of json file containing a file with wordcounts created previously")
	parser.add_argument("--input_dir", type=str, help="Enter the directory containing corpus files")
	parser.add_argument("--threshold", type=int, 
		help="OPTIONAL: Enter the minimum number of tokens varying between variant_one and variant_two that need to be present to be included in the output. Defaults to '0'")
	parser.add_argument("--timespan", type=str, help="Enter a start and end year for the output, seperated by a comma. Format: 'beginning,end'")
	#output options
	parser.add_argument("--output_words", type=str, help="Enter file name to write csv of token counts per word and position")
	parser.add_argument("--output_aggregate_position", type=str, help="Enter file name to write csv of token counts per position")
	parser.add_argument("--output_aggregate_total", type=str, help="Enter file name to write csv of token counts per variant and year")
	parser.add_argument("--write_wordcount_to_file", type=str, help="Enter name of file to write a file with word counts per year, create from input_directory")
	#read input
	args = parser.parse_args()
	#checking input
	if all([not args.read_corpusfile, not args.input_dir]):
		raise IOError("No input data. You need to either specify a corpus directory as '--input_dir' or a file with word counts as '--read_file'")
	if args.timespan:
		# turns input into [str, str] list
		timespan = args.timespan.split(",")
	
	
    
