import os
import re
import nltk
from nltk.tokenize import word_tokenize

file_state_name = open('./auxiliary files/state_name.txt').read()
state_name = [w for w in re.split('\n',file_state_name) if not w==''] 

StateFullname = [re.split(',',w)[0] for w in state_name]
StateAbbrevation = [re.split(',',w)[1] for w in state_name]

# Define a set of pattern we will use to split

ZipCodeFullPattern = re.compile('|'.join(['\\b' + w.lower() + '.{0,3}\d{5}\\b' for w in StateFullname]),re.IGNORECASE)
ZipCodeAbbPattern = re.compile('|'.join(['\\b'+w[0]+'\W?['+w[1]+'|'+w[1].lower()+'].{0,3}\d{5}\\b' for w in StateAbbrevation]))

ZipCodeExtraPattern = ['tribune.?[0-9BtlifoOS]{5}', #tribune + 5 number
                       'tribune.{,5}6\d{4}',
                       'chicago\s.{,6}\d{5}?'] #chicago + space + something + five numbers

ZipCodeExtraPattern = re.compile( '|'.join(ZipCodeExtraPattern),re.IGNORECASE ) #this one ignores case

ZipCodeExtraPattern2 = ['I.?[L|l].?[L|l].?\s\d{5}', # detect ILL as Illinois
                        'I[Ll]{1,2}.?\s[0-9BtlifoOS]{5}', # detect IL
                        'IL.?6[0oO]{1,2}[0-9BtlifoOS]{2,3}', # detect IL
                        'I.?I.?\s\d{5}', # detect II as Illinois
                        'It.?\s\d{5}', # detect It + 5 numbers as Illinois        
                        '[I|i]n\s\d{5}\s', #In + something + five numbers (as zip code)
                        'MCB\s\d{3}', #MCB + space + 3 digits
                        'BOX\sM[A-Z ]{2,3}\s[0-9BtlfoO]{3}', #BOX + space + M + two more character + 3 digits 
                        'D.?C.?\s\d{5}'] # 'D.?C.?\s\d{5}' = DC

ZipCodeExtraPattern2 = re.compile( '|'.join(ZipCodeExtraPattern2) ) #Note: No "re.IGNORECASE"

SteetNamePattern = ['\d{2,5}[\s\w]+\save',
                    '\d{2,5}[\s\w]+\sblvd',
                    '\d{2,5}[\s\w]+\sstreet',
                    '\d{2,5}[\s\w]+\shgwy',
                    '\d{2,5}[\s\w]+\sroad',
                    '\d{2,5}\s\w*\sdrive',
                    '\d{2,5}\s\w*\sst.?\sboston',
                    '\d{2,5}\s\w*\sst.?\slawrence',
                    '\d{2,5}\s\w*\s\w*\sst\scambridge',
                    '^\d{2,5}\s\w*\sst.?\s',
                    '^\d{2,5}\s\w*\s\w*\sst\W',
                    '\sfloor\sboston$',
                    'glo[6b]e.{,3}office'] # globe office

SteetNamePattern = re.compile( '|'.join(SteetNamePattern),re.IGNORECASE )

EndingPhrasePattern = ['equal opportunit[y|ies]', #EoE
                       'affirmative.?employer\s?', #affirmative[anything]employer
                       'i[n|v].?confidence.?\s?', #in confidence
                       'send.{,10}resume\s?',
                       'apply.{,20}office',
                       'submit.{,10}resume\s?',
                       'please\sapply',
                       'for\sfurther\sinformation\.{,20}contact', 
                       '\d{2,4}\sext.?\s\d{2,4}', #Phone number: numbers + ext + numbers
                       '\d{3}.\d{3}-\d{4}\s?'] #Phone number: 3 numbers + anything + 3 numbers + hyphen + four numbers'

EndingPhrasePattern = re.compile('|'.join(EndingPhrasePattern),re.IGNORECASE)

ListFirmIndicator = ['co','company','inc','corporation','inc','corp','llc',"incorporated"]
ListFirmNoTitleIndicator = ['associates','associate']

#...............................................#

def AssignFlag(InputString):
    # this function detect address / ending phrase
    AddressFound = False
    EndingPhraseFound = False
   
    if re.findall(ZipCodeFullPattern,InputString):
        AddressFound = True
    if re.findall(ZipCodeAbbPattern,InputString):
        AddressFound = True
    if re.findall(ZipCodeExtraPattern,InputString):
        AddressFound = True
    if re.findall(ZipCodeExtraPattern2,InputString):
        AddressFound = True
    if re.findall(SteetNamePattern,InputString):
        AddressFound = True
    if re.findall(EndingPhrasePattern,InputString):
        EndingPhraseFound = True

    return AddressFound , EndingPhraseFound