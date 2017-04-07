# ASVI
Takes a wordlist, a corpus of folders containing text files, and the desired [edit distance](http://www.nltk.org/_modules/nltk/metrics/distance.html) as input. 
Identifies all variants of the words in the wordlist within this edit window. 

## Description
ASVI takes the following arguments:

    editdist_shell.py (wordlist, input_dir, distance)
    
    Parameters:
    wordlist --- path to a file containing a list of words, one word per line 
    input_dir ---  path to a folder whose subfolders contain text files with corpus data. Only files with .txt extension will be processed. 
    distance --- the edit distance within which ASVI will search for variants.  

## How to run it
Run it in a shell. 

Don't know how to do that? Help with running scripts on [Mac](https://github.com/tgdp/tools/blob/master/run_mac.MD) and [Windows](https://github.com/tgdp/tools/blob/master/run_windows.MD) computers. 

Never worked with Python before? Here is how to set up your [Windows](https://github.com/tgdp/tools/blob/master/setup_windows.MD) or [Mac](https://github.com/tgdp/tools/blob/master/setup_mac.MD) computer. 

#### The basics. 

This example shows the basic setup for the ASVI: 

        editdist_shell.py wordlist.txt  corpora 2

    
For each word in wordlist.txt, this will find all items that occur within the corpus that are 2 insertions, deletions, etc distant from the word. 


## Sample output:

    python editdist_shell.py wordlist.txt  corpora

wordlist.txt contains only the word _getting_. 

>***
>55 Variants for 'getting':
>
>beating, begetting, beotting, cutting, depting, dyetting, eating, eting, fitting, fretting, geating, gebring, gelding, gemeting, gemitting, gesing, geswing, getang, getig, getin, getten, gettings, gettyn, gettynge, getyng, geuing, geving, gewring, greting, heating, hitting, jesting, lething, leting, letting, lettinge, lettyng, meating, meeting, meting, potting, putting, resting, rotting, rutting, sething, setling, setting, settinge, settling, settyng, sitting, sytting, weting, wetting
>
>
>***
>
>Token counts for variants:
>
>meeting 27.0
>
>eating 24.0
>
>sitting 17.0
>
>putting 17.0
>
>setting 16.0
>
>[...]


# ASVI - A tool for Automatic Spelling Variant Identification. 
This tool identifies spelling variants of words by computing the edit distance. 


Schultz, Patrick. ASVI: a tool for automatic spelling variant identification, 2016, https://github.com/patrickschu/editdistance [Online; accessed 2016-11-16].