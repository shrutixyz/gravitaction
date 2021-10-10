text = "following the suggestions from his mother on 11th April 2010 styles auditioned as a solo contestant ...... so basically for the 7 series of the British revised singing competition called as factor singing a retention of Stevie wonder's isn't she lovely ..."

# text = "Graphology inference of character from a person's handwriting The theory underlying graphology is that handwriting is an expression of personality hence a systematic analysis of the way words and letters are formed can reveal traits of personality"

import language_tool_python 
import re

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize


from nltk.stem import PorterStemmer

tool = language_tool_python.LanguageTool('en-US')

nltk.download('stopwords')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

def grammar_check(text):
    t = text.replace(".", "")
    # print(t)
    matches = tool.check(t)
    grammar = []
    print(len(matches))
    for i in matches:
        
        if not (i.ruleIssueType == "whitespace" or i.ruleIssueType == "typographical" or i.ruleIssueType == "misspelling"):
            print(i.ruleIssueType,i.message , i.replacements,i.context,"tada")
            temp = {
             'ruleIssueType' : i.ruleIssueType,
             'message' : i.message,
             'context' : i.context
            }
           
            grammar.append(temp)
        else:
            print(i.ruleIssueType, "nada", i.message, i.replacements)
        # print(i.ruleId, i.ruleIssueType)
        # print("\n")
    print(grammar)
    return grammar


def pace(text, time):
    pass


def tone(text):
    pass


def preprocess(text):
    #set stop words
    pre = []
    stop_words = set(stopwords.words('english'))

    words = nltk.word_tokenize(text)
    words = [w.lower() for w in words if not w in stop_words] 

    tagged = nltk.pos_tag(words)

    print(tagged)
  
    for tag in tagged:
        if not (tag[1] == "NNP" or tag[1] == "NNPS"):
            pre.append(tag[0])

    
    return pre



def get_common_words(text):
    
    lines = []
    vocab = []
    with open('common.txt') as f:
        line = f.readlines()
        
    for l in line:
        lines.append(l[:-1])
            
    words = preprocess(text)
    blacklist = []
    for word in words:
        if word not in lines and not bool(re.search(r'\d', word)) and bool(re.match('^[a-zA-Z0-9]*$',word)):
            if word in vocab:
                vocab.remove(word)
                blacklist.append(word)
            elif word not in vocab and word not in blacklist:
                vocab.append(word)
    
    numerator = len(vocab)
    l = text.replace(".","")
    temp = l.split(" ")
    
    
    
    denominator = len(temp)

    # multuply by 100 to get percentage and since 10% == 0.9, multiply the result by 0.09 ===> multiply by 100 * 0.09
    initial_index = (numerator / denominator) * 9

    print(initial_index, 'beef')
    if initial_index < 0.2:
        initial_index = 0.2
    elif initial_index > 0.9:
        initial_index = 0.9
    
    return initial_index
    

def get_filler(text):
    
    #read filler words from txt file
    lines = []
    filler = []
    with open('filler.txt') as f:
        line = f.readlines()
        
    for l in line:
        lines.append(l[:-1])

    l = text.replace(".","")
    words = l.split(" ")

    for word in words:
        if word in lines and word not in filler:
            filler.append(word)

    return filler


def most_frequently_words(text):
    pass

ans = get_filler(text)
print(ans)

    
