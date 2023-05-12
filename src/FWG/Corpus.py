from . import Comment
from . import Word
from . import utils
from tqdm import tqdm
import Kkit
import json
import copy
import numpy as np
import scipy.stats as stats
import os
import warnings
from sklearn.decomposition import PCA
from prince import CA
import pandas as pd

class Corpus:
    def __init__(self, comments, nlp_model, POS_candidate=["NN", "JJ"], phrase=True, lexical_name=False, concepts_config=None, n_process=-1, batch_size=100):
        self.vec_index = {}
        self.ca = {}
        self.pca = {}
        self.comments = []
        Words = Word.Word_list()
        Ngram = Word.Word_list()

        docs = [i for i in nlp_model.pipe(comments, n_process=n_process, batch_size=batch_size)]
        for index, doc in enumerate(tqdm(docs)):
            new_comment = Comment.Comment(doc, index, POS_candidate, phrase, lexical_name, concepts_config)
            self.comments.append(new_comment)
            for i in new_comment.Words.content:
                Words.append(i, deepcopy=True)
            for i in new_comment.Ngram.content:
                Ngram.append(i, deepcopy=True)
        self.FD = Words + Ngram
    
    def static_key_concept(self, path=None):
    # static key cincept count in self.FD
        json_dic = {"empty_concepts": []}
        for concept in utils.key_concepts:
            temp = [i.json_info() for i in self.FD.content if concept in i.key_concepts]
            if len(temp)==0:
                json_dic["empty_concepts"].append(concept)
            else:
                temp = sorted(temp, key=lambda x: x["count"], reverse=True)
                json_dic[concept] = temp
        if path!=None:
            if path.endswith("json"):
                # with open(path, "w") as f:
                #     f.write(json.dumps(json_dic))
                Kkit.store(path, json.dumps(json_dic, indent=4), encoding="utf-8")
            else:
                Kkit.store(path, json_dic)
        return json_dic

    def archive(self, path="./cache", format="bi"):
        if format not in ["bi", "json"]:
            raise Exception("format can only be bi or json, don't support %s"%format)
        timestr = Kkit.time_string()
        self.save_comments(os.path.join(path, "archive-%s"%timestr, "comments.%s"%format))
        self.save_FDs(os.path.join(path, "archive-%s"%timestr, "FD.%s"%format))
        self.save_vec_index(os.path.join(path, "archive-%s"%timestr, "index.%s"%format))
        self.save_pca_ca_bi(os.path.join(path, "archive-%s"%timestr, "pca_ca_models.bi"))

    def save_pca_ca_bi(self, path):
        try:
            Kkit.store(path, {"pca":self.pca, "ca":self.ca})
        except:
            warnings.warn("saving pca, ca failed")
    
    def save_vec_index(self, path):
        if path.endswith(".json"):
            str_json = json.dumps(self.vec_index, indent=4)
            Kkit.store(path, str_json, encoding="utf-8")
        else:
            Kkit.store(path, self.vec_index)
    
    def save_comments(self, path):
        if path.endswith(".json"):
            json_info = [i.json_info() for i in self.comments]
            str_json = json.dumps(json_info, indent=4)
            # with open(path, "w") as f:
            #     f.write(str_json)
            Kkit.store(path, str_json, encoding="utf-8")
        else:
            Kkit.store(path, self.comments)

    def save_FDs(self, path):
        if path.endswith(".json"):
            json_info = self.FD.json_info()
            str_json = json.dumps(json_info, indent=4)
            # with open(path, "w") as f:
            #     f.write(str_json)
            Kkit.store(path, str_json, encoding="utf-8")
        else:
            Kkit.store(path, self.FD)

    def assess_FD(self, ground_truth):
        pass
    
    def concept_filter(self, path=None, replace=True):
        FD_after = Word.Word_list([word for word in self.FD.content if len(word.key_concepts)>0])
        if path!=None:
            filter_out = Word.Word_list([word for word in self.FD.content if len(word.key_concepts)==0])
            archive = {"before": self.FD.json_info(), "after": FD_after.json_info(), "filter_out":filter_out.json_info()}
            if path.endswith(".json"):
                str_json = json.dumps(archive, indent=4)
                # with open(path, "w") as f:
                #     f.write(str_json)
                Kkit.store(path, str_json, encoding="utf-8")
            else:
                Kkit.store(path, archive)
        if replace:
            self.FD = FD_after
            return self
        else:
            New_Corpus = copy.deepcopy(self)
            New_Corpus.FD = FD_after
            return New_Corpus
    
    def frequency_filter(self, p_value, path=None, replace=True):
        # filter out low frequency words: how to define low frequency words?
        # use normal distrubution in this version
        # null hypothesis: the frequency of a word is significantly lower than average
        filter_out = []
        for kc in utils.key_concepts:
            counts = [w.count for w in self.FD.content]
            words = [w for w in self.FD.content if kc in w.key_concepts]
            if len(words)>0 and len(counts)>0:
                mean = np.mean(counts)
                std = np.std(counts)
                z_scores = [(freq - mean) / std for freq in counts]
                p_values = [stats.norm.cdf(z) for z in z_scores]
                remove = [word for word, p in zip(words, p_values) if p < p_value]
                for i in remove:
                    if i in filter_out:
                        pass
                    else:
                        filter_out.append(i)
            else:
                pass
        if path!=None:
            filter_out = Word.Word_list(filter_out)
            FD_after = Word.Word_list([i for i in self.FD.content if i not in filter_out.content])
            archive = {"before": self.FD.json_info(), "after": FD_after.json_info(), "filter_out":filter_out.json_info()}
            if path.endswith(".json"):
                str_json = json.dumps(archive, indent=4)
                with open(path, "w") as f:
                    f.write(str_json)
            else:
                Kkit.store(path, archive)
        if replace:
            self.FD = FD_after
            return self
        else:
            New_Corpus = copy.deepcopy(self)
            New_Corpus.FD = FD_after
            return New_Corpus

    def spell_filter(self, dictionary, path=None, replace=True):
        FD_after = Word.Word_list([word for word in self.FD.content if dictionary.check(word.lemma)])
        if path!=None:
            filter_out = Word.Word_list([word for word in self.FD.content if dictionary.check(word.lemma)==False])
            archive = {"before": self.FD.json_info(), "after": FD_after.json_info(), "filter_out":filter_out.json_info()}
            if path.endswith(".json"):
                str_json = json.dumps(archive, indent=4)
                with open(path, "w") as f:
                    f.write(str_json)
            else:
                Kkit.store(path, archive)
        if replace:
            self.FD = FD_after
            return self
        else:
            New_Corpus = copy.deepcopy(self)
            New_Corpus.FD = FD_after
            return New_Corpus

    def gen_td_vec(self):
    # token-document frequency matrix
        for fd in self.FD.content:
            temp_vec = np.zeros(len(self.comments), dtype=np.uintc)
            for comment_id, count in fd.comment_id.items():
                temp_vec[comment_id] = count
            fd.we_vec("token-doc", temp_vec)
        return self

    def gen_PCA_vec(self, base_vec="token-doc", **pca_arg):
    # using PCA de-dimension td vec
        x = np.stack([i.vecs[base_vec] for i in self.FD.content])
        pca = PCA(**pca_arg)
        pca = pca.fit(x)
        res = pca.transform(x)
        self.pca[base_vec] = pca
        res = res.tolist()
        res = [np.array(i) for i in res]
        for (fd, vec) in zip(self.FD.content, res):
            fd.we_vec(base_vec+"-PCA", vec)
        return self

    def gen_CA_vec(self, base_vec="token-doc", **ca_arg):
    # # using CA de-dimension td vec
        x = np.stack([i.vecs[base_vec] for i in self.FD.content])
        x = pd.DataFrame(x)
        ca = CA(**ca_arg)
        ca = ca.fit(x)
        res = ca.row_coordinates(x).values
        self.ca[base_vec] = ca
        res = res.tolist()
        res = [np.array(i) for i in res]
        for (fd, vec) in zip(self.FD.content, res):
            fd.we_vec(base_vec+"-CA", vec)
        return self

    def gen_tc_vec(self):
    # token-concept probability matrix
        # count concepts
        concepts = set()
        for fd in self.FD.content:
            for i in fd.top_concept.keys():
                concepts.add(i)
        concepts = list(concepts)
        self.vec_index["concepts"] = concepts
        # concepts vector
        for fd in self.FD.content:
            temp_vec = np.zeros(len(concepts), dtype="float64")
            for k,v in fd.top_concept.items():
                temp_vec[concepts.index(k)] = v
            fd.we_vec("concept", temp_vec)
        return self

    def gen_GloVe_vec(self, Word2vec_model):
    # GloVe vector:
        for fd in self.fd.content:
            fd.we_vec("glove", Word2vec_model.vectorize(fd))

