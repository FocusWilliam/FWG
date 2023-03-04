from . import Comment
from . import Word
from . import utils
from tqdm import tqdm
import Kkit
import json
import copy

class Corpus:
    def __init__(self, comments, nlp_model, POS_candidate=["NN", "JJ", "phrase"], lexical_name=False, concepts_config=None):
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

    def archive(self, FD_path="./cache/comments.json", comments_path="./cache/FD.json"):
        self.save_comments(comments_path)
        self.save_FDs(FD_path)
    
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
    
    def frequency_filter(self, path=None):
        # filter out low frequency words: how to define low frequency words?
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
        pass

    def gen_PCA_vec(self):
    # using PCA de-dimension td vec
        pass

    def gen_CA_vec(self):
    # # using CA de-dimension td vec
        pass

    def gen_tc_vec(self):
    # token-concept probability matrix
        pass

    def gen_GloVe_vec(self):
    # GloVe vector:
        pass

    def custom_vec(self, token_vec_map):
    # customized vector
        pass

class Corpus_reload_bi(Corpus):
    def __init__(self, comments_path, FD_path):
        self.comments = Kkit.load(comments_path)
        self.FD = Kkit.load(FD_path)

class Corpus_reload_json(Corpus):
    def __init__(self, comments_path, FD_path):
        # with open(comments_path, "r") as f:
        #     c = json.loads(f.read(comments_path))
        self.comments = []
        comments = json.loads(Kkit.load(comments_path, encoding='utf-8'))
        for c in comments:
            comment = Comment.Comment_reload(c)
            self.comments.append(comment)
        with open(FD_path, "r") as f:
            f = json.loads(f.read())
            self.FD = Word.Word_list_reload(f)