
from os import close
from numpy import negative, positive
import presidio_analyzer
from presidio_analyzer.entity_recognizer import EntityRecognizer
import presidio_anonymizer
from presidio_anonymizer.entities.engine.result.engine_result import EngineResult
from presidio_anonymizer.operators.geocoordinates import Geocoordinates
import spacy
from presidio_analyzer import AnalyzerEngine, RecognizerRegistry
import json
import unittest


nlp = spacy.load('en_core_web_lg')

from presidio_anonymizer import AnonymizerEngine
from presidio_anonymizer.entities.engine import RecognizerResult, OperatorConfig

# Initialize the engine with logger.




class TestSum(unittest.TestCase):

    def test(self):

        registry = RecognizerRegistry()
        registry.load_predefined_recognizers()
        f = open("dataset.json")
        data = json.load(f)
        f.close()

        # Set up analyzer with our updated recognizer registry
        analyzer = AnalyzerEngine(registry=registry)

        false_positives = 0
        false_negatives = 0

        for i in range(0,len(data)-1):

            text = data[i]['data']

            analyzer_results = analyzer.analyze(text, language="en")


            recognized = 0
            entities_recognized = []
            false = []

            for j in range(0,len(analyzer_results)-1):
                x = analyzer_results[j]
                if(not x.entity_type == 'LOCATION'):  #the entity being recognized is a location
                    continue;
                temp = [x.start,x.end,"Geolocation"]  #create an array of the same format as the one in the json format so that they can be compared
                entities_recognized.append(temp)
                if(temp in data[i]['label']):   #value correctly recognized
                    recognized = recognized + 1
                    entities_recognized.append(temp)
                else:
                    false_positives = false_positives + 1
                    false.append(text[x.start:x.end])  #register the false positives
                    #analyzer_results.remove(x)        #remove the false posivitives from the analyzer results tìsince they don't need to be anonymized
                

            n_entities_to_recognize = 0
            false_neg = []

            #count how many Geolocation entities were we supposed to recognize
            for j in range(0,len(data[i]['label'])-1):
             entity = data[i]['label'][j]
             if(entity[2] == "Geolocation"):
                    n_entities_to_recognize = n_entities_to_recognize + 1
                    if(not entity in entities_recognized):
                        start_index = int(entity[0])
                        end_index = int(entity[1])
                        false_neg.append(text[start_index:end_index])

            
            false_negatives = n_entities_to_recognize - false_positives - recognized


            print('Number of false positives:', false_negatives)
            if(not false_negatives== 0 ):
                print('False Positives:')
                for entity in false_neg:
                    print(entity)
                    
            print('Number of false positives :', false_positives )
            if(not false_negatives == 0 ):
                print('False positives:')
                for entity in false:
                    print(entity)

            anonymizer = AnonymizerEngine()
            
            anonymized_results = anonymizer.anonymize(
                    text,
                    analyzer_results,    

                    operators={
                        "LOCATION": OperatorConfig("geocoordinates",{ 
                        "function" : "calculate_coordinates",
                        "radius" : 3})},
                    )

            assert false_positives == 0 and false_negatives == 0, 'ERROR'
            

if __name__ == '__main__':
    unittest.main()

