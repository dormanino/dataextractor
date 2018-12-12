import pandas
import numpy as np
import json

data1 = json.load(open("181018_dict_end.json"))
data2 = json.load(open("181209_dict_end.json"))

# df1 = pandas.read_json("181018_dict_end.json")
# df2 = pandas.read_json("181209_dict_end.json")
#
# print(df1.head())
# print(df2.head())

list_qvv1018 = list()
list_qvv1218 = list()

for data in data1:
    if data1[data][0][1]['jan'] != '0':
        list_qvv1018.append(data)

for data in data2:
    if data2[data][0][1]['jan'] != '0':
        if data[0:3] == 'QVV':
            list_qvv1218.append(data)

print(len(list_qvv1018), len(list_qvv1218))

