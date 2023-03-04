import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="FWG",
    version="0.0.1",
    author="Yuanhao Li",
    author_email="1779599839@qq.com",
    description="Flavour Wheel Generator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ErwinLiYH/FWG",
    project_urls={
        "Bug Tracker": "https://github.com/ErwinLiYH/FWG/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    # packages=setuptools.find_packages(where="src"),
    # install_requires=[
    #     'numpy',
    #     'matplotlib',
    #     'nltk',
    #     'spacy',
    #     'Kkit @ git+https://github.com/erwinliyh/kylis_kit@main',
    #     'pyenchant',
    #     'tqdm'
    # ],
    package_data={"": ['src/data/*']},
    python_requires=">=3.6",
)
