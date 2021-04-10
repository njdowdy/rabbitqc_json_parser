import json
import os
import re
import csv

input_dir = '/home/njdowdy/Documents/RabbitQC_Reports/'  # define input directory containing json data
output = {'sequenceID': 'rawReadCount'}  # define output dictionary with header row
sequence_ids = ['sequenceID']
filenames = ['filename']
raw_read_counts = ['raw_read_count']
dates = ['date']

for subdir, dirs, files in os.walk(input_dir):
    for file in files:
        if '.json' in file:
            # read file
            with open(os.path.join(subdir, file), 'r') as myfile:
                data = myfile.read()
            # parse file
            if data != '':
                obj = json.loads(data)
                # print read number
                # print("file: " + str(re.findall(r'_(I[0-9]*)_', file)[0]))
                # print("reads: " + str(obj['summary']['before_filtering']['total_reads']))
                # parse and store data
                filenames.append(file)
                sequence_id = str(re.findall(r'(I[0-9]*)_', file)[0])
                sequence_ids.append(sequence_id)
                raw_read_count = int(obj['summary']['before_filtering']['total_reads'])
                raw_read_counts.append(raw_read_count)
                dates.append(str(subdir.split('/')[-1]))
            else:
                print(f"WARNING!... File Empty: " + file)
# write output data to csv
rows = zip(filenames, sequence_ids, dates, raw_read_counts)
with open('output/output.csv', "w") as f:
    writer = csv.writer(f)
    for row in rows:
        writer.writerow(row)
