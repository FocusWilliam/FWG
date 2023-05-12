# Flavour Wheel Generator

processing......

## Environment setup

1. [For development](documents/development.md)

2. For runtime:

```bash
pip install git+https://github.com/erwinliyh/fwg@main

python -c "import nltk;nltk.download("wordnet");nltk.download("stopwords")"
```

## start to use

```python
from FWG import utils
from FWG import Concepts
from FWG import Corpus
import Kkit

nlp = utils.init_spacy_nlp()
probase = utils.init_probase("path to probase")

probase_config = Concepts.Concept_conf(probase=probase)

comments = ["I love apples, not the apple phone", "Green apple is a type of apple", "Apple is a kind of fuits, I like apple, I love apple"]

c = Corpus.Corpus(comments, nlp, lexical_name=True, concepts_config=probase_config)

print(c.FD)

print(c.comments)
```

## todo

### Functions

- [ ] Finish Corpus.py
  - [ ] assess_FD()
  - [x] frequency_filter()
  - [x] POS filter
  - [x] concept filter
  - [x] static_key_concept()
  - [x] gen_td_vec()
  - [x] gen_PCA_vec()
  - [x] gen_CA_vec()
  - [x] gen_tc_vec()
  - [x] gen_GloVe_vec()
- [x] Finish display.py: for more good visualisation of FD extraction (move to utlils.py)

### test

- [x] test reload class
