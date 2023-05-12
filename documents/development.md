# Development instruction

1. Fork the repository to your own Github repository

2. Clone your repository

   ```bash
   git clone https://github.com/you_user_name/fwg
   ```

3. Create virtual environment(Optional)

   ```bash
   conda create -n env_name python=3.10 jupyter jupyterlab
   conda activate env_name
   ```

4. Install requirements

   ```bash
   pip install -r requirements.txt
   ```

5. Download NLTK wordnet and stopwords

   ```bash
   python -c "import nltk;nltk.download("wordnet");nltk.download("stopwords")"
   ```

6. Download develop folder (contain  recommended project structure, and probase model(Microsoft Concept Graph))

   After that, you can develop the code in repository, and create test scripts in FWG/test directory. Insert the following snippet to your test code.

   ```python
   import os
   import sys
   sys.path.append("../src")
   
   model_path = "develop_folder/model"
   data_path = "develop_folder/data"
   cache_path = "develop_folder/cache"
   ```

   An example test:

   ```python
   import os
   import sys
   sys.path.append("../src")
   
   model_path = "develop_folder/model"
   data_path = "develop_folder/data"
   cache_path = "develop_folder/cache"
   
   from FWG import Corpus
   from FWG import utils
   from FWG import Concepts
   from FWG import Word
   
   nlp = utils.init_spacy_nlp()
   
   probase = utils.init_probase(os.path.join(model_path, "probase_bi"), binary=True)
   probase_config = Concepts.Concept_conf(probase=probase, cache_path=os.path.join(cache_path, "MCG"))
   
   comments = ["I love apples, not the apple phone", "Green apple is a type of apple", "Apple is a kind of fuits, I like apple, I love apple", "Apple is a kind of fuits, I like apple, I love apple"]
   
   c = Corpus.Corpus(comments, nlp, lexical_name=True, concepts_config=probase_config)
   c.frequency_filter(path=os.path.join(cache_path, "test.json"), p_value=0.05)
   
   # ...
   ```

   
