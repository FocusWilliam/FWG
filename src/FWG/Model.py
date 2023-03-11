import os
import gensim
class Word2vec_model:
    def __init__(self, model_name=None):
        self.model_name = model_name
        _DEFAULT_BASE_DIR = os.path.expanduser('~/gensim-data')
        self.dir = os.environ.get('GENSIM_DATA_DIR', _DEFAULT_BASE_DIR)
        self.error = []
        self.model == None
    def list(self):
        candidate_model = list(gensim.downloader.info()['models'].keys())
        downloaded_model = os.listdir(self.dir)
        info = "models in %s:\n"%self.dir
        for i in candidate_model:
            if i.startswith("_") == False:
                if i in downloaded_model:
                    info += (i+"*"+"\n")
                elif i==self.model_name:
                    info += (i+"**"+"\n")
                else:
                    info += (i+"\n")
        print(info.strip("\n"))
    def set_model(self, model_name):
        self.model_name = model_name
        return self
    def load(self):
        if self.model_name == None:
            raise Exception("Please set model tobe loaded, 'model.set_model(\"glove-twitter-25\")")
        self.model=  gensim.downloader.load(self.model_name)
        return self
    def vectorize(self, W):
        if self.model == None:
            raise Exception("Please load a model")
        vec = None
        try:
            vec = self.model.get_vector(W.lemma)
        except KeyError:
            try:
                vec = self.model.get_vector(W.root)
            except AttributeError:
                self.error.append(W)
        return vec