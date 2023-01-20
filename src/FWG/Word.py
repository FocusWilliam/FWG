from . import utils
import copy
import json
import numpy as np

class W:
    def __init__(self, token, lemma, POS, comment_id):
        self.POS = POS
        self.tokens = [token]
        self.lemma = lemma
        # all word embedding vectors
        self.vecs = dict()
        # top n concepts
        self.top_concept = dict()
        #key concept
        self.key_concept_chain = []
        self.key_concepts = []
        # count in corpus
        self.count = 1
        # laxical names in wordnet
        self.WN_laxical_names = []

        self.comment_id = {comment_id: 1}

    def add_count(self, n):
        self.count+=n

    def add_comment_id(self, n):
        for id, count in n.items():
            if id not in self.comment_id:
                self.comment_id[id] = count
            else:
                self.comment_id[id] += count

    def add_tokens(self, tokens):
        for token in tokens:
            if token not in self.tokens:
                self.tokens.append(token)

    def get_concepts(self, num, layers, cache_path = "./cache/MCG", probase = None):
        self.top_concept = utils.get_concept_prob(self.lemma, num=num, cache_path=cache_path, probase=probase)
        self.key_concept_chain = utils.build_key_concept_chain(self.lemma, layers, cache_path=cache_path, probase = probase)
        self.key_concepts = list(set([i[-1] for i in self.key_concept_chain]))

    def we_vec(self, name, vec):
        if isinstance(vec, np.ndarray) == False:
            print("vec class error, vec must be numpy.ndarray")
            return
        self.vecs[name] = vec

    def json_info(self):
        return self.__dict__

    def __eq__(self,other):
        return self.POS==other.POS and self.lemma==other.lemma

    def __repr__(self):
        return self.lemma+"_"+self.POS+"_"+str(self.count)

class Word(W):
    def __init__(self, token, lemma, POS, comment_id, lexical_name=False, concepts_config=None):
        super(Word, self).__init__(token, lemma, POS, comment_id)

        if lexical_name:
            self.get_lexical_name()

        if concepts_config!=None:
            self.get_concepts(concepts_config.num, concepts_config.layers, concepts_config.cache_path, concepts_config.probase)

    # def json_info(self):
    #     return {"token": self.tokens, "lemma": self.lemma, "POS": self.POS, "count": self.count, "WN_laxical_names": self.WN_laxical_names, "comment_id": self.comment_id,
    #             "vecs":self.vecs, "top_concept": self.top_concept, "key_concept_chain": self.key_concept_chain, "key_concepts": self.key_concepts}

    def get_lexical_name(self):
        self.WN_laxical_names = utils.get_lexical_file_name(self.lemma)

    def __str__(self):
        return json.dumps(self.json_info(), indent=4)

class Ngram(W):
    def __init__(self, token, lemma, root, POS, N, comment_id, lexical_name=False, concepts_config=None):
        super(Ngram, self).__init__(token, lemma, POS, comment_id)
        self.root = root
        self.N = N

        if lexical_name:
            self.get_lexical_name()

        if concepts_config!=None:
            self.get_concepts(concepts_config.num, concepts_config.layers, concepts_config.cache_path, concepts_config.probase)

    # def json_info(self):
        # return {"token": self.tokens, "lemma": self.lemma, "POS": self.POS, "root": self.root, "N": self.N, "WN_laxical_names": self.WN_laxical_names, "comment_id": self.comment_id,
        #         "count": self.count, "vecs":self.vecs, "top_concept": self.top_concept, "key_concept_chain": self.key_concept_chain, "key_concepts": self.key_concepts}

    # def we_vec(self, name, vecs, method="average"):
    #     for vec in vecs:
    #         if isinstance(vec, np.ndarray) == False:
    #             print("vec class error, vec must be numpy.ndarray")
    #             return
    #     final_vec = np.zeros(vecs[0].shpae)
    #     if method=="average":
    #         for vec in vecs:
    #             final_vec += vec
    #         final_vec = final_vec/len(vecs)
    #     self.vecs[name] = final_vec

    # def get_concepts(self, num, cache_path = "./MCG", probase = None):
    #     concept = utils.get_concept_prob(self.lemma, num=num, cache_path=cache_path, probase=probase)
    #     if len(concept)==0:
    #         concept = utils.get_concept_prob(self.root, num=num, cache_path=cache_path, probase=probase)
    #     self.top_concept = concept

    def get_lexical_name(self):
        self.WN_laxical_names = utils.get_lexical_file_name(self.root)
    
    def __str__(self):
        return json.dumps(self.json_info(), indent=4)

class Word_reload(Word):
    def __init__(self, json_dic):
        for k,v in json_dic.items():
            self.__dict__[k] = v

class Ngram_reload(Ngram):
    def __init__(self, json_dic):
        for k,v in json_dic.items():
            self.__dict__[k] = v

class Word_list:
    def __init__(self, words=None):
        if words==None:
            self.content = []
        else:
            self.content = words
    def append(self, word, deepcopy=False):
        if isinstance(word, W) == False:
            print("append failed, class error")
            return
        if word not in self.content:
            if deepcopy:
                self.content.append(copy.deepcopy(word))
            else:
                self.content.append(word)
        else:
            x = self.content.index(word)
            self.content[x].add_count(word.count)
            self.content[x].add_tokens(word.tokens)
            self.content[x].add_comment_id(word.comment_id)

    def json_info(self):
        return [i.json_info() for i in self.content]

    def to_list(self):
        return [i.lemma for i in self.content]

    def __add__(self, other):
        new_word_list = Word_list(self.content + other.content)
        return new_word_list

    def __repr__(self):
        return "Word_list(len=%d)"%len(self.content)

    def __str__(self):
        return json.dumps(self.json_info(), indent=4)

    def __len__(self):
        return len(self.content)

class Word_list_reload(Word_list):
    def __init__(self, json_dic):
        self.content = []
        for i in json_dic:
            if "N" in i:
                self.content.append(Ngram_reload(i))
            else:
                self.content.append(Word_reload(i))
