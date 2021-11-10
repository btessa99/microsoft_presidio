


import json
from collections import namedtuple
import re
import os

def find_nth(haystack, needle, n):
    start = haystack.find(needle)
    while start >= 0 and n >= 1:
        start = haystack.find(needle, start+len(needle))
        n -= 1
    return start



def preprocess_file():

    Label = namedtuple('Label', 'start, end, tag')


    with open('../pira_dataset.jsonl') as dataset:
        lines = []
        for line in dataset:
            line = json.loads(line) 
            original_data = line['data']
            new_data = re.sub('[^0-9a-zA-Z]', ' ', original_data)
            original_labels = line['label']
            named_labels = [Label._make(l) for l in original_labels]

            header = original_data.split('\n')[0]

            if named_labels[0].tag == 'No_Tag':
                line['label'] = []
                line['data'] = new_data
                continue
        
            named_labels  = [x for x in named_labels if x.tag not in ('No_Tag', 'Text_Column')]
            header_labels = [x for x in named_labels if x.start < len(header)]
            other_labels  = [x for x in named_labels if x.start >= len(header)]
            
            if not header_labels:
                tmp = []
                for x in named_labels:
                    if x.tag == 'Geolocation':
                        tmp += [[x.start, x.end, 'GPE']]
                    else:
                        tmp += [list(x)]
                line['label'] = tmp
                line['data'] = new_data
                lines.append(line)
                continue


            # Column id (starting at 0) of the useful labels in the header
            header_label_ids = [header[:x[1]].count(';') for x in header_labels]

            new_labels = []
            # for each new label + id
            for lab, cid in zip(header_labels, header_label_ids):
                # offset from the start of the data
    #            print(len(header), header)
                start_pos = 1 + len(header) # +1 takes into account the newline char
                # for each non-header row in data:
                for row in original_data.strip().split('\n')[1:]: # the very last row is empty, all lines are newline-terminated
    #                print(len(row), row, cid)
                    if cid == 0: # first column
                        p_start = 0
                        p_end = find_nth(row, ';', cid)
                    else: # other columns
                        p_start = 1 + find_nth(row, ';', cid-1) # +1 takes into account the ; char
                        p_end = find_nth(row, ';', cid)
                    if p_end == -1: # last column
                        p_end = len(row)
    #                print(p_start, p_end)    
    #                print('---', Label(start_pos + p_start, start_pos + p_end, lab[2]))
                    new_labels.append(Label(start_pos + p_start, start_pos + p_end, lab[2]))
                    start_pos += 1 + len(row) # +1 takes into account the newline char
                # line['label'] = [tuple(x) for x in other_labels + new_labels]
                
            tmp = []
            for x in other_labels + new_labels:
                if x.tag == 'Geolocation':
                    tmp += [[x.start, x.end, 'GPE']]
                else:
                    tmp += [list(x)]
            line['label'] = tmp
            line['data'] = new_data
            lines.append(line)

            continue



    with open('../new_dataset.json',"w") as dataset:
        

        for n_line in range(0,len(lines)):
        
            l = json.dumps(lines[n_line])

            if( n_line == 0): #json arrays must start with a [ and objects must be separated with a ,
                json_to_write = "[" + l + ",\n"


            elif(n_line == len(lines)-1): #json arrays must end with a ]
                json_to_write = l + "]"

            else:
                json_to_write = l + ",\n"

            b = dataset.write(json_to_write)

 

 










