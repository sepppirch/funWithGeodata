import json
 
# Opening JSON file

with open('nodes.txt', 'w') as out:

    with open('nodes.json') as f:
        json_data = json.load(f)
    # returns JSON object as

        x = json_data['nodes']
        for i in range(len(x)):
            line = str(i)+','+str(x[i]['n'])
            out.write(line)
            out.write('\n')
            print(line)
    


 
# Closing file
f.close()