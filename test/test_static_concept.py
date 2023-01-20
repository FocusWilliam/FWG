import sys
sys.path.append("/home/kylis/Desktop/test/FWG/src")

from FWG import Corpus
from FWG import utils
from FWG import Review
from FWG import Concepts

from matplotlib import pyplot as plt

nlp = utils.init_spacy_nlp()
probase = utils.init_probase("/home/kylis/Desktop/test/probase_bi", binary=True)

probase_config = Concepts.Concept_conf(probase=probase)

comments = ["I love apples, not the apple phone", "Green apple is a type of apple", "Apple is a kind of fuits, I like apple, I love apple", "Apple is a kind of fuits, I like apple, I love apple"]

c = Corpus.Corpus(comments, nlp, lexical_name=True, concepts_config=probase_config)
c.concept_filter(path="./concept_filter.json")
json_dic = c.static_key_concept("./static_concept.json")
Review.visual_key_concept_statistics(json_dic)
plt.show()