import os
from collections import OrderedDict
import json
import datetime


# if x is present in arr[] then
# returns the index of FIRST
# occurrence of x in arr[0..n-1],
# otherwise returns -1
def first(arr, low, high, x, n):
    if high >= low:
        mid = low + (high - low) // 2
        if (mid == 0 or x > arr[mid - 1]) and arr[mid] == x:
            return mid
        elif x > arr[mid]:
            return first(arr, (mid + 1), high, x, n)
        else:
            return first(arr, low, (mid - 1), x, n)

    return -1


# if x is present in arr[] then
# returns the index of LAST occurrence
# of x in arr[0..n-1], otherwise
# returns -1
def last(arr, low, high, x, n):
    if high >= low:
        mid = low + (high - low) // 2
        if (mid == n - 1 or x < arr[mid + 1]) and arr[mid] == x:
            return mid
        elif x < arr[mid]:
            return last(arr, low, (mid - 1), x, n)
        else:
            return last(arr, (mid + 1), high, x, n)

    return -1


# provide txt file
with open(os.getcwd() + '\\B3902V.TXT', 'r') as file:
    # remove new line from string
    txtfile = (line.rstrip('\n') for line in file.readlines())


    readlines = None
    data_list = None

    list_num_var = []
    num = 0
    var_list = []

    # creates a list transforming the string data in variants with numbers in order to last and first
    # functions to work
    # also create mail file data
    counter = 0
    for obj in enumerate(data_list_srt):
        print(obj)
        for index in obj:
            print(obj.count(index), index)

    for index, obj in enumerate(data_list_srt):
        if index == 0:
            list_num_var.append(0)
            dict_var = OrderedDict()
            dict_var['index'] = counter
            dict_var['plant'] = data_list_srt[index][0]
            dict_var['variant'] = data_list_srt[index][1]
            dict_var['baumuster'] = data_list_srt[index][2]
            dict_var['valid_by'] = data_list_srt[index][3]
            dict_var['valid_till'] = data_list_srt[index][4]
            dict_var['validity_index'] = data_list_srt[index][5]
            dict_var['aggregate_desciption'] = data_list_srt[index][9]
            dict_var['variant_plausibility'] = data_list_srt[index][11]
            var_list.append(dict_var)
            counter += 1
        elif data_list_srt[index][1] != data_list_srt[index - 1][1]:
            num += 1
            list_num_var.append(num)
            dict_var = OrderedDict()
            dict_var['index'] = counter
            dict_var['plant'] = data_list_srt[index][0]
            dict_var['variant'] = data_list_srt[index][1]
            dict_var['baumuster'] = data_list_srt[index][2]
            dict_var['valid_by'] = data_list_srt[index][3]
            dict_var['valid_till'] = data_list_srt[index][4]
            dict_var['validity_index'] = data_list_srt[index][5]
            dict_var['aggregate_desciption'] = data_list_srt[index][9]
            dict_var['variant_plausibility'] = data_list_srt[index][11]
            var_list.append(dict_var)
            counter += 1
        else:
            list_num_var.append(num)
    # data_list_srt = None

    date = datetime.date.today()
    date_string = date.strftime('%y%m%d')

    with open(date_string + '_' + 'variant_data', 'w') as f:
        json.dump(var_list, f, indent=4, sort_keys=True, ensure_ascii=False)
    var_list = None
    f = None


    num = None
    st_en = []
    i = 0

    # find first and last occurence in the registers
    while i < (len(list_num_var)):
        num_ini = first(list_num_var, i, len(list_num_var), list_num_var[i], len(list_num_var))
        num_fin = last(list_num_var, i, len(list_num_var), list_num_var[i], len(list_num_var))
        st_en.append((num_ini, num_fin))

        if num_fin != len(list_num_var) - 1:
            i = num_fin + 1
        else:
            break

    var_list = []

    i = 0
    final_register = 0
    register_index = 0

    while i < len(data_list_srt):
        dict_code = OrderedDict()
        for a, b in st_en:
            final_register = b
            if a == b:
                dict_code['code_prefix'] = (data_list_srt[a][6])
                dict_code['code'] = (data_list_srt[a][7])
                dict_code['bg'] = (data_list_srt[a][8])
                dict_code['code_description'] = data_list_srt[a][10]
                break
            else:
                for st_en_rng in range(a, b):
                    dict_code['code_prefix'] = (data_list_srt[st_en_rng][6])
                    dict_code['code'] = (data_list_srt[st_en_rng][7])
                    dict_code['bg'] = (data_list_srt[st_en_rng][8])
                    dict_code['code_description'] = data_list_srt[st_en_rng][10]
                break
        var_list.append(code)
        register_index += 1

        if final_register != len(data_list_srt):
            i = final_register + 1
        else:
            break

    date = datetime.date.today()
    date_string = date.strftime('%y%m%d')

    with open(date_string + '_' + 'variant_data', 'w') as f:
        json.dump(var_list, f, indent=4, sort_keys=True, ensure_ascii=False)

# TODO: save following code for future snippets
# num_ini = data_list.index (data_list[i])
# num_fin = len (data_list) - 1 - data_list[::-1].index (data_list[i])
