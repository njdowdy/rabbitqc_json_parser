# rabbitqc_json_parser
Code to parse output from RabbitQC

This code takes in a directory containing outputs from RabbitQC. It parses information from the JSON-formatted output file for compilation into a data object (e.g., database, dataframe, excel, etc) via a CSV file.

Currently, only the sample ID and raw read count are collected. Because this is designed for AHE reads from the Lemmon Lab at FSU, it is assumed the file names will resemble:

P0060_JZ_I4289_TTCATACG_L002_R1_001.json

Most importantly, the "Specimen ID" is taken to be the part of the filename matching "_I####_".
