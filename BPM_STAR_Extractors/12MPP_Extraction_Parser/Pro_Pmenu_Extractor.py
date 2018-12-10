import json
import csv
import datetime
from collections import OrderedDict
from GeneralHelpers import CheckFileExists
from BPM_STAR_Extractors.DataPoint import DataPoint
from BPM_STAR_Extractors.String_Parser import Parse


class MakeFile:

    @staticmethod
    def make_json_file(source_dict, filename, indent=None):
        date = datetime.date.today()
        date_string = date.strftime('%y%m%d')
        full_filename = date_string + filename + "." + DataPoint.EXT_json
        path = DataPoint.PATH_DataFiles + "\\" + full_filename
        with open(path, 'w') as file:
            json.dump(source_dict, file, indent=indent, ensure_ascii=False)
        print(full_filename + " concluded")

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
        b3902v = json.load(open(DataPoint.data_variant_final_data))
        dozempp = json.load(open(DataPoint.data_12mpp_parsed))

        bm_variants_dict = dict()
        for b in b3902v:
            bm_id = b['baumuster'][0:7]
            bm_variant = b['variant']
            total_vol_key = "total"
            variant_total_vol = 0
            if next(filter(lambda v: v == bm_variant, dozempp.keys()), None):
                variant_total_vol = int(dozempp[bm_variant][total_vol_key])
            if variant_total_vol <= 0:
                continue
            if bm_id not in bm_variants_dict.keys():  # create bm_key, start total, add variant
                bm_variants_dict[bm_id] = {total_vol_key: variant_total_vol, bm_variant: variant_total_vol}
            else:  # add variant, update total
                updated_total = bm_variants_dict[bm_id][total_vol_key] + variant_total_vol
                bm_variants_dict[bm_id].update({total_vol_key: updated_total, bm_variant: variant_total_vol})

        MakeFile.make_json_file(bm_variants_dict, DataPoint.filename_bm_qvv_vol, 2)

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
        b3902v = json.load(open(DataPoint.data_variant_final_data))
        dozempp = json.load(open(DataPoint.data_12mpp_parsed))
        bm_qvv_vol = json.load(open(DataPoint.data_qvv_bm_vol))
        bm_info = json.load(open(DataPoint.data_info_bm))
        variant_code_data = {val['variant']: val['codes'] for val in b3902v}

        end_dict = {}
        for (bm_id, variant_vol) in bm_qvv_vol.items():
            for (variant, vol) in variant_vol.items():
                if variant == "total":
                    continue
                # TODO: Proper dictionary hierarchy, current structure reeks of go-horse
                end_dict[variant] = [[[bm_id, [bm_info[bm_id][0],
                                               bm_info[bm_id][1]]],
                                      dozempp[variant]],
                                     variant_code_data[variant]]

        MakeFile.make_json_file(end_dict, DataPoint.filename_dict_end, 4)


class MakeFinalDict:
    def __init__(self):
        if CheckFileExists.Check.open_file(DataPoint.data_final_dict):
            print('dict end available')
        self.qvv_data = json.load(open(DataPoint.data_final_dict))

    def variant_info_gen(self, month_data):

        qvvs_data = list((key, values[0][0][0], values[0][0][1][0],
                          values[0][0][1][1], [i['code'] for i in values[1]], int(values[0][1][month_data]))
                         for key, values in self.qvv_data.items() if values[0][1][month_data] is not '0')

        return qvvs_data

    def variant_model_gen(self, months, year):
        qvvs_data_dict = {"year": year, 'production': []}
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
                monthly_production['data'] = swap_list
            qvvs_data_dict['production'].append(monthly_production)
        return qvvs_data_dict


# MakeFile.parsed_12mpp()
# time.sleep(5)  # TODO:routine to analise if the new file is ready for next analisys
# MakeFile.bm_qvv_vol()
# time.sleep(5)  # TODO:routine to analise if the new file is ready for next analisys
# MakeFile.concatenate_infos()
#
month_list = ['jan', 'fev', 'mar', 'abr', 'mai', 'jun', 'jul', 'ago', 'set', 'out', 'nov', 'dez', 'total']
year = 2019
#
date = datetime.date.today()
date_string = date.strftime('%y%m%d')
#
for month in month_list:
    total_qvv_list = MakeFinalDict().variant_info_gen(month)

    with open(DataPoint.PATH_DataFiles + "\\" + date_string + "_" + month + '_qvvs.csv', 'w', newline='\n') as csvfile:
        wr = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
        for line in total_qvv_list:
            wr.writerow(line)

total_qvv_dict = MakeFinalDict().variant_model_gen(month_list, year)
with open(DataPoint.PATH_DataFiles + "\\" + date_string + '_dictionary_qvvs_by_month.json', 'w') as f:
    json.dump(total_qvv_dict, f, indent=4, sort_keys=True, ensure_ascii=False)

# MakeFile.bm_qvv()
