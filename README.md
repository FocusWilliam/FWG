# Flavour Wheel Generator

processing......

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

  - [ ] frequency_filter()

  - [ ] static_key_concept()

  - [ ] gen_td_vec()

  - [ ] gen_PCA_vec()

  - [ ] gen_CA_vec()

  - [ ] gen_tc_vec()

  - [ ] gen_GloVe_vec()

  - [ ] custom_vec()

- [ ] Finish display.py: for more good visualisation of FD extraction

Finished:

- POS filter
- concept filter

### test

- [ ] test reload class