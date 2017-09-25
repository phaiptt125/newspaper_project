import os
import re
import sys
import nltk
import enchant, difflib
import operator
from enchant import DictWithPWL
from edit_distance import *

#...............................................#
# This python function performs spelling correction
# on words with hyphen
#...............................................#

def CorrectHyphenated(InputByLine,mydictfile):

    # "InputByLine" is a string of the text by line.
    # "mydictfile" is a filename (e.g., "myPWL.txt") for personal word list
    # The function returns a string as output

    d = enchant.DictWithPWL('en_US', mydictfile) # define spell-checker 
    # http://pythonhosted.org/pyenchant/tutorial.html
    # http://stackoverflow.com/questions/22898355/pyenchant-spellchecking-block-of-text-with-a-personal-word-list

    text = InputByLine 

    HyphenWords = re.findall(r'\b[a-zA-Z]+-\s?[a-zA-Z]+\b', InputByLine)
    # "HyphenWords" is a list of potential hyphen word corrections 

    for word in HyphenWords:
        WordForCheck = re.sub('[- ]','',word)
        # Newspaper tends to the cut to a new line in the middle of a word. 
        # Therefore, most corrections are just removing "-" and " "
        CorrectionFlag = 0 #indicator for correction
        if d.check(word): # if the word (with hyphen) is already correct
            pass #do nothing
        elif d.check(WordForCheck): # elif the word without "-" and " " is correct
            Correction = WordForCheck
            CorrectionFlag = 1
        elif d.suggest(WordForCheck): #get a suggestion
            ListSuggest = [w for w in d.suggest(WordForCheck) if not ' ' in w]
            if len(ListSuggest) > 0:
                DistanceSuggest = [EditDistance(w,WordForCheck) for w in ListSuggest]
                min_index, min_value = min(enumerate(DistanceSuggest), key=operator.itemgetter(1))
                if min_value <= 3: #if the difference is not exceeding 3
                    Correction = ListSuggest[min_index]
                    CorrectionFlag = 1

        if CorrectionFlag == 1:
            text = re.sub(word,Correction,text)
            
    return text

#...............................................#
