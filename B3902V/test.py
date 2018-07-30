import os
import time
import sys
import datetime
import json
import LatestFileVersion
from functools import partial
from collections import OrderedDict
from B3902V.Data import DataPoint


def it():
    b3902v_file = DataPoint.data_b3902v
    # provide txt file
    # (62, 64), (64, 83), (83, 85), (115, 145)
    slices = [(0, 3), (3, 24), (24, 45), (45, 53), (53, 61), (61, 62), (62, 64), (64, 83), (83, 85), (85, 115), (115, 145), (145, 146)]
    start_time = time.time()
    # set() will only include items that are not already inside it
    # tuple() because its immutable and a smaller data type
    # data_list = sorted((line[slice(start, end)].strip() for start, end in [part for part in slices]) for line in open(os.getcwd() + '\\B3902V - Copia.TXT', 'r'), key=lambda x: x[1])

    #data_list = ((line[slice(start, end)].strip() for start, end in [part for part in slices]) for line in open(os.getcwd() + '\\B3902V - Copia.TXT', 'r'))
    data_list = sorted([tuple(line[slice(start, end)].strip() for start, end in [part for part in slices]) for line in open(b3902v_file, 'r')], key=lambda x: x[1])

    # data_list = set(tuple(line[slice(start, end)].strip()
                          # for start, end in [part for part in slices])
                    # for line in open(os.getcwd() + '\\B3902V - Copia.TXT', 'r'))

    # data_list = set (tuple (line[slice (start, end)].strip ()
    # for start, end in [part for part in slices]) for line in
    # open (os.getcwd () + '\\B3902V.TXT', 'r'))


    # change tuple to list to
    print(sys.getsizeof(data_list), type(data_list))
    # data_list_srt = sorted(data_list_to_srt, key=lambda x: x[1])

    # date = datetime.date.today()
    date_string = datetime.date.today().strftime('%y%m%d')

    with open(date_string + '_' + 'variant_data_raw.json', 'w') as f:
        json.dump(data_list, f, sort_keys=True, ensure_ascii=False)

    # with open('data.pkl', 'wb') as output:
    #     # pickle.dump(data_list_srt, outpu    t)
    #     pickle.dump(data_list_srt, output, -1)
    # print(sys.getsizeof(txtfile), "--- %s GB's ---" % int(sys.getsizeof(txtfile) / 10000000))
    print("--- %s seconds ---" % (time.time() - start_time))
    print("concluded")


def it2():
    # provide txt file
    # (62, 64), (64, 83), (83, 85), (115, 145)
    # (0, 3)
    # [(62, 64), (64, 83), (83, 85), (115, 145), (85, 115)
    slices = [(3, 24)]
    start_time = time.time()
    data_list = [[line[slice(start, end)].strip()
                 for start, end in [part for part in slices]]
                 for line in open(os.getcwd() + '\\B3902V - Copia.TXT', 'r')]

    """
     data_list = set (tuple (line[slice (start, end)].strip () for start, end in [part for part in slices])
     for line in open (os.getcwd () + '\\B3902V.TXT', 'r'))
    """

    data_list_srt = sorted(data_list, key=lambda x: x[0])
    dicto = {}
    start = 0
    for index, obj in enumerate(data_list_srt):
        if index == 0:
            start = index
        elif data_list_srt[index][0] != data_list_srt[index - 1][0]:
            end = index - 1
            dat_tuple = (start, end)
            dicto[data_list_srt[index - 1][0]] = dat_tuple
            start = index
        elif index + 1 == len(data_list_srt):
            end = index - 1
            dat_tuple = (start, end)
            dicto[data_list_srt[index][0]] = dat_tuple

    date = datetime.date.today()
    date_string = date.strftime('%y%m%d')

    with open(date_string + '_' + 'variant_data_raw.json', 'w') as f:
        json.dump(dicto, f, indent=4, sort_keys=True, ensure_ascii=False)

    # print(sys.getsizeof(txtfile), "--- %s GB's ---" % int(sys.getsizeof(txtfile) / 10000000))
    print("--- %s seconds ---" % (time.time() - start_time))
    print("concluded")


def it3():
    start_time = time.time()
    file = LatestFileVersion.latest_file_version('json', 'variant_data_raw')
    with open(file, 'r') as infh:
        for data in json_parse(infh):
            print(data)

    print("--- %s seconds ---" % (time.time() - start_time))


def it4():

    start_time = time.time()
    file = json.load(open(LatestFileVersion.latest_file_version('json', 'variant_data_raw')))
    slice_start_end = None
    data_concluded = False
    start_data_chk = ''
    counter = 0
    final_data_list = []

    for line, data in enumerate(file):
        if (start_data_chk != data[1]) or (line == len(file) - 1):
            if line == 0:
                start_data_chk = data[1]
            else:
                data_concluded = True  # flow control
                start_data_chk = data[1]  # reset data for comparison
                if line == len(file) - 1:
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
                    code_prefix_preview = file[i][6]  # set the main prefix in case of different one
                code_data['code'] = file[i][7]
                code_data['bg'] = file[i][8]
                code_data['code_description'] = file[i][10]
                if code_prefix_preview != file[i][6]:  # creation of different prefix into the data
                    code_data['qw'] = file[i][6]
                code_list.append(code_data)
                code_data = OrderedDict()
                if i == (slice_start_end[1]):
                    dict_var['plant'] = file[i][0]
                    dict_var['variant'] = file[i][1]
                    dict_var['baumuster'] = file[i][2]
                    dict_var['valid_by'] = file[i][3]
                    dict_var['valid_till'] = file[i][4]
                    dict_var['validity_index'] = file[i][5]
                    dict_var['code_prefix'] = code_prefix_preview
                    dict_var['aggregate_description'] = file[i][9]
                    dict_var['variant_plausibility'] = file[i][11]
                    dict_var['codes'] = code_list
            final_data_list.append(dict_var)
            data_concluded = False  # flow control

    print("--- %s seconds ---" % (time.time() - start_time))

    file = None

    date = datetime.date.today()
    date_string = date.strftime('%y%m%d')

    with open(date_string + '_' + 'final_variant_data.json', 'w') as f:
        json.dump(final_data_list, f, indent=4, sort_keys=True, ensure_ascii=False)

    print("--- %s seconds ---" % (time.time() - start_time))


def json_parse(fileobj, decoder=json.JSONDecoder(), buffersize=2048):
    buffer = ''
    for chunk in iter(partial(fileobj.read, buffersize), ''):
        buffer += chunk
        while buffer:
            try:
                result, index = decoder.raw_decode(buffer)
                yield result
                buffer = buffer[index:]
            except ValueError:
                # Not enough data to decode, read more
                break


it()
it4()
