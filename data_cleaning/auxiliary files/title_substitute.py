import os
import re
import sys
import platform
import shutil
import enchant, difflib
import io

d = enchant.DictWithPWL("en_US", 'myPWL.txt')

#...............................................#
# This python module cleans titles
# (1.) substitute word-by-word: includes plural => singular, abbrevations...
# (2.) substitute phrases
# (3.) general plural to singular transformation
#...............................................#

def WordSubstitute(InputString, word_substitutes):
    # This function makes word-by-word substitutions (See: word_substitutes.csv)
    # For each row, everything in the second to last column will be substituted with the first column
    # Example, one row reads "assistant | assistants | asst | asst. | assts"
    # If any word is "assistants", "asst." or "assts" is found, it will be substituted with simply "assistant"    

    InputTokens = [w for w in re.split('\s|-', InputString.lower()) if not w=='']
    
    ListBase = [re.split(',', w)[0] for w in word_substitutes] # list of everything in the first column
    
    RegexList = ['|'.join(['\\b'+y+'\\b' for y in re.split(',', w)[1:] if not y=='']) for w in word_substitutes]
    # regular expressions of everyhing in the second to last column
    
    OutputTokens = InputTokens[:] #copying the output from input
    
    for tokenInd in range(0,len(OutputTokens)):
        token = OutputTokens[tokenInd] # (1) For each word...
        for regexInd in range(0,len(RegexList)):   
            regex = RegexList[regexInd] # (2) ...for each set of regular expressions...
            baseForm = ListBase[regexInd] 
            if re.findall(re.compile(regex),token): # (3) ...if the word contains in the set of regular expressions... 
                OutputTokens[tokenInd] = baseForm # (4) ...the word becomes that baseForm = value of the first column.
    return ' '.join(OutputTokens)

#...............................................#

def PhraseSubstitute(InputString, phrase_substitutes):
    # This function makes phrases substitutions (See: phrase_substitutes.csv)
    # The format is similar to word_substitutes.csv 
    # Example: 'assistant tax mgr' will be substituted with 'assistant tax manager'
    
    ListBase = [re.split(',',w)[0] for w in phrase_substitutes]
    RegexList = ['|'.join(['\\b'+y+'\\b' for y in re.split(',',w)[1:] if not y=='']) for w in phrase_substitutes]
    
    OutputString = InputString.lower()

    # Unlike WordSubstitute(.) function, this one looks at the whole InputString and make substitution.

    for regexInd in range(0,len(RegexList)):
        regex = RegexList[regexInd]
        baseForm = ListBase[regexInd]
        if re.findall(re.compile(regex),InputString):
            OutputString = re.sub(re.compile(regex),baseForm,InputString)
    return OutputString

#...............................................#

def SingularSubstitute(InputString):
    # This function performs general plural to singular transformation
    # Note that several frequently appeared words would have been manually typed in "word_substitutes.csv" 

    InputTokens = [w for w in re.split(' ', InputString.lower()) if not w=='']
    OutputTokens = InputTokens[:] #initialize output to be exactly as input
    
    for tokenInd in range(0,len(OutputTokens)):
        
        token = OutputTokens[tokenInd]
        corrected_token = ''

        if d.check(token): # To be conservative, only look at words that d.check(.) is true
            if re.findall('\w+ies$',token):
                # if the word ends with 'ies', changes 'ies' to 'y'
                corrected_token = re.sub('ies$','y',token) 
            elif re.findall('\w+ches$|\w+ses$|\w+xes|\w+oes$',token):
                # if the word ends with 'ches', 'ses', 'xes', 'oes', drops the 'es'
                corrected_token = re.sub('es$','',token)
            elif re.findall('\w+s$',token):
                # if the word ends with 's' BUT NOT 'ss' (this is to prevent changing words like 'business')
                if not re.findall('\w+ss$',token): 
                    corrected_token = re.sub('s$','',token) # drop the 's'
            
        if len(corrected_token) >= 3 and d.check(corrected_token):
            #finally, make a substitution only if the word is at least 3 characters long...
            # AND the correction actually has meanings! 
            OutputTokens[tokenInd] = corrected_token
        
    return ' '.join(OutputTokens)

#...............................................#

def SubstituteTitle(InputString,word_substitutes,phrase_substitutes):
    # This is the main function

    # (1.) Initial cleaning:
    CleanedString = re.sub('[^A-Za-z- ]','',InputString)
    CleanedString = re.sub('-',' ',CleanedString.lower())
    CleanedString = ' '.join([w for w in re.split(' ', CleanedString) if not w==''])

    # (2.) Three types of substitutions:

    if len(CleanedString) >= 1:
        CleanedString = PhraseSubstitute(CleanedString, phrase_substitutes)
        CleanedString = WordSubstitute(CleanedString, word_substitutes)
        CleanedString = SingularSubstitute(CleanedString)
        CleanedString = PhraseSubstitute(CleanedString, phrase_substitutes)

    # (3.) Get rid of duplicating words:
    # This step is to reduce dimensions of the title.
    # for example, "sale sale engineer sale " would be reduced to simply "sale engineer"
    
    ListTokens = [w for w in re.split(' ',CleanedString) if not w=='']
    FinalTokens = list()

    for token in ListTokens: # for each word...
        if not token in FinalTokens: # ...if that word has NOT appeared before...
            FinalTokens.append(token) # ...append that word to the final result. 
            
    return ' '.join(FinalTokens)  

#...............................................#
