import os
import sys
sys.path.append("/home/kylis/Desktop/git/FWG/src")

model_path = "/home/kylis/Desktop/FYP/model"
data_path = "/home/kylis/Desktop/FYP/data"
cache_path = "/home/kylis/Desktop/FYP/cache"

from FWG import Corpus
from FWG import utils
from FWG import Concepts

nlp = utils.init_spacy_nlp()

comments = ["I love apples, not the apple phone", "Green apple is a type of apple", "Apple is a kind of fuits, I like apple, I love apple", "Apple is a kind of fuits, I like apple, I love apple"]

c = Corpus.Corpus(comments, nlp, lexical_name=True, concepts_config=None)
c.gen_td_vec()

print(c.FD)