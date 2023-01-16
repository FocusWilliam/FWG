from . import utils
import copy
import Kkit

class Concept_conf:
    def __init__(self, num=20, layers=[3,3,3], cache_path="./cache/MCG", probase=None):
        self.num=num
        self.layers = layers
        self.cache_path=cache_path
        self.probase=probase

class Node:
    def __init__(self, word, prob):
        self.word = word
        self.prob = prob
        self.children = []
    def __repr__(self):
        return self.word
    def __str__(self):
        return self.word

def build_concept_tree(word_node, layers, index, cache_path = "./cache/MCG", probase = None):
    if index >= len(layers):
        return
    temp = utils.get_concept_prob(word_node.word, layers[index], cache_path, probase)
    if len(temp)!=0:
        for w,p in temp.items():
            word_node.children.append(Node(w,p))
        for n in word_node.children:
            build_concept_tree(n, layers, index+1, cache_path, probase)
    else:
        return

def deep_search_key_concept(word_node, path, paths):
    path.append(word_node.word)
    if len(word_node.children) != 0:
        for i in word_node.children:
            deep_search_key_concept(i, copy.copy(path), paths)
    else:
        if Kkit.list_in_list(path, utils.key_concepts, "any"):
            paths.append(path)
        return