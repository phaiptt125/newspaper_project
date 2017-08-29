import re
import enchant, difflib
from enchant import DictWithPWL

#...............................................#

def ComputeSpellingError(rawtext,mydict):

    d = enchant.DictWithPWL("en_US", mydict)
    tokens = [w for w in re.split(' ',rawtext.lower()) if not w == '']
    tokens = [re.sub(r'[^a-z]','',w) for w in tokens]
    tokens = [w for w in tokens if not w=='']

    CountInDict = 0
    CountNotInDict = 0
    CountTotal = len(tokens)
    if CountTotal > 0:
        for word in tokens:
            if len(word)==1:
                CountNotInDict += 1
            elif d.check(word):
                CountInDict += 1
            else:
                CountNotInDict += 1
        Ratio = str(round(CountInDict/CountTotal,2))
    else:
        Ratio = str(0)

    TotalWord = str(CountTotal)
    Output = [TotalWord,Ratio]
    return Output
#...............................................#

def RecordCorrectSpelling(rawtext):
    
    d = enchant.Dict("en_US")
    tokens = [w for w in re.split(' ',rawtext.lower()) if not w == '']
    tokens = [re.sub(r'[^a-z]','',w) for w in tokens]
    tokens = [w for w in tokens if len(w) >= 3]
    tokens = [w for w in tokens if not w=='']
    
    TotalWord = len(tokens)

    if TotalWord > 0:
        correct_tokens = [w for w in tokens if d.check(w)]
        correct_tokens = [w for w in correct_tokens if not w=='']
        output_text = ' '.join(correct_tokens)
        WordCount = str(len(correct_tokens))
    else:
        output_text = ''
        WordCount = str(0)

    Output = [WordCount,output_text]
    return Output

#...............................................#   



