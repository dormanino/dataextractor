import os
import LatestFileVersion


class DataPoint:

    current_working_directory = os.getcwd()
    data_12mpp = LatestFileVersion.latest_file_version('json', '12mpp_raw', current=current_working_directory + '\\DataPoint')
    data_b3902v = LatestFileVersion.latest_file_version('json', '_final_variant_data', current=current_working_directory + '\\DataPoint')
    data_12mpp_parsed = LatestFileVersion.latest_file_version('json', '12mpp_parsed', current=current_working_directory + '\\DataPoint')
    data_qvv_bm_vol = LatestFileVersion.latest_file_version('json', 'qvv_bmvol', current=current_working_directory + '\\DataPoint')
    data_bm_tot = LatestFileVersion.latest_file_version('json', 'bmvol_tot', current=current_working_directory + '\\DataPoint')
    data_info_bm = os.getcwd() + '\\DataPoint\\bm_info.json'
    data_mashed = LatestFileVersion.latest_file_version('json', 'dict_end', current=current_working_directory + '\\DataPoint')
