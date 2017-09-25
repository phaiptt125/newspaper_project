import os
import re
import sys

def DetermineUppercase(string):
    # This function determines whether a line is uppercase
    # There are cases where there are some non-uppercased as well
    # example: ENGINEERS MICRowAVE...which should be considered as uppercase
    # This would help detecting job titles
    StringUppercase = re.sub('[^A-Z]','',string) # take out all non uppercase
    if string.isupper(): # perfect uppercase
        Output = True
    elif len(string) > 4 and len(StringUppercase)/len(string) >= 0.8:
        # this line allows some "imperfect" uppercase lines
        # (length of string is long enough and contains 80% of uppercase characters)
        Output = True
    else:
        Output = False
    return Output

#...............................................#

def IndexAll(word,tokens): # IndexAll('b',['a','b','c','b','c','c']) = [1, 3]
    return [i for i,v in enumerate(tokens) if v == word]

#...............................................#

def NextWordIsNotNumber(word,tokens):
    Output = True
    for location in IndexAll(word,tokens):
        if location == len(tokens) - 1: # if the word is the last word -- skip
            pass
        elif re.findall('\d', tokens[location + 1] ):
            Output = False
    return Output

#...............................................#

def UppercaseNewline(ListByLine,LineBreak):
    # This function adds an extra line break when an uppercase word or phrases is found
    # The purpose of this function is to break the uppercase phrases within the line that contains
    # both upper and lower case words
    OutputResetLine = list()
    for line in ListByLine:
        if line.isupper(): #ignore if the whole line is already uppercase
            OutputResetLine.append(line) #just write down exactly the same
        elif len(re.findall(r'[a-z]',line)) >= 5: #the line must contain come lowercases characters
            ResetThisLine = list() 
            tokens = [w for w in re.split(' ',line) if not w=='']
            for word in tokens:
                WordNoHyphen = re.sub('-','',word) 
                if WordNoHyphen.isupper() and len(WordNoHyphen) >= 2 and NextWordIsNotNumber(word,tokens):
                    # if the line is uppercase, is long enough and is NOT followed by a set of number
                    # (because a set of uppercase followed by a set of number could be a zip code!)
                    ResetThisLine.append(LineBreak + word + LineBreak)
                else:
                    ResetThisLine.append(word)
            OutputResetLine.append(' '.join(ResetThisLine))
        else:
            OutputResetLine.append(line) #just write down exactly the same

    # At this point, some elements in the "OutputResetLine" would contain more than one line.
    # We want to convert this list such that one element is one line
    # This can be done by (1) join everything with 'LineBreak' and (2) split again   
    OutputResetLine = [w for w in re.split(LineBreak,LineBreak.join(OutputResetLine)) if not w==''] #reset lines
    return OutputResetLine

#...............................................#

def CombineUppercase(ListByLine):

    # This function combines short consecutive uppercase lines together to facilitate job title detection
    # For example: "SALE\nMANAGER\nWanted" >>> "SALE MANAGER\nWanted"
    # See DetermineUppercase(string) function above for a new definition of "uppercase".  
    
    ListByLineNotEmpty = [w for w in ListByLine if re.findall(r'[a-zA-Z0-9]',w)]
    # take out lines where no a-z, A-Z or 0-9 is found (empty lines)
    
    OutputResetLine = [''] #initialze output
    CurrentLine = 0 # current number of line  
    PreviousShortUpper = False # indicator that the previous line is short uppercase

    for line in ListByLineNotEmpty:
        LineNoSpace = re.sub('[^a-zA-Z]','',line) #this only serves the purpose of detecting uppercase line
        if DetermineUppercase(LineNoSpace) and PreviousShortUpper == True: # if this line AND the previous one is uppercase
            tokens = [w for w in re.split(' ',line) if not w=='']
            if len(tokens) <= 3: #the line must be short enough
                #add this line to the previous one
                # NOTE: "CurrentLine" does not get +1  
                OutputResetLine[CurrentLine] = OutputResetLine[CurrentLine] + ' ' + re.sub('[^A-Z0-9- ]','',line.upper())
                PreviousShortUpper = True
            else: #rather, even if the line is upper -- ignore and write down as normal if it is too long
                PreviousShortUpper = False
                OutputResetLine.append('') # prepare a new empty line
                CurrentLine += 1 # moving on to the next line
                OutputResetLine[CurrentLine] = line
                PreviousShortUpper = False 
        elif DetermineUppercase(LineNoSpace) and PreviousShortUpper == False:
            # if the line is uppercase BUT the pervious one is not => start the new line AND change "PreviousUpper" to "True" 
            OutputResetLine.append('') # prepare a new empty line
            CurrentLine += 1 # moving on to the next line
            OutputResetLine[CurrentLine] = re.sub('[^A-Z0-9- ]','',line.upper())
            PreviousShortUpper = True # change status 
        else: # if the line is not uppercase => just write it down as normally should
            OutputResetLine.append('') # prepare a new empty line
            CurrentLine += 1 # moving on to the next line
            OutputResetLine[CurrentLine] = line
            PreviousShortUpper = False 
    OutputResetLine = [w for w in OutputResetLine if not w==''] # delete empty lines
    return OutputResetLine

#...............................................#

def CheckNoTXTLost(list1, list2, AllFlag):
    #this function checks that "list1" and "list2" contains exactly the same string of chatacters
    combine_list1 = re.sub( AllFlag,'',''.join(list1).lower() ) #take out all flags (title, firm names, etc...)
    combine_list2 = re.sub( AllFlag,'',''.join(list2).lower() )
    if re.sub( '\W|\s','',combine_list1) == re.sub( '\W|\s','',combine_list2): #test
        output = True
    else:
        output = False
    return output

#...............................................#