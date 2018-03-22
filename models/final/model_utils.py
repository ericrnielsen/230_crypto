import pandas as pd
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import string
import os

# Helper functions

def print_distribution(df, labels_column_name):
    n = df.shape[0]
    print("{} labels frequency:".format(labels_column_name))
    print("Value\tCount\tPercent")
    indeces = df[labels_column_name].value_counts().index.tolist()
    counts = df[labels_column_name].value_counts().tolist()
    for val, count in zip(indeces, counts):
        print("{}\t{}\t{}%".format(val, count, (count / float(n)) * 100))
    
def get_max_words(text_arr):
    max_words = 0
    for line in text_arr:
        if not isinstance(line, str):
            line = str(line)
        num_words = len(line.split())
        if num_words > max_words:
            max_words = num_words
    return max_words

# Helper class for streaming the data to train the Word2Vec model

class CorpusReader:
    '''
    Class to read in text files from directory/files, clean the text and allow 
    text to be iterated over using a generator
    Input:
        dir_name -- string; name of the directory to look for the files
        file_names -- (optional) list; list of the filenames to process, if not given, 
                      will walk directory and open all files
        sample_size -- (optional) integer; Allows you to specify a size of lines to read in to perform testing on 
                       a smaller subset of the data if the amount of data may be very large
    Output:
        list of tokens generated from string input
    '''
    def __init__(self, dir_name, file_names=None, sample_size=None, source=False):
        self.dir_name = dir_name
        self.sample_size = sample_size
        self.source = source
        if file_names:
            assert isinstance(file_names, list)
            self.file_names = file_names
        else:
            self.file_names = None
        
    def __iter__(self):
        if self.file_names:
            for fname in self.file_names:
                with open(os.path.join(self.dir_name, fname), 'r') as f_in:
                    print("Parsing file: {}".format(fname))
                    for iter_num, line in enumerate(f_in):
                        if self.sample_size and iter_num > self.sample_size:
                            break
                        else:
                            tokens = self._clean_and_tokenize(line)
                            #tokens = self._remove_stop_words(tokens)
                            if self.source:
                                yield tokens, fname
                            else:
                                yield tokens

        else:
            for fname in os.listdir(self.dir_name):
                if fname.endswith('.txt'):
                    with open(os.path.join(self.dir_name, fname), 'r') as f_in:
                        print("Parsing file: {}".format(fname))
                        for line in f_in:
                            tokens = self._clean_and_tokenize(line)
                            #tokens = self._remove_stop_words(tokens)
                            yield tokens
    
    def _clean_and_tokenize(self, text):
        # Do some initial cleaning
        text = text.replace(r"http", "") # Get rid of http tags standalone
        text = text.replace(r"@", "at") # Replace @ symbols with at
        text = text.replace(r"/", " ")
        text = text.replace(r".", " ")
        tokens = word_tokenize(text)
        
        # convert to lower case
        tokens = [w.lower() for w in tokens]
        
        # remove punctuation from each word
        table = str.maketrans('', '', string.punctuation)
        stripped = [w.translate(table) for w in tokens]
        
        # remove remaining tokens that are not alphabetic
        words = [word for word in stripped if word.isalpha() or word.isdecimal()]
        #words = stripped
        return words
    
    def _remove_stop_words(self, tokens):
        # Filter out stop words
        stop_words = set(stopwords.words('english'))
        tokens = [word for word in tokens if not word in stop_words]
        return tokens