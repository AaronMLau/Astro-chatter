import re
import wikipedia

documents = []

def clean(word):
    return re.sub(r'\W+', '', word)

def frequency(term,words):
    return (float(term)/float(words))

class document:
    # Computing the term_frequency for a document is a relatively inefficient process. 
    # We must iterate over the entire document to calculate the frequency of a single word. 
    # To make this process more efficient we should pre-compute the term frequencies of a document. 
    # The initializer should construct a dictionary which maps from terms (string) to their frequency in the document (floats).
    def pre_compute(self):
        mydict = {}
        self.total = 0
        if self.wiki is None:
            return None
        for word in self.wiki.content:
            self.total += 1
            cleaned_word = clean(word)
            if cleaned_word in mydict:
                mydict[cleaned_word] += 1
            else:
                mydict[cleaned_word] = 1
        self.dict = {}
        for word in mydict:
            self.dict[word] = frequency(mydict[word],self.total)
        return self

    def term_frequency(self,term):
        if(term in self.dict):
            return self.dict[term]
        return 0
        
    def get_words(self):
        words = []
        for word in self.dict:
            if word not in words:
                words.append(word)
        return words

    def get_name(self):
        return self.name


    def __init__(self,name):
        self.name = name
        self.wiki = get_from_wiki(name)

def get_from_wiki(article_name):
    # check article exsists, get most relevant, and return it
    results = wikipedia.search(article_name)
    for result in results:
        if(result == article_name):
            return wikipedia.WikipediaPage(result)
    return None
    pass