import json
import csv

data = json.load(open("181209_bm_qvv_vol.json"))
file_name = "csv_bm_data.csv"

with open(file_name, 'w', newline='') as csvfile:
    # spamwriter = csv.writer(csvfile, delimiter='', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    spamwriter = csv.writer(csvfile)
    for key, value in data.items():
        string = [str(key) + "," + str(value['total'])]
        spamwriter.writerow(string)
