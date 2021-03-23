# This implementation from geeks for geeks:
#https://www.geeksforgeeks.org/implement-your-own-word2vecskip-gram-model-in-python/

import re
import numpy as np
#from nltk.corpus import stopwords


def softmax(x):
    """Compute softmax values for each sets of scores in x."""
    e_x = np.exp(x - np.max(x)) 
    return e_x / e_x.sum()
# Variables: 
# V    Number of unique words in our corpus of text ( Vocabulary )
# x    Input layer (One hot encoding of our input word ). 
# N    Number of neurons in the hidden layer of neural network
# W    Weights between input layer and hidden layer
# W'   Weights between hidden layer and output layer
# y    A softmax output layer having probabilities of every word in our vocabulary
class word2vec:
    def __init__(self):
        self.N = 10
        self.X_train = []
        self.y_train = []
        self.window_size = 2
        self.alpha = 0.001
        self.words = []
        self.word_index = {}
    
    def initialize(self,V,data):
        self.V = V
        self.W = np.random.uniform(-0.8, 0.8, (self.V, self.N))
        self.W_ = np.random.uniform(-0.8, 0.8, (self.N, self.V))
        self.words = data
        for i in range(len(data)):
            self.word_index[data[i]] = i
    
    def feed_forward(self,point):
        # Multiplying one hot encoding of centre word (denoted by x) with the first weight matrix W to get hidden layer matrix h (of size N x 1).
        self.h = np.dot(self.W.T,point).reshape(self.N,1)
        # Now we multiply the hidden layer vector h with second weight matrix W’ to get a new matrix u
        self.u = np.dot(self.W_.T,self.h)
        # Note that we have to apply a softmax> to layer u to get our output layer y.
        self.y = softmax(self.u)

        # Let uj be jth neuron of layer u
        # Let wj be the jth word in our vocabulary where j is any index
        # Let Vwj be the jth column of matrix W’(column corresponding to a word wj)

        # P(wj|wi) is the probability that wj is a context word, given wi is the input word; where P(wj|wi) = yj = softmax(uj)
        # Thus, our goal is to maximise P( wj* | wi ), where j* represents the indices of context words
        return self.y
    
    def back_prop(self,point,label):
        # The parameters to be adjusted are in the matrices W and W’, 
        # hence we have to find the partial derivatives of our loss function 
        # with respect to W and W’ to apply gradient descent algorithm.
        loss = self.y - np.asarray(label).reshape(self.V,1)
        # loss shape is V x 1
        derivative_W_ = np.dot(self.h,loss.T)
        derivative_W = np.dot(np.array(point).reshape(self.V,1), np.dot(self.W_, loss).T)
        self.W_ = self.W_ - self.alpha * derivative_W_
        self.W = self.W - self.alpha * derivative_W

    # An epoch is a term used in machine learning and indicates the number of passes of the entire training dataset the
    # machine learning algorithm has completed. I.E. If the batch size is the whole training dataset then the number of epochs is the number of iterations.
    def train(self, epochs):
        for x in range(1,epochs):
            self.loss = 0
            for j in range(len(self.X_train)):
                self.feed_forward(self.X_train[j])
                self.back_prop(self.X_train[j],self.y_train[j])
                C = 0
                for m in range(self.V):
                    if(self.y_train[j][m]):
                        self.loss += -1*self.u[m][0]
                        C += 1
                self.loss += C*np.log(np.sum(np.exp(self.u)))
            print("Epoch ",x," with loss= ",self.loss)
            self.alpha *= 1/((1+self.alpha*x))

    def predict(self,word,num_predictions):
        if word in self.words:
            index = self.word_index[word]
            X = [0 for i in range(self.V)]
            X[index] = 1
            prediction = self.feed_forward(X)
            output = {}
            for i in range(self.V):
                output[prediction[i][0]] = i
            top_context_words = []
            for k in sorted(output,reverse=True):
                top_context_words.append(self.words[output[k]])
                if(len(top_context_words)>num_predictions):
                    break
            return top_context_words
        else:
            print("Word not found in dictionary")


# TODO implement word2vec
#https://towardsdatascience.com/a-word2vec-implementation-using-numpy-and-python-d256cf0e5f28

stop_words = []

#word_to_index : A dictionary mapping each word to an integer value
# {‘modern’: 0, ‘humans’: 1} 
#index_to_word : A dictionary mapping each integer value to a word
# {0: ‘modern’, 1: ‘humans’}
#corpus : The entire data consisting of all the words 
#vocab_size : Number of unique words in the corpus

# Input: a bunch of tuples of words
def train():
    pass

# Prep the data for training
def prep_data(file_name, stop_word_removal='no'):
    file_contents = []
    with open(file_name) as f:
        file_contents = f.read()
    text = []
    for val in file_contents.split('.'):
        sent = re.findall("[A-Za-z]+", val)
        line = ''
        for words in sent:
            
            if stop_word_removal == 'yes': 
                if len(words) > 1 and words not in stop_words:
                    line = line + ' ' + words
            else:
                if len(words) > 1 :
                    line = line + ' ' + words
        text.append(line)
    return text
    pass
