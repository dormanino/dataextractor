import json
import csv
import datetime
import time
from collections import OrderedDict
from GeneralHelpers import CheckFileExists
from BPM_STAR_Extractors.DataPoint import DataPoint
from BPM_STAR_Extractors.String_Parser import Parse
from collections import namedtuple


class MakeFile:

    @staticmethod
    def parsed_12mpp():
        # loads json file 12mpp raw data as a dictionary
        volume_data_raw_dict = json.load(open(DataPoint.data_12mpp))
        print(type(volume_data_raw_dict))  # dictionary
        nd = {}
        lista = []
        month_list = ['jan', 'fev', 'mar', 'abr', 'mai', 'jun', 'jul', 'ago', 'set', 'out', 'nov', 'dez', 'total']

        for key, val in volume_data_raw_dict.items():
            for i in val[1]:
                lista = Parse.parse(i)
            # TODO: change json from list with one string to only string
            nd[key[slice(1, 29)].strip().replace(' ', '')] = dict(zip(month_list, lista))

        date = datetime.date.today()
        date_string = date.strftime('%y%m%d')

        with open(DataPoint.PATH_DataFiles + "\\" + date_string + "_12mpp_parsed.json", "w") as f:
            json.dump(nd, f, indent=4, sort_keys=True, ensure_ascii=False)

    @staticmethod
    def bm_qvv_vol():

        while not CheckFileExists.Check.open_file(DataPoint.data_variant_final_data):
            print('fst pass final variant data not available')
        print('fst pass final variant data available')

        while not CheckFileExists.Check.open_file(DataPoint.data_12mpp_parsed):
            print('fst pass 12 mpp data not available')
        print('fst pass 12 mpp data available')

        b3902v = json. load(open(DataPoint.data_variant_final_data))
        dozempp = json.load(open(DataPoint.data_12mpp_parsed))
        # TODO: dict comprehension
        dicto_tst = {}
        for b in b3902v:
            dicto_tst[str(b['variant'])] = b['baumuster'][0:7]

        final_dict = {}
        # TODO: dict comprehension
        for dc in dozempp:
            if dozempp[dc]['total'] != '0':
                final_dict[dc] = dozempp[dc]['total']

        for f in final_dict:
            for b in dicto_tst:
                if f == b:
                    if f == 'QVV81503113B':
                        print(f)
                    volume = final_dict[f]
                    final_dict[f] = dicto_tst[b], volume
                    break

        set_bm = set()
        for dt in final_dict.values():
            set_bm.add(dt[0])
        print(set_bm)

        data_sum = 0
        dict_tst = {}
        data_tot_sum = 0
        for po in set_bm:
            for dt in final_dict.items():
                if po == dt[1][0]:
                    data_sum += int(dt[1][1])
            data_tot_sum += data_sum
            dict_tst[po] = data_sum
            data_sum = 0

        date = datetime.date.today()
        date_string = date.strftime('%y%m%d')

        with open(DataPoint.PATH_DataFiles + "\\" + date_string + '_qvv_bmvol.json', 'w') as f:
            json.dump(final_dict, f, indent=2, sort_keys=True, ensure_ascii=False)

            time.sleep(3)
            while not CheckFileExists.Check.open_file(DataPoint.PATH_DataFiles + "\\" + date_string + '_qvv_bmvol.json'):
                print('not ready')
                time.sleep(3)
            print('ready')

        with open(DataPoint.PATH_DataFiles + "\\" + date_string + '_bmvol_tot.json', 'w') as f:
            json.dump(dict_tst, f, sort_keys=True, ensure_ascii=False)

    @staticmethod
    def bm_qvv():

        b3902v = json. load(open(DataPoint.data_variant_final_data))
        dozempp = json.load(open(DataPoint.data_12mpp_parsed))
        bm_dict = json.load(open(DataPoint.data_info_bm))

        swap_dict = {}
        for item in b3902v:
            if item['baumuster'][0] == 'C' and item['validity_index'] == 'S' and item['variant_plausibility'] == '1':
                if item['baumuster'][0:7] in bm_dict:
                    info_bm = bm_dict[item['baumuster'][0:7]]
                else:
                    info_bm = ['notfound', 'notfound']

                swap_dict[item['variant']] = {'description': item['aggregate_description'],
                                              'baumuster': item['baumuster'],
                                              'family': info_bm[1]
                                              }

        with open(DataPoint.PATH_DataFiles + "\\" + 'qvv_by_bm_by_family.csv', 'w', newline='\n') as csvfile:
            wr = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
            for variant, info in swap_dict.items():
                line = variant, info['description'], info['baumuster'], info['family']
                wr.writerow(line)

        return print('done')

        # for variant in swap_dict:
        #     for data in bm_dict:
        #         if variant['baumuster'][0:7] == data:
        #             for dozempp_item in dozempp:
        #                 if item['baumuster'][0] == 'C' and item['validity_index'] == 'S' and item['variant_plausibility'] == '1':
        #                     if item['variant'] == dozempp_item:
        #                         swap_dict[item['variant']] = [namedtuple('description', item['aggregate_description']),
        #                                                       namedtuple('baumuster', item['baumuster']),
        #                                                       namedtuple('family', data[1]),
        #                                                       namedtuple('volume', dozempp_item['total'])
        #                                                       ]
        #                     else:
        #                         volume = 0
        #                         swap_dict[item['variant']] = [namedtuple('description', item['aggregate_description']),
        #                                                       namedtuple('baumuster', item['baumuster']),
        #                                                       namedtuple('family', data[1]),
        #                                                       namedtuple('volume', str(volume))
        #                                                       ]

    @staticmethod
    def concatenate_infos():

        while not CheckFileExists.Check.open_file(DataPoint.data_qvv_bm_vol):
            print('qvv_bm_vol not available')
            time.sleep(5)
        print('qvv_bm_vol available')
        CheckFileExists.Check.open_file(DataPoint.data_variant_final_data)
        print('variant final data available')
        CheckFileExists.Check.open_file(DataPoint.data_info_bm)
        print('info bm available')
        CheckFileExists.Check.open_file(DataPoint.data_12mpp_parsed)
        print('12mpp parsed available')

        qvv_info = json.load(open(DataPoint.data_qvv_bm_vol))
        b3902v_info = json.load(open(DataPoint.data_variant_final_data))
        gen_info = json.load(open(DataPoint.data_info_bm))
        prog_prod = json.load(open(DataPoint.data_12mpp_parsed))

        dicto = {}
        qvv_with_volume_list = [[key, val] for key, val in qvv_info.items()]
        info_a_ver = [[info, bm] for info, bm in gen_info.items()]
        for bm_qvv in qvv_with_volume_list:
            for bm_info in info_a_ver:
                if bm_info[0] == bm_qvv[1][0]:
                    dicto[bm_qvv[0]] = bm_info

        for key_dicto, val_dicto in dicto.items():
            if 'QVV81503113B' == key_dicto:
                print('yes')

            if key_dicto in prog_prod:
                dicto[key_dicto] = [dicto[key_dicto], prog_prod[key_dicto]]
        print('not found')

        data_prev = {val['variant']: val['codes'] for val in b3902v_info}

        for key_dicto, val_dicto in dicto.items():
            if key_dicto in data_prev:
                dicto[key_dicto] = [dicto[key_dicto], data_prev[key_dicto]]

        date = datetime.date.today()
        date_string = date.strftime('%y%m%d')

        with open(DataPoint.PATH_DataFiles + "\\" + date_string + '_dict_end.json', 'w') as f:
            json.dump(dicto, f, indent=4, sort_keys=True, ensure_ascii=False)
    print('dict_end.json concluded')


