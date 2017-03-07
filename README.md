# The Contextfinder
Takes a dictionary (as [JSON](http://www.json.org/)-file) and identifies contexts in which spelling variation between two characters occurs. 


## Description
The contextfinder takes the following arguments:

    variantfinder (variant_one, variant_two, input_dict, pre_window, post_window, differential_cutoff=100)
    
    Parameters:
    variant_one --- a character, presumably used interchangeably with variant_two. 
    variant_two ---  a character, presumably used interchangeably with variant_one. 
    input_dict --- a JSON file containing the complete dictionary. 
    pre_window  --- determines the number of characters preceding variant_one or variant_two to be taken into account. 
    post_window --- determines the number of characters following variant_one or variant_two to be taken into account. 
    differential_cutoff --- sets a threshold regarding the differential between variant_one and variant_two; items above the threshold will be excluded. Defaults to 100, i.e. all items included. 


## How to run it
Run it in a shell. See here for instructions. 

#### The basics. 

This example shows the basic setup for the contextfinder: 

    python contextfinder.py u v /Users/ps22344/Downloads/editdistance/dictbuilder_output.json 1 3 20 
    
This will find all items that occur with u and v interchangeably. It will extract a context window of one character preceding and up to three characters following the variant. 
It will exclude all items with a differential of more than 20 percentage points, i.e. any item that has more than 80 percent of variant_one or variant_two will be excluded. 


## Notes:


## Sample output:

****
MOST FREQUENT CONTEXTS of u - v variation (token counts < 10 excluded) 
****

i_a	tokens: 45	7.589% of total,u: 53.33%, v: 46.67%
d_i	tokens: 24	4.047% of total,u: 41.67%, v: 58.33%
r_e	tokens: 22	3.71% of total,u: 45.45%, v: 54.55%
n_e	tokens: 10	1.686% of total,u: 40.0%, v: 60.0%
n_i	tokens: 10	1.686% of total,u: 40.0%, v: 60.0%
i_e	tokens: 10	1.686% of total,u: 50.0%, v: 50.0%
_g	tokens: 10	1.686% of total,u: 50.0%, v: 50.0%

****
HIGHEST DIFFERENTIAL IN VARIANT USE of u - v variation (token counts < 10 excluded)
n_e	tokens: 10	1.686% of total,u: 40.0%, v: 60.0%
n_i	tokens: 10	1.686% of total,u: 40.0%, v: 60.0%
d_i	tokens: 24	4.047% of total,u: 41.67%, v: 58.33%
r_e	tokens: 22	3.71% of total,u: 45.45%, v: 54.55%
i_a	tokens: 45	7.589% of total,u: 53.33%, v: 46.67%
i_e	tokens: 10	1.686% of total,u: 50.0%, v: 50.0%
_g	tokens: 10	1.686% of total,u: 50.0%, v: 50.0%




# ASVI - A tool for Automatic Spelling Variant Identification. 
This tool identifies spelling variants of words by computing the edit distance. 


Schultz, Patrick. ASVI: a tool for automatic spelling variant identification, 2016, https://github.com/patrickschu/editdistance [Online; accessed 2016-11-16].
