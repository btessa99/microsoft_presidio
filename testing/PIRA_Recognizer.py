#!/usr/bin/env python
# coding: utf-8

# In[1]:


import json
from presidio_anonymizer.anonymizer_engine import AnonymizerEngine
from presidio_anonymizer.entities.engine.operator_config import OperatorConfig 
from tqdm import tqdm

json_file  = open("/Users/bened/AppData/Local/Programs/Python/Python39/new_dataset.json", 'rt')
data = json.load(json_file)
json_file.close()



# In[72]:


configuration = {
    "nlp_engine_name": "spacy",
    "models": [{"lang_code": "it", "model_name": "it_core_news_sm"},
                {"lang_code": "en", "model_name": "en_core_web_lg"}],
}

from presidio_analyzer import AnalyzerEngine, RecognizerRegistry
from presidio_analyzer.nlp_engine import NlpEngineProvider

provider = NlpEngineProvider(nlp_configuration=configuration)
nlp_engine_with_italian = provider.create_engine()

analyzer = AnalyzerEngine(
    nlp_engine=nlp_engine_with_italian,
    supported_languages=["en", "it"]
)

anonimyzer = AnonymizerEngine()


# In[73]:


def convert(tag):

    if(tag == "LOCATION"):
        return "GPE"
    elif(tag == "PERSON"):
        return "Person_Name"
    else:
        return tag



num_labels = 0
tp = 0
unique_entities = set()
unique_results = set()

for item in tqdm(data):
    labels = item['label']
    text = item['data']
#    num_labels += len(labels)
    
    for l in labels:
        ent = text[l[0]:l[1]]
        if len(ent) > 0:
            if not ent.isnumeric():
                unique_entities.add(ent)
                num_labels += 1
        
    results = analyzer.analyze(text = text, language= "it")
    
    for r in results:
        is_in_unique = 0
        presidio_ent = text[r.start:r.end]
        unique_results.add(presidio_ent)
        for l in unique_entities:
            if l in presidio_ent:
                tp += 1
                break



    anonimyzer_results = anonimyzer.anonymize(

                                        text,
                                        results,
                                        operators={"LOCATION": OperatorConfig("geocoordinates",{ 
                                            "function" : "standard_gaussian",
                                            "variance" : 0.2}        
                                    )})
    print("**************")
    print(anonimyzer_results.text)

print("RECOGNIZED: ", tp, "ENTITIES OUT OF: ", num_labels)






