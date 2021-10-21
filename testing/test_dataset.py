import presidio_analyzer
from presidio_analyzer.analyzer_engine import AnalyzerEngine
from presidio_analyzer.nlp_engine.spacy_nlp_engine import SpacyNlpEngine
from presidio_analyzer.nlp_engine.stanza_nlp_engine import StanzaNlpEngine
from presidio_analyzer.recognizer_result import RecognizerResult
from presidio_anonymizer.anonymizer_engine import AnonymizerEngine
from presidio_anonymizer.entities.engine.operator_config import OperatorConfig
import stanza
import json


def convert(tag):
    """convert types from the Stanza ones into the ones in the dataset """
    
    if(tag == "GPE"):
        return "Geolocation"
    elif(tag == "PERSON"):
        return "Person_Name"
    else:
        return tag  #other types don't need to be converted

def isState(geolocation,states):

    """check whether a geolocation is a country or not"""

    for state in states:
        state_to_check = state[0:len(state)-1] #discard \n character at the end of the string
        if(geolocation.__contains__(state_to_check)):
            return True

    return False


#recognition with Stanza
analyzer = stanza.Pipeline('en')

#anonimyzation with Spacy
anonimyzer = AnonymizerEngine()

json_file  = open("new_dataset.json","r")
data = json.load(json_file)
json_file.close()

f_states = open("states.txt")
states = f_states.readlines()
f_states.close()

count = 0 #number of entities actually recognized
total = 0 #number of entities to recognize

for i in range(0,len(data)):  

        doc = analyzer(data[i]['data'])
        labels = data[i]['label']
        total = len(labels) + total

        total_entities = []
 
        for ent in doc.entities:

            if(isState(ent.text,states)): #discard countries
                continue

            entity = [ent.start_char,ent.end_char,convert(ent.type)] #create same label format as in the one in the json file

            #convert so that it can be given as input to the anonimyzer
            r = RecognizerResult(entity_type = convert(ent.type),start = ent.start_char, end = ent.end_char, score= 0.7) 
            total_entities.append(r) 

            if(entity in labels): #check if the entity was correctly recognized
                count = count + 1

        #anonimyze the data
        anonimyzer_result = anonimyzer.anonymize(data[i]['data'] , total_entities, operators={"Geolocation": OperatorConfig("geocoordinates", {"function":"calculate_coordinates","radius":5})})
        print(anonimyzer_result.text)

print("NUMBER OF ENTITIES RECOGNIZED: ",count,"NUMBER OF ENTITIES TO RECOGNIZE: ",total,"FALSE POSITIVES: ",total - count)


