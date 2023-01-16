from . import utils
import Kkit
from . import Word
import json

class Comment:
    def __init__(self, string, nlp_model, POS_candidate=["NN", "JJ", "phrase"], lexical_name=False, concepts_config=None):
        self.string = string
        self.Words = Word.Word_list()
        self.Ngram = Word.Word_list()

        try:
            doc = nlp_model(self.string)
            if "phrase" in POS_candidate:
                # all noun phrases
                noun_chunks = doc.noun_chunks
                # if len(noun_chunks)!=0:
                noun_chunks = [chunk for chunk in noun_chunks if (chunk.end-chunk.start==2)] # only keep noun phrase with length 2
                noun_chunks = [chunk for chunk in noun_chunks if Kkit.list_in_list(chunk.lemma_.split(" "), utils.stops, X="any")==False] # remove noun phrase with stop words
            # all tokens
            tokens = [word for word in doc if (word.tag_ in POS_candidate) and (word.lemma_ not in utils.stops)]
            # delete overlap between tokens and phrases
            for chunk in noun_chunks:
                tokens = [word for word in tokens if (word.i<chunk.start or word.i>=chunk.end)]
            
            all_tokens = [word.text_with_ws for word in doc]
            star_index = []
            for chunk in noun_chunks:
                star_index.append([chunk.start, chunk.end])
                new_Ngram = Word.Ngram(chunk.text.lower(), chunk.lemma_, chunk.root.lower_, chunk.label_, 2, lexical_name, concepts_config)
                self.Ngram.append(new_Ngram, deepcopy=True)

            for token in tokens:
                star_index.append(token.i)
                new_Word = Word.Word(token.lower_, token.lemma_, token.tag_, lexical_name, concepts_config)
                self.Words.append(new_Word, deepcopy=True)
            for i in star_index:
                if isinstance(i, int):
                    all_tokens[i] = ("*"+utils.add_star(all_tokens[i]))
                elif isinstance(i, list):
                    all_tokens[i[0]] = ("*"+all_tokens[i[0]])
                    all_tokens[i[1]-1] = utils.add_star(all_tokens[i[1]-1])
            self.string = "".join(all_tokens)
            
        except Exception as e:
            print("")
            print(self.string)
            print(e)

    def json_info(self):
        return {"comment_text": self.string, "words": self.Words.json_info(), "Ngram": self.Ngram.json_info()}

    def __str__(self):
        return json.dumps(self.json_info(), indent=4) 