class Corpus_reload_bi(Corpus):
    def __init__(self, path):
        paths = ["comments.bi", "FD.bi", "index.bi", "pca_ca_models.bi"]
        paths = [os.path.join(path, i) for i in paths]
        print("load following archives:")
        Kkit.print_list(paths, 1, verbose=False)
        self.comments = Kkit.load(paths[0])
        self.FD = Kkit.load(paths[1])
        self.vec_index = Kkit.load(paths[2])
        bi = Kkit.load(paths[3])
        self.ca = bi["ca"]
        self.pca = bi["pca"]

class Corpus_reload_json(Corpus):
    def __init__(self, path):
        paths = ["comments.json", "FD.json", "index.json", "pca_ca_models.bi"]
        paths = [os.path.join(path, i) for i in paths]
        print("load following archives:")
        Kkit.print_list(paths, 1, verbose=False)
        self.comments = []
        comments = json.loads(Kkit.load(paths[0], encoding='utf-8'))
        for c in comments:
            comment = Comment.Comment_reload(c)
            self.comments.append(comment)
        self.FD = Word.Word_list_reload(json.loads(Kkit.load(paths[1], encoding="utf-8")))
        self.vec_index = json.loads(Kkit.load(paths[2], encoding="utf-8"))
        bi = Kkit.load(paths[3])
        self.ca = bi["ca"]
        self.pca = bi["pca"]