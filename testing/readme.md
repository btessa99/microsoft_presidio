# HOW TO RUN THE TEST

To perform tests on the Pira dataset, do as follows:

- 1 download the PIRA dataset `pira_dataset.json` at [this link] (https://github.com/tonellotto/pira-project/tree/main/deliverable2)


- 2 ` $python -m spacy download it_core_news_sm`

So that the AnalyzerEngine will be able to support the Italian language


- 3 ` $python preprocessing.py`

To preprocess the PIRA dataset and print it onto the `new_dataset.json` file so that it can be in a suitable format for the recognition and anonymization


- 4 ` $python PIRA_Recognition.py`

To get the results of the recognition and anonymization process

