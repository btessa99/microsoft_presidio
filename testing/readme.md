# ACCURACY TEST

This folder contains files which are useful for testing the accuracy of the recognition of entities and their anonimyzation.
It is made of 5 files:

- #### states.txt
Contains a list of state that shall not be recognized by the Analyzer.

- #### dataset.json
The initial dataset contatining data to test

- #### new_dataset.json
The final dataset used for the testing which contains the result of a previous preprocessing of the initial dataset.

This file is initally empty.

- #### preprocessing.py
Preprocesses the inital dataset by removing files labeled as NO_TAGS, and adding labels where needed.

Afterwards it fills the new_dataset.json file

- #### test_dataset.py
Analyzes the new dataset contained in new_dataset.json and counts the entities correctly recognized.

It also anonimyzes data as well and prints the result of such anonimyzation.


In order for the test to work correctly, it's crucial to run `preprocessing.py` before `test_dataset.py` otherwise the last will retrieve data from an empty file

