import json
from BPM_STAR_Extractors.Models.QVVPartialMainData import QVVPartialMainData
from BPM_STAR_Extractors.DataPoint import DataPoint
from BPM_STAR_Extractors.Models.QVVPartialVolumeData import QVVPartialVolumeData


data_for_analisys = QVVPartialMainData.from_dict(json.load(open(DataPoint.data_12mpp_partial)))

qvv_list = []
for data in data_for_analisys.variant_data:
    qvv_list.append(data)

qvv_set = set()
qvv_repeat = set()
cereps = set()
qvv_atual = ""

for data_qvv in qvv_list:
    qvv_set.add(data_qvv.variant)
    cereps.add(data_qvv.cereps())

    if data_qvv.amnt_of_destinations() != 1:
        qvv_repeat.add(data_qvv.variant)

volume = 0
data = []
for dado in cereps:
    volume = data_qvv.total_volume()
    data.append((dado, volume))
volume = 0
print(data)
