import os
import sys
sys.path.append("../src")

model_path = "/home/kylis/Desktop/FYP/model"
data_path = "/home/kylis/Desktop/FYP/data"
cache_path = "/home/kylis/Desktop/FYP/cache"

from FWG import Corpus
from FWG import utils
from FWG import Concepts
from FWG import Word

nlp = utils.init_spacy_nlp()

probase = utils.init_probase(os.path.join(model_path, "probase_bi"), binary=True)
probase_config = Concepts.Concept_conf(probase=probase, cache_path=os.path.join(cache_path, "MCG"))

comments = ["I love apples, not the apple phone", "Green apple is a type of apple", "Apple is a kind of fuits, I like apple, I love apple", "Apple is a kind of fuits, I like apple, I love apple"]

c = Corpus.Corpus(comments, nlp, lexical_name=True, concepts_config=probase_config)
c.frequency_filter(path=os.path.join(cache_path, "test.json"), p_value=0.05)