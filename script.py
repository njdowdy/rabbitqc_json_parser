import json
import os
import re
import csv
import pandas as pd

external_input = '/home/njdowdy/Documents/RabbitQC_Reports/'  # define input directory containing json data
input_read_data = 'input/raw_read_analysis.csv'

sequence_ids = []
filenames = []
total_raw_read_counts = []
paired_raw_read_counts = []
dates = []
headers = ['Individual', 'filename', 'date', 'total_raw_read_count', 'paired_raw_read_count']

for subdir, dirs, files in os.walk(external_input):
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
                total_raw_read_count = int(obj['summary']['before_filtering']['total_reads'])
                total_raw_read_counts.append(total_raw_read_count)
                paired_raw_read_counts.append(total_raw_read_count/2)
                dates.append(str(subdir.split('/')[-1]))
            else:
                print(f"WARNING!... File Empty: " + file)

# convert json data to dataframe
json_data_0 = zip(sequence_ids, filenames, dates, total_raw_read_counts, paired_raw_read_counts)
json_data = pd.DataFrame(list(json_data_0), columns=headers)

# write output data to csv
rows = zip(sequence_ids, filenames, dates, total_raw_read_counts, paired_raw_read_counts)
with open('output/output.csv', "w") as f:
    writer = csv.writer(f)
    writer.writerow(headers)
    for row in rows:
        writer.writerow(row)

# pair to assembly data
assembly_data = pd.read_csv(input_read_data)

# merge json and assembly data
merged_data = pd.merge(assembly_data, json_data, on=['Individual'], how='right')

# make new column with percent reads
merged_data["percent_recovered_total"] = merged_data["total_raw_read_count"] / merged_data["nRawReads"]
merged_data["percent_recovered_paired"] = merged_data["paired_raw_read_count"] / merged_data["nRawReads"]

# write to csv
merged_data.to_csv('output/merged_data.csv', header=True, index=False)
