from . import Comment
from . import Word
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

    def save_comments(self, path, bi=True):
        if bi:
            Kkit.store_result(path, self.comments)
        else:
            json_info = [i.json_info() for i in self.comments]
            str_json = json.dumps(json_info, indent=4)
            with open(path, "w") as f:
                f.write(str_json)

    def save_FDs(self, path, bi=True):
        if bi:
            Kkit.store_result(path, self.FD)
        else:
            json_info = self.FD.json_info()
            str_json = json.dumps(json_info, indent=4)
            with open(path, "w") as f:
                f.write(str_json)
    
    def concept_filter(self):
        pass
    
    def frequency_filter(self):
        pass

    def spell_filter(self):
        pass

class Corpus_reload(Corpus):
    def __init__(self, comments_path, FD_path):
        self.comments = Kkit.load_result(comments_path)
        self.FD = Kkit.load_result(FD_path)