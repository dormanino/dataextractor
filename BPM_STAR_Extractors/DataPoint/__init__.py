import Settings
from PDS_Extractors.Helpers.LatestFileVersion import LatestFileVersion


class DataPoint:
    # Paths
    PATH_DataFiles = Settings.PROJECT_DATA_FILES

    # Extensions
    EXT_json = "json"

    data_variant_final_data = LatestFileVersion.latest_file_version(EXT_json, '_final_variant_data', PATH_DataFiles)
    data_info_bm = PATH_DataFiles + '\\bm_info.json'
    data_12mpp = LatestFileVersion.latest_file_version(EXT_json, '_12mpp_raw', PATH_DataFiles)
    data_12mpp_parsed = LatestFileVersion.latest_file_version(EXT_json, '_12mpp_parsed', PATH_DataFiles)
    data_qvv_bm_vol = LatestFileVersion.latest_file_version(EXT_json, '_qvv_bmvol', PATH_DataFiles)
    data_bm_tot = LatestFileVersion.latest_file_version(EXT_json, '_bmvol_tot', PATH_DataFiles)
    data_final_dict = LatestFileVersion.latest_file_version(EXT_json, '_dict_end', PATH_DataFiles)
    data_12mpp_partial = LatestFileVersion.latest_file_version(EXT_json, '_partials_operation', PATH_DataFiles)
