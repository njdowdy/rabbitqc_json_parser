import json
import os
import re
import csv

input_dir = '/home/njdowdy/Documents/RabbitQC_Reports/TEST DATA/'  # define input directory containing json data
output = {'sequenceID': 'rawReadCount'}  # define output dictionary with header row

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
            # parse data
            sequence_id = str(re.findall(r'_(I[0-9]*)_', file)[0])
            raw_reads = int(obj['summary']['before_filtering']['total_reads'])
            # store data
            if sequence_id not in output:
                output.update({sequence_id: raw_reads})
            else:  # if sequence_id exists, the reads were split into multiple files; add them up
                # TODO: ensure DATE is same; redos from other dates maybe should not be added together
                # TODO: track the number of files added together; doesn't fit in dictionary though
                output.update({sequence_id: output[sequence_id] + raw_reads})
# write output data to csv
with open('output/test.csv', 'w') as f:
    writer = csv.writer(f)
    for k, v in output.items():
        writer.writerow([k, v])
