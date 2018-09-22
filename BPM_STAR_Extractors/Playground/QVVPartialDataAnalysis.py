import json
from BPM_STAR_Extractors.Models.QVVPartialVolumeData import QVVPartialVolumeData
from BPM_STAR_Extractors.Models.QVVPartialSalesData import QVVPartialSalesData
from BPM_STAR_Extractors.Models.QVVPartialVariantData import QVVPartialVariantData
from BPM_STAR_Extractors.Models.QVVPartialMainData import QVVPartialMainData
from BPM_STAR_Extractors.DataPoint import DataPoint

data = json.load(open(DataPoint.data_12mpp_partial))
data_for_analisys = QVVPartialVolumeData.from_dict(data)

