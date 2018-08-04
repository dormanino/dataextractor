import datetime
import json
from PDS_Extractors.Data.DataPoint import DataPoint

date = datetime.date.today()
date_string = date.strftime('%y%m%d')

vehicle_sbc_json_file = json.load(open(DataPoint.data_agrmz_raw_vehicles_sbc))
vehicle_jdf_json_file = json.load(open(DataPoint.data_agrmz_raw_vehicles_jdf))

data_agr = vehicle_sbc_json_file + vehicle_jdf_json_file

with open(DataPoint.PATH_DataFiles + '\\' + date_string + '_main_vehicle_PDS_agrmz.json', 'w+') as f:
    json.dump(data_agr, f, indent=4, sort_keys=True, ensure_ascii=False)
