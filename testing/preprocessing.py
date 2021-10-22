import json

def find_nth(haystack, needle, n):

    '''Return the position of the n-th (n starts at 0) needle string in the haystack string. Return -1 if not found.'''
    start = haystack.find(needle)
    while start >= 0 and n >= 1:
        start = haystack.find(needle, start+len(needle))
        n -= 1
    return start

with open('dataset.json') as dataset:

    loaded_dataset =  json.load(dataset)

    new_json_file  = open("new_dataset.json","a")
    lines_to_write = []
    json_row = 0
       
    for line in loaded_dataset:

        data = line['data']
        labels = line['label']

        header = data.split('\n')[0]

        # Remove No_Tag label, print empty labels, and continue
        if labels[0][2] == 'No_Tag':
            line['label'] = []
            #print(line)
            continue

        # Useful labels
        clean_labels = [x for x in labels if x[2] != 'No_Tag' and x[2] != 'Text_Column']
        
        # Useful labels in the header
        header_labels = [x for x in clean_labels if x[1] <= len(header)]
        #print(header_labels)

        # Column id (starting at 0) of the useful labels in the header
        header_labels_colid = [header[:x[1]].count(';') for x in header_labels]
        #print(header_labels_colid)

        
        # If nothing to be fixed, print cleaned labels, and continue
        if not header_labels:
            line['label'] = clean_labels
            lines_to_write.append(line)
            continue

        new_labels = []

        # for each new label + id
        for lab, cid in zip(header_labels, header_labels_colid):
            
            # offset from the start of the data
            start_pos = 1 + len(header) # +1 takes into account the newline char
            # for each non-header row in data:
            for row in data.split('\n')[1:-1]: # the very last row is empty, all lines are newline-terminated
                
                if cid == 0: # first column
                    p_start = 0
                    p_end = find_nth(row, ';', cid)
   
                else: # other columns
                    p_start = 1 + find_nth(row, ';', cid-1) # +1 takes into account the ; char
                    p_end = find_nth(row, ';', cid)
                    
                    if p_end == -1: # last column
                        p_end = len(row)
                        
                new_labels.append([start_pos + p_start, start_pos + p_end, lab[2]])
                start_pos += 1 + len(row) # +1 takes into account the newline char
                

        line['label'] = [x for x in clean_labels if x[1] > len(header)] + new_labels
        lines_to_write.append(line)


#print lines into a new json file used for testing

for n_line in range(0,len(lines_to_write)):

    l = json.dumps(lines_to_write[n_line])

    if( n_line == 0): #json arrays must start with a [ and objects must be separated with a ,
        json_to_write = "[" + l + ",\n"


    elif(n_line == len(lines_to_write)-1): #json arrays must end with a ]
        json_to_write = l + "]"

    else:
        json_to_write = l + ",\n"
        
    new_json_file.write(json_to_write)

new_json_file.close()
        

        
 

