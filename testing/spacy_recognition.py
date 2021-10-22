from numpy import result_type
import presidio_analyzer
from presidio_analyzer import analyzer_engine
from presidio_analyzer.analyzer_engine import AnalyzerEngine
from presidio_analyzer.nlp_engine.spacy_nlp_engine import SpacyNlpEngine
from presidio_analyzer.nlp_engine.stanza_nlp_engine import StanzaNlpEngine
from presidio_analyzer.recognizer_result import RecognizerResult
import presidio_anonymizer
from presidio_anonymizer import AnonymizerEngine
from presidio_anonymizer.entities.engine import operator_config
import stanza
import json

def convert(tag):
    
    if(tag == "LOCATION"):
        return "Geolocation"
    elif(tag == "PERSON"):
        return "Person_Name"
    else:
        return tag

def isState(geolocation,states):


    for state in states:
        state_to_check = state[0:len(state)-1]
        if(geolocation.__contains__(state_to_check)):
            return True

    return False



analyzer = AnalyzerEngine()
anonimyzer = AnonymizerEngine()

json_file  = open("new_dataset.json","r")
data = json.load(json_file)
json_file.close()

f_states = open("states.txt")
states = f_states.readlines()
f_states.close()

count = 0
total = 0
total_entities = []



for i in range(0,len(data)):  

    labels = data[i]['label']
    text = data[i]['data']
    total = len(labels) + total

    analyzer_result = analyzer.analyze(text = text, language= "en")


    for result in analyzer_result:

        if(isState(text[result.start:result.end],states)): #discard countries
            analyzer_result.remove(result)

        entity = [result.start,result.end,convert(result.entity_type)] #create same label format as in the one in the json file
        if(entity in labels): #check if the entity was correctly recognized
            count = count + 1

    

    anonimyzer_result = anonimyzer.anonymize(text , analyzer_result, operators= {"Location": operator_config.OperatorConfig("calcolate_coordinates", {"radius":5})})

    
    

print("NUMBER OF ENTITIES RECOGNIZED: ",count,"NUMBER OF ENTITIES TO RECOGNIZE: ",total,"FALSE NEGATIVES: ",total - count)

    