class MakeFinalDict:
    def __init__(self):
        if CheckFileExists.Check.open_file(DataPoint.data_final_dict):
            print('dict end available')
        self.qvv_data = json.load(open(DataPoint.data_final_dict))

    def variant_info_gen(self, month_data, year):

        qvvs_data = list((key, values[0][0][0], values[0][0][1][0],
                          values[0][0][1][1], [i['code'] for i in values[1]], int(values[0][1][month_data]))
                         for key, values in self.qvv_data.items() if values[0][1][month_data] is not '0')

        return qvvs_data

    def variant_model_gen(self, months):
        qvvs_data_dict = {'production': []}
        for month in months:
            monthly_production = {'month': '',  # change to `month_year` and pass year along
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
                monthly_production['year'] = year
                monthly_production['data'] = swap_list
            qvvs_data_dict['production'].append(monthly_production)
        return qvvs_data_dict


# MakeFile.parsed_12mpp()
# time.sleep(5)  # TODO:routine to analise if the new file is ready for next analisys
# MakeFile.bm_qvv_vol()
# time.sleep(5)  # TODO:routine to analise if the new file is ready for next analisys
# MakeFile.concatenate_infos()
#
# month_list = ['jan', 'fev', 'mar', 'abr', 'mai', 'jun', 'jul', 'ago', 'set', 'out', 'nov', 'dez', 'total']
# year = 2019
#
# date = datetime.date.today()
# date_string = date.strftime('%y%m%d')
#
# for month in month_list:
#     total_qvv_list = MakeFinalDict().variant_info_gen(month, year)
#
#     with open(DataPoint.PATH_DataFiles + "\\" + date_string + "_" + month + '_qvvs.csv', 'w', newline='\n') as csvfile:
#         wr = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
#         for line in total_qvv_list:
#             wr.writerow(line)
#
# total_qvv_dict = MakeFinalDict().variant_model_gen(month_list)
# with open(DataPoint.PATH_DataFiles + "\\" + date_string + '_dictionary_qvvs_by_month.json', 'w') as f:
#     json.dump(total_qvv_dict, f, indent=4, sort_keys=True, ensure_ascii=False)

MakeFile.bm_qvv()
