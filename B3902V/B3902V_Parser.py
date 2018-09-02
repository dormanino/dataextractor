import datetime
import json
from collections import OrderedDict
from B3902V.Data.DataPoint import DataPoint


def parse_b3902v_raw_data():

    slices = [(0, 3), (3, 24), (24, 45), (45, 53), (53, 61), (61, 62), (62, 64), (64, 83),
              (83, 85), (85, 115), (115, 145), (145, 146)]
    data_list = sorted(
        [tuple
         (line
          [slice(start, end)].strip() for start, end in [part for part in slices]
          ) for line in open(DataPoint.data_b3902v, 'r')], key=lambda x: x[1])

    # file = json.load(open(LatestFileVersion.latest_file_version('json', 'variant_data_raw')))

    slice_start_end = None
    data_concluded = False
    start_data_chk = ''
    counter = 0
    final_data_list = []

    for line, data in enumerate(data_list):
        if (start_data_chk != data[1]) or (line == len(data_list) - 1):
            if line == 0:
                start_data_chk = data[1]
            else:
                data_concluded = True  # flow control
                start_data_chk = data[1]  # reset data for comparison
                if line == len(data_list) - 1:
                    slice_start_end = (int(line - counter), int(line))  # (counter - line) start of chunk and (line - 1) = end of chunk
                else:
                    slice_start_end = (int(line - counter), int(line - 1))  # (counter - line) start of chunk and (line - 1) = end of chunk
                counter = 0  # counter reset
        counter += 1

        if data_concluded:
            dict_var = OrderedDict()
            code_data = OrderedDict()
            code_list = []
            code_prefix_preview = ''
            for i in range(slice_start_end[0], slice_start_end[1] + 1):
                # if the index is the last chunk information, create the header with all code dict
                # since the file is sorted by similarity between fields
                if i == (slice_start_end[0]):
                    code_prefix_preview = data_list[i][6]  # set the main prefix in case of different one
                code_data['code'] = data_list[i][7]
                code_data['bg'] = data_list[i][8]
                code_data['code_description'] = data_list[i][10]
                if code_prefix_preview != data_list[i][6]:  # creation of different prefix into the data
                    code_data['qw'] = data_list[i][6]
                code_list.append(code_data)
                code_data = OrderedDict()
                if i == (slice_start_end[1]):
                    dict_var['plant'] = data_list[i][0]
                    dict_var['variant'] = data_list[i][1]
                    dict_var['baumuster'] = data_list[i][2]
                    dict_var['valid_by'] = data_list[i][3]
                    dict_var['valid_till'] = data_list[i][4]
                    dict_var['validity_index'] = data_list[i][5]
                    dict_var['code_prefix'] = code_prefix_preview
                    dict_var['aggregate_description'] = data_list[i][9]
                    dict_var['variant_plausibility'] = data_list[i][11]
                    dict_var['codes'] = code_list
            final_data_list.append(dict_var)
            data_concluded = False  # flow control

    date = datetime.date.today()
    date_string = date.strftime('%y%m%d')

    with open(DataPoint.PATH_DataFiles + "\\" + date_string + '_variant_data_raw.json', 'w') as f:
        json.dump(data_list, f, sort_keys=True, ensure_ascii=False)

    with open(DataPoint.PATH_DataFiles + "\\" + date_string + '_final_variant_data.json', 'w') as f:
        json.dump(final_data_list, f, indent=4, sort_keys=True, ensure_ascii=False)


parse_b3902v_raw_data()
