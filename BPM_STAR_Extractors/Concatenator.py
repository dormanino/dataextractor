from BPM_STAR_Extractors.DataPoint import DataPoint
import json
import csv
import datetime
from collections import OrderedDict


class Makover:
    def __init__(self):
        self.qvv_data = json.load(open(DataPoint.data_mashed))

    def vartiant_info_gen(self, month_data):

        qvvs_data = list((key, values[0][0][0], values[0][0][1][0], values[0][0][1][1], [i['code'] for i in values[1]], int(values[0][1][month_data]))
                         for key, values in self.qvv_data.items() if values[0][1][month_data] is not '0')

        return qvvs_data

    def vartiant_model_gen(self, months):
        qvvs_data_dict = {'production': []}
        for month in months:
            monthly_production = {'month': '',
                                  'data': []}
            swap_list = []

            for key, values in self.qvv_data.items():
                if values[0][1][month] is not '0':
                    main_dict = OrderedDict()
                    main_dict['qvv'] = key
                    main_dict['bm'] = values[0][0][0]
                    main_dict['bu'] = values[0][0][1][0]
                    main_dict['family'] = values[0][0][1][1]
                    main_dict['composition'] = [i['code'] for i in values[1]]
                    main_dict['volume'] = int(values[0][1][month])
                    swap_list.append(main_dict)
                monthly_production['month'] = month
                monthly_production['data'] = swap_list
            qvvs_data_dict['production'].append(monthly_production)
        return qvvs_data_dict


month_list = ['jan', 'fev', 'mar', 'abr', 'mai', 'jun', 'jul', 'ago', 'set', 'out', 'nov', 'dez', 'total']

for month in month_list:
    total_qvv_list = Makover().vartiant_info_gen(month)

    with open(month + '_qvvs.csv', 'w', newline='\n') as csvfile:
        wr = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
        for line in total_qvv_list:
            wr.writerow(line)

date = datetime.date.today()
date_string = date.strftime('%y%m%d')

total_qvv_dict = Makover().vartiant_model_gen(month_list)
with open(date_string + 'dictionary_qvvs_by_month.json', 'w') as f:
    json.dump(total_qvv_dict, f, indent=4, sort_keys=True, ensure_ascii=False)
