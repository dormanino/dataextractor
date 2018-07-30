from BPM_STAR_Extractors.DataPoint import DataPoint
import json
import csv


class Makover:
    def __init__(self):
        self.qvv_data = json.load(open(DataPoint.data_mashed))

    def vartiant_info_gen(self):

        july_qvvs = list(((key, values[0][0][0], values[0][0][1][0], values[0][0][1][1], [i for i in values[1][0]], int(values[0][1]['jul']))
                          for key, values in self.qvv_data.items() if values[0][1]['jul'] is not '0'))
        print(july_qvvs)
        august_qvvs = list((key, values[0][0][0], values[0][0][1][0], values[0][0][1][1], int(values[0][1]['ago']))
                           for key, values in self.qvv_data.items() if values[0][1]['ago'] is not '0')
        total_qvvs = list((key, values[0][0][0], values[0][0][1][0], values[0][0][1][1], int(values[0][1]['total']))
                          for key, values in self.qvv_data.items() if values[0][1]['total'] is not '0')

        return july_qvvs, august_qvvs, total_qvvs


jul, aug, total = Makover().vartiant_info_gen()

with open('july_qvvs.csv', 'w', newline='\n') as csvfile:
    wr = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
    for line in jul:
        wr.writerow(line)

with open('aug_qvvs.csv', 'w', newline='\n') as csvfile:
    wr = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
    for line in aug:
        wr.writerow(line)

with open('total_qvvs.csv', 'w', newline='\n') as csvfile:
    wr = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
    for line in total:
        wr.writerow(line)

