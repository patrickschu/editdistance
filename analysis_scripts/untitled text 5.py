def checker(new_name, old_names):
    """
    The checker takes a string new_name and checks if it is contained in the list old_names.
    It prints out the results.
    """ 
    print "***\n\ninitializing the checker"
    print "searching for ", new_name
    print "old names", old_names
    old_names= sorted(old_names)
    #set the match variable to false
    namematch= False
    #iterate over list while new_name does not match
    while not namematch and len(old_names) > 1:
        middle= len(old_names)/2
        print "middle item is", old_names[middle], "middle index is", middle
        #match
        if old_names[middle] == new_name:
            namematch= True
        #no match
        else:
            if sorted(list((new_name, old_names[middle])))[0] != new_name:
                print "word is to the right"
                old_names = old_names[middle:]
            else:
                print "word is to the left"
                old_names = old_names[:middle]
    #check for list of length 1: is it new_name
    if (len(old_names)) == 1 and (old_names[0] == new_name):
        namematch = True
    if not namematch: 
        print "this name is not taken:", new_name
    else:
        print "this name is taken:", new_name
        
    
names_list= [u'annie', u'max', u'chris', u'11alpha', u'zotti', u'zatti', u'zutti', u'?andy', u'getr\xfc', u'zilly']

checker('max', names_list)
checker('fail', names_list)