# HOW TO RUN THE TEST

The testing folder purpose is to check how many entities were correctly recognized by the Analyzer module of Presidio. 
Each entity is annotated with a tag describing its nature (e.g. GEOLOCATION, PERSON_NAME)

This happens in two steps:

### PREPROCESSING
It takes the `pira_dataset.jsonl` file and makes sure that the data and label field of each document is fixed for a better ananlysis and recognition process.	<br>
All special characters such as “;” and “\n” can be simply removed with a regular expression, while fixing of the labels requires the following steps: <br>

***IF*** the label tag is “No_Tag” ***THEN***	:	                      
Discard the whole document since it does not contain any relevant information.

***IF*** one or more fields in the header are labeled as “Text_Column”  ***THEN*** :   <br>
Remove these annotations from the label array.   

***ELSE***  :                                                                                                                        
A header field is annotated with a label different from the above and one annotation per line must be added.                                                                In order to do so, we need to find for each entity in the line its starting and ending position in the document and add it to the label array.
Once the preprocessing phase will be completed, the newly processed JSON objects will be saved into a new file that will be used later for the analysis and anonymization process.

### RECOGNITION


To check the number of entities correctly recognized: <br>	

•	Create a list of the entities that are supposed to be recognized; each entity can be easily retrieved since each object in the labels array contains the initial and final character of a specific entity to recognize <br>	

•	Create a list of entities the Analyzer recognized. Again, the Analyzer does not return the value of the entity but its position in the text. <br>	

•	Check for each element in the result list if it’s contained in the list of entities to recognize. If the answer is yes, then it is possible to increase the true positive counter. <br>	


### INSTALLATION

    $ git clone https://github.com/btessa99/microsoft_presidio.git
    
    $ pip3 install --upgrade pip
    $ pip3 install presidio-anonymizer
    $ pip3 install presidio-analyzer
    $ python3 -m spacy download it_core_news_sm
  

From the microsoft_presidio/tetsing directory:
```console
python Pira-Recognizer.py
```
To start see how many entities were recognized.


### DEPLOYMENT

From the microsoft_presidio/tetsing directory:

Build the docker image
```console
docker build -t test-pira .
```
To download all the necessary libraries and then to run the test

```console
python Pira-Recognizer.py
```





