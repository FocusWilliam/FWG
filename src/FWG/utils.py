from pkg_resources import resource_filename
import os
import enchant
import requests
import Kkit
import json
from nltk.corpus import wordnet as wn
from nltk.corpus import stopwords
import spacy
import logging
from . import Probase
from . import Concepts
import math
from matplotlib import pyplot as plt
import re

stops = stopwords.words('english')

default_concepts_config = {"num": 20, "cache_path": "./cache/MCG", "probase": None}

key_concepts = ["plant", "food", "crop", "oil", "flavor", "flavours", "taste", "food quality", "sensory property", "organ", "acid", "additive", "ingredient", "scent", "drink", "beverage", "phenolic compound", "aromatic compound"]

def log(log_file, messege):
    logging.basicConfig(filename=log_file, format="%(message)s", level=logging.INFO)
    logging.INFO(messege)

def init_enchant_Dict(dic="en", extra_legal_voca=True):
    # initialize enchant spell dictionary
    # parameter:
    # dic: enchant Dcit language such as en, en_US, etc.
    if extra_legal_voca:
        voca_path = os.path.join(resource_filename(__name__, "data"), "legal_voca.txt")
        enchant_dic = enchant.DictWithPWL(dic, voca_path)
    else:
        enchant_dic = enchant.Dict(dic)
    return enchant_dic

def init_probase(path, binary=False):
    if binary:
        probase = Kkit.load(path)
    else:
        probase = Probase.ProbaseConcept(path)
    return probase

def init_spacy_nlp(model="en_core_web_trf"):
    nlp = spacy.load(model)
    # if phrase:
    #     nlp.add_pipe("textrank")
    return nlp

def get_lexical_file_name(single_token, pos=wn.NOUN):
    lexname_list = [j.lexname() for j in wn.synsets(single_token,pos=pos)]
    return lexname_list

def get_concept_prob(word, num, cache_path = "./cache/MCG", probase = None) -> dict:
    cache_list = []
    try:
        cache_list = os.listdir(cache_path)
    except:
        os.makedirs(cache_path)
    if "%s_%d"%(word,num) in cache_list:
        res = Kkit.load(os.path.join(cache_path, "%s_%d"%(word,num)))
        return res
    else:
        if probase == None:
            link = requests.get("https://concept.research.microsoft.com/api/Concept/ScoreByProb?instance=%s&topK=%d"%(word, num), verify=False)
            if link.status_code == 200:
                res = json.loads(link.text)
                Kkit.store(os.path.join(cache_path,"%s_%d"%(word,num)),res)
                return res
            else:
                raise Exception("code: %d"%link.status_code)
        else:
            res = {}
            concept_list = probase.conceptualize(word, score_method="likelihood")[:num]
            total = 0
            for i in concept_list:
                total+=i[1]
            for i in concept_list:
                res[i[0]] = i[1]/total
            Kkit.store(os.path.join(cache_path,"%s_%d"%(word,num)),res)
            return res

def build_key_concept_chain(word, layers, cache_path = "./cache/MCG", probase = None):
    paths = []
    paths_new = []
    root = Concepts.Node(word, 1)
    Concepts.build_concept_tree(root, layers, 0, cache_path, probase)
    Concepts.deep_search_key_concept(root, [], paths)
    for path in paths:
        temp = []
        for i in path:
            temp.append(i)
            if i in key_concepts:
                break
        if temp not in paths_new:
            paths_new.append(temp)
    return paths_new

def coverage(test_list, sdandart_DF):
    pass

def check(token, A_list):
    # example: drink in ["alcohol drink", "rice"]
    x = [i.split(" ") for i in A_list]
    y = []
    for i in x:
        y.append(i[-1])
        try:
            y.append(" ".join(i[-2:]))
        except:
            pass
        try:
            y.append(" ".join(i[-3:]))
        except:
            pass
    if token in y:
        return True
    else:
        return False

def add_star(string):
    if string.endswith(" "):
        return string.rstrip(" ")+"*"+" "
    else:
        return string+"*"

def visual_key_concept_statistics(json_dic, n_col_limit=3):
    num = len(json_dic.keys()) - 1
    if num<=n_col_limit:
        row = 1
        col = num
    else:
        row = math.ceil(num/n_col_limit)
        col = n_col_limit
    for i, (k, v) in enumerate(json_dic.items()):
        if k!="empty_concepts":
            x = [i["lemma"] for i in v]
            y = [i["count"] for i in v]
            plt.subplot(row, col, i)
            plt.bar(x, y)
            plt.title(k)

def scan_archive(path, format="json", time_string=None):
    files = os.listdir(path)
    files = [i.split("_") for i in files if re.fullmatch(r"archive_(comments|FD|key)_\d+\.[a-zA-Z]+", i)]
    groups = {}
    for i in files:
        if i[1] in groups:
            groups[i[1]].append(i[0])
        else:
            groups[i[1]] = [i[0]]
    if len(groups)==1:
        k, v = groups.items()
        if len(v) == 3 and "archive_comments" in v and "archive_FD" in v and "archive_key" in v:
            return "_".join("archive_comments",k), "_".join("archive_FD",k), "_".join("archive_key",k)
        else:
            raise Exception("Wrong archive")
    else:
        if time_string==None:
            raise Exception("multiple archives in same folder, time_string can't be empty")
        else:
            for k,v in groups.items():
                if k.startswith(time_string):
                    if len(v) == 3 and "archive_comments" in v and "archive_FD" in v and "archive_key" in v:
                        return "_".join("archive_comments",k), "_".join("archive_FD",k), "_".join("archive_key",k)
                    else:
                        raise Exception("Wrong archive")
            raise Exception("Can't find archive at %s")%time_string