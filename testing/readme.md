# HOW TO RUN THE TEST

To perform tests on the Pira dataset, do as follows:

- 1 `python -m spacy download it_core_news_sm`
So that the AnalyzerEngine will be able to support the Italian language

- 2 'python preprocessing.py' 
To preprocess the file `pira_dataset.json` and print it onto the `new_dataset.json` file so that it can be in a suitable format for the recognition and anonymization

- 3 'python PIRA_Recognition.py' 
To get the results of the recognition and anonymization process

