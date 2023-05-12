from . import utils
import Kkit
from . import Word
import json

class Comment:
    def __init__(self, doc, comment_id, POS_candidate=["NN", "JJ"], phrase=True, lexical_name=False, concepts_config=None):
        # self.doc = doc
        self.comment_id = comment_id
        self.Words = Word.Word_list()
        self.Ngram = Word.Word_list()

        # doc = nlp_model(self.string)
        if phrase:
            # all noun phrases
            noun_chunks = doc.noun_chunks
            # if len(noun_chunks)!=0:
            noun_chunks = [chunk for chunk in noun_chunks if (chunk.end-chunk.start==2)] # only keep noun phrase with length 2
            noun_chunks = [chunk for chunk in noun_chunks if Kkit.list_in_list(chunk.lemma_.split(" "), utils.stops, X="any")==False and utils.is_only_az_AZ(chunk.lemma_)] # remove noun phrase with stop words
        # all tokens
        tokens = [word for word in doc if (word.tag_ in POS_candidate) and (word.lemma_ not in utils.stops) and utils.is_only_az_AZ(word.lemma_)]
        # delete overlap between tokens and phrases
        for chunk in noun_chunks:
            tokens = [word for word in tokens if (word.i<chunk.start or word.i>=chunk.end)]
        
        all_tokens = [word.text_with_ws for word in doc]
        star_index = []
        for chunk in noun_chunks:
            star_index.append([chunk.start, chunk.end])
            new_Ngram = Word.Ngram(chunk.text.lower(), chunk.lemma_, chunk.root.lower_, chunk.label_, 2, comment_id, lexical_name, concepts_config)
            self.Ngram.append(new_Ngram, deepcopy=True)

        for token in tokens:
            star_index.append(token.i)
            new_Word = Word.Word(token.lower_, token.lemma_, token.tag_, comment_id, lexical_name, concepts_config)
            self.Words.append(new_Word, deepcopy=True)
        for i in star_index:
            if isinstance(i, int):
                all_tokens[i] = ("*"+utils.add_star(all_tokens[i]))
            elif isinstance(i, list):
                all_tokens[i[0]] = ("*"+all_tokens[i[0]])
                all_tokens[i[1]-1] = utils.add_star(all_tokens[i[1]-1])
        self.string = "".join(all_tokens)

    def json_info(self):
        return {"string": self.string, "comment_id": self.comment_id, "Words": self.Words.json_info(), "Ngram": self.Ngram.json_info()}

    def __str__(self):
        return json.dumps(self.json_info(), indent=4)

    def __repr__(self):
        return "FWG.Comment(id=%d, len(Ngram)=%d, len(Word)=%d)"%(self.comment_id, len(self.Ngram), len(self.Words))

class Comment_reload(Comment):
    def __init__(self, json_dic):
        self.string = json_dic["string"]
        self.comment_id = json_dic["comment_id"]
        self.Words = Word.Word_list_reload(json_dic["Words"])
        self.Ngram = Word.Word_list_reload(json_dic["Ngram"])