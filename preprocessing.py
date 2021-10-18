

from os import close, startfile
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



# Initialize the engine with logger.

nlp = stanza.Pipeline('en')


def sortTag(obj):
    return obj[2]

#the tag of stanza are different from the ones in our dataset and 
# must be converted

def convert(tag):

    if(tag == "GPE"):
        return "Geolocation"
    elif(tag == "PERSON"):
        return "Person_Name"

class TestSum(unittest.TestCase):



    def test(self):

        f_dataset = open("dataset.json")
        data = json.load(f_dataset)
        f_dataset.close()

        f_states = open("states.txt")
        states = f_states.readlines()
        f_states.close()


        count = 0
        total = 0
        false_positives = 0
        false_negatives = 0

        for i in range (0,len(data)):

            text = data[i]['data']

            #sort by tag 
            data[i]['label'].sort(key = sortTag ,reverse = True)

            tag = data[i]['label'][0][2]
           
            splitted_text = text.split(";")

            if(tag == "No_Tag"): #there are no elements to analyze
                continue

            else: 
            
                start_index = int(data[i]['label'][0][0])
                end_index = int(data[i]['label'][0][1])

                if(tag == "Text_Column"):  
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

                len_pre_my_text = 0

                for j in range(5,index_my_text):  #Calculate the len of all rows
                    
                   len_pre_my_text = len_pre_my_text + len(splitted_text[j]) + 1 # +1 because we need to add the num of ;

                

                recognized = []

                if(not tag == "Geolocation"):
                    doc = nlp(my_text) #analyze the text


                    for j in range(0,len(doc.entities)):   #save the entities recognized
                        entity = json.loads(str(doc.entities[j])) #conversion from json to python

                        if(entity["type"] == "GPE"):
                            location = entity["text"]
                            if((location+'\n') in states ): #Discard countries. They mustn't be recognized
                                continue
                             #our recognizer recognizes text such as "Ibadan,Nigeria" as a whole entity.
                             #since countries aren't supposed to be recognized, we only keep the city.
                            if(not location.find(',') == -1): 
                                app = entity["text"].split(',')
                                location = app[0] #the city
                                entity['text'] = location
                                entity['end_char'] = entity['start_char'] + len(location)


                            
                        recognized.append(entity)

                else:
                    recognized.append({"text":my_text,"type":"GPE","start_char":0,"end_char":len(my_text)})


                entities = []

                #find the number of entities that were supposed to be recognized and the ones who are actually recognized

                if(tag == "Geolocation"):   #all locations were automatically annotated and recognized
                    count = count + n_rows
                    total = total + n_rows


                else:         
                    total = total + len(data[i]['label'])

                recognizer = []

                if(len(recognized)>0):

                        for j in range(0,len(recognized)):  

                                start = int(recognized[j]["start_char"]) 
                                end = int(recognized[j]["end_char"])
                                annotation = recognized[j]["type"]
                                t = recognized[j]["text"]

                                start_index = start + len_header + len_pre_my_text
                                end_index = end + len_header + len_pre_my_text

                                lun = end_index - start_index

                                #calculate the position of the entity for each row

                                for cur_row in range(0,n_rows): #find the absolute position in the data field of the json object
                        
                                    if(annotation not in ["GPE","PERSON","GENDER"]): #keep only annotations in our dataset 
                                        continue


                                    entity = [start_index,end_index,convert(annotation)] 

                                    if( entity in data[i]['label']):
                                        count = count + 1

                                    start_index = start_index + lens[cur_row]  #calculate where the new entity begins
                                    end_index = start_index + lun  #calculate where the new entity ends
                                    
                   
                             #print(entities)
        print("recognised ",count,"total ",total,"false negatives",total-count)
                        
        

if __name__ == '__main__':
    unittest.main()


