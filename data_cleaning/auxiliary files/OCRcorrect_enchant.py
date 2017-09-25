import os
import re
import sys
import nltk
import enchant, difflib
import operator
from enchant import DictWithPWL

#...............................................#
# This python function performs word-by-word spelling correction
#...............................................#

def EnchantErrorCorrection(InputByLine,mydictfile):

    # "InputByLine" is a string of the text by line.
    # "mydictfile" is a filename (e.g., "myPWL.txt") for personal word list
    # The function returns " ' '.join(OutputList) " as a string

    d = enchant.DictWithPWL('en_US', mydictfile) # define spell-checker 

    # http://pythonhosted.org/pyenchant/tutorial.html
    # http://stackoverflow.com/questions/22898355/pyenchant-spellchecking-block-of-text-with-a-personal-word-list
    
    InputList = [w for w in re.split(' ',InputByLine) if not w=='']
    OutputList = list()
    
    for Word in InputList:
        if len(Word)>=3: # only check words with length greater than or equal to 3
            if d.check(Word): #d.check() is TRUE if the word is correctly spelled
                OutputList.append(Word) #append the old word back
            else: #d.check() is FALSE if the word is correctly spelled
                correct = d.suggest(Word) #get a suggestion
                count=0
                if correct: #if a suggestion is not empty
                    dictTemp,maxTemp = {},0  ##ea
                    for b in correct:  ## ea
                        count=count+1
                        if count<8:
                            tmp = max(0,difflib.SequenceMatcher(None, Word.lower(), b.lower()).ratio()-(1e-3)*count); ##ea
                            dictTemp[tmp] = b   ##ea
                            if tmp > maxTemp:   ##ea
                                maxTemp = tmp   ##ea                         
                    if maxTemp>=0.8:
                        OutputList.append(dictTemp[maxTemp])  ##ea
                    else:
                        OutputList.append(Word)
                else: #if a suggestion is empty, just append the old word back
                    OutputList.append(Word)
        else: # if the word is less than 3 characters, just append the same word back to output
            OutputList.append(Word)
            
    return ' '.join(OutputList) 

#...............................................#
