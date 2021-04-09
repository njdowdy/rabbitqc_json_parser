import json
import os
import re
import csv

input_dir = '/home/njdowdy/Documents/RabbitQC_Reports/TEST DATA/'  # define input directory containing json data
output = {'id': 'rawReadCount'}  # define output dictionary with header row

for subdir, dirs, files in os.walk(input_dir):
    for file in files:
        if '.json' in file:
            # read file
            with open(os.path.join(subdir, file), 'r') as myfile:
                data = myfile.read()
            # parse file
            obj = json.loads(data)
            # print read number
            # print("file: " + str(re.findall(r'_(I[0-9]*)_', file)[0]))
            # print("reads: " + str(obj['summary']['before_filtering']['total_reads']))
            # store data
            output.update({str(re.findall(r'_(I[0-9]*)_', file)[0]): int(obj['summary']
                                                                         ['before_filtering']
                                                                         ['total_reads'])})

# write output data to csv
with open('output/test.csv', 'w') as f:
    writer = csv.writer(f)
    for k, v in output.items():
        writer.writerow([k, v])
