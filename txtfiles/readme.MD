#Variantfinder

The variantfinder identifies all words that differ in the use of spelling variants such as _u_ versus _v_ in _but_ and _bvt_. 

It takes set of texts and two characters (or character groups) as input and identifies all words showing this kind of variation. 

For instance, when _u_ and _v_ are entered, it will identify a word such as _turbulent_ as potentially relevant since it contains _u_ s. It will then check the corpus for the presence of variants such as _turbvlent_, _tvrbulent_, and _tvrbvlent_.

For each, a token count over the years is returned, and output according to user criteria. 

##Output aggregate (total or by position) or by word or context window

##Flags

--

###Required arguments, input

> variant_one           
Enter character(s) representing the first variant

>  variant_two           
Enter character(s) representing the second variant

and one of the two below:

> \--read_corpusfile           
Enter name of json file containing wordcounts created
                        previously

>  \--input_dir           
                        Enter the directory containing a corpus of .txt files
                        to read

###Required arguments, output

>  \--output_words            
Enter file name to write csv of **token counts per word
                        and position**

>  \--output_position           
Enter file name to write csv of token counts **per
                        position**

>  \--output_aggregate           
Enter file name to write csv of token counts per
                        **variant and year**

###Optional arguments
                        
>  \--write_corpusfile          
OPTIONAL: Enter name of file to write a json file with word counts
                        per year, created from input_directory

>  \--threshold            
OPTIONAL: Enter the minimum number of tokens varying
                        between variant_one and variant_two that need to be
                        present to be included in the output. Defaults to '0'

>  \--timespan           
OPTIONAL: Enter a start and end year for the output,
                        separated by a comma. Format: 'beginning,end'

>  \--verbose           
OPTIONAL: Set to 'True' for complete printout

>  \-h, \--help            
show help message and exit


