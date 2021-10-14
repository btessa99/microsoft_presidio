
from os import close
from re import split
from numpy import negative, positive
from numpy.lib.function_base import append
import presidio_analyzer
from presidio_analyzer import nlp_engine
from presidio_analyzer.entity_recognizer import EntityRecognizer
import presidio_anonymizer
from presidio_anonymizer.entities.engine.result.engine_result import EngineResult
from presidio_anonymizer.operators.geocoordinates import Geocoordinates
import spacy
from presidio_analyzer import AnalyzerEngine, RecognizerRegistry
import json
import unittest
import stanza

stanza.download('en') # download English model

nlp = spacy.load('en_core_web_lg')

from presidio_anonymizer import AnonymizerEngine
from presidio_anonymizer.entities.engine import RecognizerResult, OperatorConfig

# Initialize the engine with logger.

nlp = stanza.Pipeline('en')

def sortTag(obj):
    return obj[2]

class TestSum(unittest.TestCase):

    def test(self):

        f = open("prova.json")
        data = json.load(f)
        f.close()

        for i in range (0,len(data)):

            text = data[i]['data']

            #sort by tag in reversed lexicographical order
            data[i]['label'].sort(key = sortTag ,reverse = True)

            tag = data[i]['label'][0][2]
            print(tag)

            splitted_text = text.split(";")

            #print(splitted_text)

            if(tag == "No_Tag"): #there are no location to analyze
                continue

            else: 
            
                start_index = int(data[i]['label'][0][0])
                end_index = int(data[i]['label'][0][1])

                data[i]['label'].remove(data[i]['label'][0]) #remove the annotation

                column_label = text[start_index:end_index]
 
                index_in_array = splitted_text.index(column_label) #index of the column containing data to analyze

                my_text = splitted_text[index_in_array+4] #find the column in the first row with the text to analyze.
                                                          #the text will be the same for all rows

                index_my_text = splitted_text.index(my_text) #where the text to analyze starts in the data field

                len_header = 0 #find the length of the header
                for j in range(0,5):  #first 5 cells of the array contains the header
                    t = splitted_text[j]
                    len_header = len_header + len(t)

                len_header = len_header + 5 #add the number of ;



                len_row = 0 #find the length of the rows
                lens = []
                n_rows = 0


                #we should not count the header so we start from the 5th cell of the array containing the splitted text
                for j in range(5,len(splitted_text)):  #Calculate the len of all rows
                    
                    t = splitted_text[j]
                    len_row = len_row + len(t)

                    if(j%4 == 0):  # a row is made up of 4 cells
                     
                        len_row = len_row + 4 #add the number of ;
                        n_rows = n_rows + 1
                        lens.append(len_row)
                        len_row = 0
                
        

                locations_recognized = []

                if(tag == "Text_Column"): #we need to analyze the text to check if it containsany geolocation 
                    doc = nlp(my_text) #analyze the text

                    for j in range(0,len(doc.entities)):   #save the entities recognized
                        if(doc.entities[j].type == "GPE"):
                            entity = json.loads(str(doc.entities[j])) #conversion from json to python
                            locations_recognized.append(entity)

                else: #the column contains only geolocations
                    locations_recognized.append({"text":my_text,"type":"GPE","start_char":0,"end_char":len(my_text)})


                entities = []

                if(len(locations_recognized)>0):


                    for j in range(0,len(locations_recognized)):  

                            start = int(locations_recognized[j]["start_char"]) 
                            end = int(locations_recognized[j]["end_char"])

                            start_index = start +len_header+lens[0]
                            end_index = end +len_header+lens[0]

                            lun = end_index - start_index

                            #calculate the position of the location for each row

                            for cur_row in range(1,n_rows): #find the absolute position in the data field of the json object
                                entity = [start_index,end_index,"Geolocation"] 
                                print(text[start_index:end_index])
                                entities.append(entity)  
                                start_index = start_index + lens[cur_row]    
                                end_index = start_index + lun                                                            

                   

if __name__ == '__main__':
    unittest.main()

