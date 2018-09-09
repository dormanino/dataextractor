import json
from BPM_STAR_Extractors.DataPoint import DataPoint
from BPM_STAR_Extractors.Playground.QVVPartialDataAnalysis import QVVPartialDataAnalysis
from BPM_STAR_Extractors.Models.QVVPartialMainData import QVVPartialData

analysis_data_source = QVVPartialData.from_dict(json.load(open(DataPoint.data_12mpp_partial)))
print(type(analysis_data_source))
