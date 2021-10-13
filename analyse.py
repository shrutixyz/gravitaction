text = "following the suggestions from his f***ing mother on 11th April 2010 styles auditioned as a solo contestant ...... so basically for the 7 series of the British revised singing competition called as factor singing a retention of Stevie wonder's isn't she lovely ..."

# text = "Graphology inference of character from a person's handwriting The theory underlying graphology is that handwriting is an expression of personality hence a systematic analysis of the way words and letters are formed can reveal traits of personality"

import language_tool_python 
import re

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize

from collections import Counter

from nltk.stem import PorterStemmer
from nltk.util import pr

tool = language_tool_python.LanguageTool('en-US')

nltk.download('stopwords')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')

from nltk.corpus import wordnet


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
    # text = text.replace(".", "")
    words = split_words(text)
    total_words = len(words)

    limit = (total_words / time) * 60
    print(words)
    return limit


def tone(text):
    pass

def preprocess(text):
    #set stop words
    pre = []
    text = text.replace(".", "")
    stop_words = set(stopwords.words('english'))

    words = nltk.word_tokenize(text)
    words = [w.lower() for w in words if not w in stop_words] 

    tagged = nltk.pos_tag(words)

    print(tagged)
  
    for tag in tagged:
        if not (tag[1] == "NNP" or tag[1] == "NNPS"):
            pre.append(tag[0])

    
    return pre

def split_words(text):
    text = text.replace(".", "")
    words = text.split(" ")

    for word in words:
        if len(word) < 1:
            words.remove(word)
    return words

def get_common_words(text):
    
    lines = []
    vocab = []
    with open('common.txt') as f:
        line = f.readlines()
        
    for l in line:
        lines.append(l[:-1])
            
    words = preprocess(text)
    # blacklist = []
    for word in words:
        if word not in lines and not bool(re.search(r'\d', word)) and bool(re.match('^[a-zA-Z0-9]*$',word)):
            
            if word not in vocab:
                vocab.append(word)
    
    numerator = len(vocab)
    print(vocab, "ye rahi aampki vocab")
    temp = split_words(text)
    
    
    if len(temp) > 0:
        denominator = len(temp)
    else:
        denominator = 1
    # multuply by 100 to get percentage and since 10% == 0.9, multiply the result by 0.09 ===> multiply by 100 * 0.09
    initial_index = (numerator / denominator) * 9

    # print(initial_index, 'love')
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

    
    words = split_words(text)

    for word in words:
        if word in lines and word not in filler:
            filler.append(word)

    return filler


def most_frequently_words(text):

    #preprocess
    words = preprocess(text)

    # stop_words = set(stopwords.words('english'))

    
    # words = [w.lower() for w in words if not w in stop_words] 
    
    for word in words:
        if bool(re.search(r'\d', word)):
            words.remove(word)

    #get freq
    ref = Counter(words)
    a = {}
    for word in ref:
        if ref[word] > 1:
            a[word] = ref[word]

    ans = sorted(a.items(), key=lambda item: item[1])
    ans = ans[::-1]

    if len(ans) > 5:
        ans = ans[:5]
    print(ans, "aur ye rahi freq")
    return ans
    

def getsynonyms(word):

    #Creating a list 
    synonyms = []
    for syn in wordnet.synsets(word):
        for lm in syn.lemmas():
                synonyms.append(lm.name())#adding into synonyms
    return (list(synonyms))


def banned_words(text):

    words = split_words(text)
    count = 0
    for word in words:
        if "*" in word:
            count += 1
    return count 

# print(most_frequently_words(text))
# print(getsynonyms("apprehensive"))

    
