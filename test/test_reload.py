import sys
sys.path.append("/home/kylis/Desktop/git/FWG/src")

from FWG import Corpus

model_path = "/home/kylis/Desktop/FYP/model"
data_path = "/home/kylis/Desktop/FYP/data"
cache_path = "/home/kylis/Desktop/FYP/cache"

a = Corpus.Corpus_reload_bi(cache_path)

print(a.FD)
print(a.comments)
print(a.vec_index)