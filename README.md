# Flavour Wheel Generator

processing......

## Environment setup

Dev:
```bash
# fork the repo to your github

git clone https://github.com/you_user_name/fwg

conda create -n fw python=3.10 jupyter jupyterlab #optional

conda activate fw                                 #optional

pip install -r requirements.txt

pip install -e git+https://github.com/explosion/spacy-models/releases/download/en_core_web_trf-3.5.0/en_core_web_trf-3.5.0-py3-none-any.whl

pip install git+https://github.com/erwinliyh/kylis_kit@main

python -c "import nltk;nltk.download("wordnet");nltk.download("stopwords")"

# then develop code from FWG/src and debug using code in FWG/test
```

Runtime:
```bash
pip install -e git+https://github.com/explosion/spacy-models/releases/download/en_core_web_trf-3.5.0/en_core_web_trf-3.5.0-py3-none-any.whl

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