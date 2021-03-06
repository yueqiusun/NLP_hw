import re
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize   
from hyperparameter import Hyperparameter as hp

  
def remove_stopwords(l):
	stop_words = set(stopwords.words('english')) 
	l_s = l.split(' ')
	filtered_sentence = [w for w in l_s if not w in stop_words] 
	return filtered_sentence

def prep_data(r, if_rs = False):
	REPLACE_NO_SPACE = re.compile("(\.)|(\;)|(\:)|(\!)|(\')|(\?)|(\,)|(\")|(\()|(\))|(\[)|(\])")
	REPLACE_WITH_SPACE = re.compile("(<br\s*/><br\s*/>)|(\-)|(\/)")
	r1 = [REPLACE_NO_SPACE.sub("", line.lower()) for line in r]
	r2 = [REPLACE_WITH_SPACE.sub(" ", line) for line in r1]
	if if_rs:
		r3 = [remove_stopwords(line) for line in r2]
	else:
		r3 = [line.split(' ') for line in r2]
	output = r3
	return output

def word_grams(sent, min=1, max=4):
	words = sent.split(' ')
	s = []
	for n in range(min, max):
		for ngram in ngrams(words, n):
			s.append(' '.join(str(i) for i in ngram))
	return s

#output list of list of words
def read_data(filename_p, filename_n, count = 9999999):
	x = []
	y = []
	raw_data_p = []
	
	with open(filename_p, "r") as f:

		line_num_p = 0
		line_p = f.readline()
		while line_p != None and line_p != "" and line_num_p<count:
			line_num_p += 1
			raw_data_p.append(line_p)
			line_p = f.readline()
	raw_data_n = []
	with open(filename_n, "r") as f:
		line_num_n = 0
		line_n = f.readline()
		while line_n != None and line_n != "" and line_num_n<count:
			line_num_n += 1
			raw_data_n.append(line_n)
			line_n = f.readline()
			
	x = x + prep_data(raw_data_p)
	x = x + prep_data(raw_data_n)
	y = y + [1] * line_num_p
	y = y + [0] * line_num_n
	return x, y

import nltk
from nltk.util import ngrams

def word_grams(sent, min=1, max=5):
	s = []
	for n in range(min, max):
		for ngram in ngrams(sent, n):
			s.append(' '.join(str(i) for i in ngram))
	return s

# This is the code cell that tokenizes train/val/test datasets
import pickle as pkl

def tokenize_dataset(dataset, min=1, max=5):
	token_dataset = []
	# we are keeping track of all tokens in dataset 
	# in order to create vocabulary later
	all_tokens = []
	
	for sample in dataset:
		tokens = word_grams(sample, min=min, max=max)
		token_dataset.append(tokens)
		all_tokens += tokens

	return token_dataset, all_tokens

