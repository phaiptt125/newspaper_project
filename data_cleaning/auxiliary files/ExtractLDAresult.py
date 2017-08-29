import re

'''
The command 'lda.show_topics' gives a pretty complicate output format
for example, if given 2 words and 2 topics, it will show:

[(0, [('price', 0.014396994044837077), 
('new', 0.0122260497589219)])
, 
(1, [('opportun', 0.020830242773974533), 
('experi', 0.019701193739871937)])]

The first element belongs to the first topic

TopicKeyword[0] = 
(0, [('price', 0.014396994044837077), ('new', 0.0122260497589219)])

TopicKeyword[0][0] = 0 
TopicKeyword[0][1] = [('price', 0.014396994044837077), ('new', 0.0122260497589219)]

so the way to extract is to loop over TopicKeyword[Ind][1], where Ind is topic number
'''

def GetWordScore(TopicKeyword):
    WordScoreList = list() # list of word and its score 
    for Ind in range(0,len(TopicKeyword)): #loop by topics
        WordsThisTopic = TopicKeyword[Ind][1]
        for WordScore in WordsThisTopic: #loop by words
            Word = WordScore[0]
            Score = "{0:.3f}".format(WordScore[1]) #round to 3 decimal 
            #"{0:.2f}".format(13.949999999999999) = '13.95'
            WordScoreList.append(str(Ind) + '\t' + Word + '\t' + str(Score))
    return WordScoreList 
    
def GetWordList(WordScoreList,TopicNum):
    ListWordByTopic = ['']*TopicNum
    for item in WordScoreList:
        Split = re.split('\t',item)
        ListWordByTopic[int(Split[0])] = ListWordByTopic[int(Split[0])] + '\t' + Split[1]
    return [[y for y in re.split('\t',w) if not y==''] for w in ListWordByTopic if not w=='']

#...............................................#

'''
"docTopic" item contains document score by topic, has length = number of doc
NOTE: topic score that is below a certain threshold is set to be zero and not report
For example:

docTopic[0] = [(0, 0.1334268305392638), (2, 0.8638742905886998)]

means the first document has 0.13 for topic 0, 0 for topic 1 and 0.86 for topic 2
'''

def GetDocumentScore(docTopic,TopicNum):
    OutputTable = list()    
    for Ind in range(0,len(docTopic)):
        ScoreThisDoc = docTopic[Ind]
        RecordScore = ['0']*TopicNum
        for item in ScoreThisDoc:
            RecordScore[item[0]] = "{0:.3f}".format(item[1])
        OutputTable.append( '\t'.join(RecordScore) )
    assert( len(docTopic) == len(OutputTable) )
    return OutputTable

#...............................................#
