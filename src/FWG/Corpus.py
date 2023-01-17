from . import Comment
from . import Word
from . import utils
from tqdm import tqdm
import Kkit
import json

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
    
    def static_key_concept(self):
        pass

    def save_comments(self, path):
        if path.endswith(".json"):
            json_info = [i.json_info() for i in self.comments]
            str_json = json.dumps(json_info, indent=4)
            with open(path, "w") as f:
                f.write(str_json)
        else:
            Kkit.store_result(path, self.comments)

    def save_FDs(self, path):
        if path.endswith(".json"):
            json_info = self.FD.json_info()
            str_json = json.dumps(json_info, indent=4)
            with open(path, "w") as f:
                f.write(str_json)
        else:
            Kkit.store_result(path, self.FD)

    def assement_FD(self, ground_truth):
        pass
    
    def concept_filter(self, path=None):
        FD_after = Word.Word_list([word for word in self.FD.content if len(word.key_concepts)>0])
        if path!=None:
            filter_out = Word.Word_list([word for word in self.FD.content if len(word.key_concepts)==0])
            archive = {"before_concept_filter": self.FD.json_info(), "after_concept_filter": FD_after.json_info(), "filter_out":filter_out.json_info()}
            if path.endswith(".json"):
                str_json = json.dumps(archive, indent=4)
                with open(path, "w") as f:
                    f.write(str_json)
            else:
                Kkit.store_result(path, archive)
        self.FD = FD_after
    
    def frequency_filter(self, path=None):
        # filter out low frequency words: how to define low frequency words?
        for kc in utils.key_concepts:
            pass

    def spell_filter(self, dictionary, path=None):
        FD_after = Word.Word_list([word for word in self.FD.content if dictionary.check(word.lemma)])
        if path!=None:
            filter_out = Word.Word_list([word for word in self.FD.content if dictionary.check(word.lemma)==False])
            archive = {"before_spell_filter": self.FD.json_info(), "after_spell_filter": FD_after.json_info(), "filter_out":filter_out.json_info()}
            if path.endswith(".json"):
                str_json = json.dumps(archive, indent=4)
                with open(path, "w") as f:
                    f.write(str_json)
            else:
                Kkit.store_result(path, archive)
        self.FD = FD_after

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
        self.comments = Kkit.load_result(comments_path)
        self.FD = Kkit.load_result(FD_path)