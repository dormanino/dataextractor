import json
from BPM_STAR_Extractors.Models.QVVPartialMainData import QVVPartialMainData
from BPM_STAR_Extractors.DataPoint import DataPoint

data_for_analisys = QVVPartialMainData.from_dict(json.load(open(DataPoint.data_12mpp_partial)))

qvv_list = []
for data in data_for_analisys.variant_data:
    qvv_list.append(data)

for data_qvv in qvv_list:
    print(data_qvv)

print(qvv_list)
