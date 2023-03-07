from . import Comment
from . import Word
from . import utils
from tqdm import tqdm
import Kkit
import json
import copy
import numpy as np
import os

class Corpus:
    def __init__(self, comments, nlp_model, POS_candidate=["NN", "JJ", "phrase"], lexical_name=False, concepts_config=None):
        self.vec_index = {}
        self.comments = []
        Words = Word.Word_list()
        Ngram = Word.Word_list()
        for index, comm in enumerate(tqdm(comments)):
            new_comment = Comment.Comment(comm, nlp_model, index, POS_candidate, lexical_name, concepts_config)
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

    def archive(self, path="./cache", format="json"):
        timestr = Kkit.time_string()
        self.save_comments(os.path.join(path, "archive_comments_%s.%s"%(timestr ,format)))
        self.save_FDs(os.path.join(path, "archive_FD_%s.%s"%(timestr ,format)))
        self.save_vec_index(os.path.join(path, "archive_key_%s.%s"%(timestr ,format)))
    
    def save_vec_index(self, path):
        if path.endswith(".json"):
            str_json = json.dumps(self.vec_index, indent=4)
            Kkit.store(path, str_json, encoding="utf-8")
        else:
            Kkit.store(path, self.comments)
    
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
    
    def frequency_filter(self, p_value, path=None):
        # filter out low frequency words: how to define low frequency words?
        # use normal distrubution?
        for kc in utils.key_concepts:
            pass

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

    def gen_PCA_vec(self):
    # using PCA de-dimension td vec
        pass

    def gen_CA_vec(self):
    # # using CA de-dimension td vec
        pass

    def gen_tc_vec(self):
    # token-concept probability matrix
        # count concepts
        for fd in self.FD.content:
            pass
        # concepts vector
        for fd in self.FD.content:
            pass

    def gen_GloVe_vec(self):
    # GloVe vector:
        pass

    def custom_vec(self, token_vec_map):
    # customized vector
        pass

class Corpus_reload_bi(Corpus):
    def __init__(self, path):
        paths = utils.scan_archive(path)
        paths = [os.path.join(path, i) for i in paths]
        self.comments = Kkit.load(paths[0])
        self.FD = Kkit.load(paths[1])
        self.vec_index = Kkit.load(paths[2])

class Corpus_reload_json(Corpus):
    def __init__(self, path):
        paths = utils.scan_archive(path)
        paths = [os.path.join(path, i) for i in paths]
        self.comments = []
        comments = json.loads(Kkit.load(paths[0], encoding='utf-8'))
        for c in comments:
            comment = Comment.Comment_reload(c)
            self.comments.append(comment)
        self.FD = Word.Word_list_reload(json.loads(Kkit.load(paths[1], encoding="utf-8")))
        self.vec_index = json.loads(Kkit.load(paths[2], encoding="utf-8"))