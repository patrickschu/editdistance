## Variantfinder

### Description
The variantfinder identifies and counts words that differ in the use of spelling variants such as _u_ versus _v_ in _but_ and _bvt_. 

It takes set of texts (a _corpus_) and two _characters_ (or character groups) as input and identifies all words showing variation between the specified characters. 

For instance, when _u_ and _v_ are entered, it will identify a word such as _turbulent_ as potentially relevant since it 
contains two _u_ s. It will then check the corpus for the presence of variants such as _turbvlent_, _tvrbulent_, and _tvrbvlent_.

For each of these types, a token count over the years is returned, and output as a csv file according to user criteria. 

Download [here](https://raw.githubusercontent.com/patrickschu/editdistance/master/analysis_scripts/variantfinder.py) for Python 2. You also need to download the [Corpus tools](https://github.com/patrickschu/editdistance/blob/master/analysis_scripts/emodcorpustools.py). See [here](https://github.com/patrickschu/tgdp/blob/master/summer16/shell_basics.MD) for instructions on how to run it in a shell. 

See below for instructions on Parameters and Examples. 


----

### Parameters

### 1. Required arguments, input

> variant_one           
Enter character(s) representing the first variant

>  variant_two           
Enter character(s) representing the second variant

and one of the two below:

> \--read_corpusfile           
Enter name of json file containing wordcounts created
                        previously

>  \--input_dir           
Enter a directory containing a corpus of .txt files
                        to read


> \--read_wordlist
Enter name of a json file containing wordcounts created previously; these will be used to establish varying types. 


### 2. Required arguments, output

>  \--output_words            
Enter file name to write csv of **token counts per word
                        and position**

>  \--output_position           
Enter file name to write csv of token counts **per
                        position**

>  \--output_aggregate           
Enter file name to write csv of token counts per
                        **variant and year**

### 3. Optional arguments

> \--lemmatize
OPTIONAL: Removes word-final 's' to normalize plural forms
                        
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

----

### Examples 

These examples illustrate how the parameters listed above can be combined. 

#### Example 1
The code below will identify variants with _u_ and _v_; 
read word counts from a file called *vocab.json*; 
and output token counts by position (i.e. initial, second character, etc.) to a csv file called *uv_output.csv*. 

    python variantfinder.py u v --read_corpusfile vocab.json --output_position uv_output

The resulting csv will look like this:


| year     |base       |  0        |  1     | etc... |
| --------- | ----------| ----------| ------ | ---- |
| 1600  | 200 | 27 | 432 | 
| 1601  | 435 | 112 | 65 | 
| etc ...|



Where *base* indicates that base form containing *u* and the numbers indicate the position of the word *u* has been replaced by *v*. 

For instance, *v* replacing *u* in initial position is counted under position *0*; 27 instances of this were found for the year 1600. 

#### Example 2
The code below will identify variants with _t_ and _r_; 
compute word counts from the text files contained in *home/corpora*; 
and output token counts by year (i.e. the sum of words with _t_ compared to _r_ per year) to a csv file called *tr_output.csv*. 

    python variantfinder.py r t --input_dir home/corpora --output_aggregate tr_output

The resulting csv will look like this:


| year        | t            | r  |
| ------------- |---------| -----|
| 0     | 112949 | 46119 |
| 850      | 6786      |   4097 |
| 950 | 9658      |    12411 |
| etc ...|

#### Example 3
The code below will identify variants with _u_ and _v_; 
compute word counts from the text files contained in *home/x/corpora*; 
write those word counts to a file called *vocab.json*, so they can be used in the future with --read_corpusfile;
and output token counts by individual words (e.g. _turbulent_ vs . _turbvlent_, _tvrbulent_, and _tvrbvlent_) to a file called *words_spreadsheet.csv*.
The `--threshold` setting limits the analysis to words that occur at least 100 times;
`--timespan` tells the program to output only data between 1600 and 1700. 

    python variantfinder.py u v  --input_dir /home/x/corpora --write_corpusfile vocab --output_words words_spreadsheet --threshold 100 --timespan 1600,1700 

The resulting csv will look like this:



| year | aboue_base | aboue_3 | abound_base | abound_3 |
| --------- | ---------- | --------- | ------- | ---- |
| 1600 | NA | 1 | NA | NA |
| 1601 | 6 | NA | 3 | NA |
| 1602 | 9 | NA | 3 | NA |
| etc...|



That is, for the year 1600, there are no instances of *aboue*, but 1 token of *above*, where *v* replaces *u* in the fourth character slot
(note that an index of *3* refers to the 4th slot -- 0 indicates the first character). 


#### Example 4

The code below will replicate Example 3, except that the setting --lemmatize will remove suffixes such as plural *-s* from the words. The items included as affixes are given in Notes and Conventions below. 

    python variantfinder.py u v  --input_dir /home/x/corpora --lemmatize --write_corpusfile vocab --output_words words_spreadsheet --threshold 100 --timespan 1600,1700 


----
### Notes and Conventions

- the script requires that [pandas](https://pandas.pydata.org/pandas-docs/stable/install.html) and [NLTK](http://www.nltk.org/install.html) are installed. 

- the following notation is used in output csvs: the form containing variant_one is labeled the *base* form; 
all other forms are suffixed by an index indicating the character slot where they vary. E.g. when running it with *u* and *v*, *reputation_base* labels the tokens of *reputation*, 
reputation_3 labels tokens of *repvtation*. 

- *NA* indicates that no tokens of the word were present in that year's data

- documents that do not have a publication date are counted as publication year *0*. 

- the list called on to remove affixes when using `--lemmatize` currently contains: [suffix *-s*].
