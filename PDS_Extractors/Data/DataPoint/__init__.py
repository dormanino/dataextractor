import Settings
from PDS_Extractors.Helpers.LatestFileVersion import LatestFileVersion
from PDS_Extractors.Models.BaumusterDataSource import BaumusterDataSource


class DataPoint:
    # PATHS
    PATH_DataFiles = Settings.PROJECT_DATA_FILES

    # Extensions
    EXTENSION_json = "json"

    # Suffixes
    SUFFIX_data_agrmz = "_PDS_AGRMZ_parsed_final_"
    SUFFIX_data_agrmz_vehicle = SUFFIX_data_agrmz + str(BaumusterDataSource.Vehicle.value)
    SUFFIX_data_agrmz_aggregate = SUFFIX_data_agrmz + str(BaumusterDataSource.Aggregate.value)

    # Data Points
    data_0e = LatestFileVersion.latest_file_version(EXTENSION_json, '_PDS_0E', current=PATH_DataFiles)
    data_acc = LatestFileVersion.latest_file_version(EXTENSION_json, '_PDS_ACC', current=PATH_DataFiles)

    data_02 = LatestFileVersion.latest_file_version(EXTENSION_json, '_PDS_02', current=PATH_DataFiles)
    data_kgs_agr_vehicles = LatestFileVersion.latest_file_version(EXTENSION_json, '_PDS_KGS_AGR_Vehicles', current=PATH_DataFiles)
    data_agrmz_raw_vehicles = LatestFileVersion.latest_file_version(EXTENSION_json, '_PDS_BM´s_AGRMZ_Vehicles', current=PATH_DataFiles)
    data_agrmz_vehicles = LatestFileVersion.latest_file_version(EXTENSION_json, SUFFIX_data_agrmz_vehicle, current=PATH_DataFiles)

    data_03 = LatestFileVersion.latest_file_version(EXTENSION_json, '_PDS_03', current=PATH_DataFiles)
    data_kgs_agr_aggregates = LatestFileVersion.latest_file_version(EXTENSION_json, '_PDS_KGS_AGR_Aggregates', current=PATH_DataFiles)
    data_agrmz_raw_aggregates = LatestFileVersion.latest_file_version(EXTENSION_json, '_PDS_BM´s_AGRMZ_Aggregates', current=PATH_DataFiles)
    data_agrmz_aggregates = LatestFileVersion.latest_file_version(EXTENSION_json, SUFFIX_data_agrmz_aggregate, current=PATH_DataFiles)

    production = LatestFileVersion.latest_file_version(EXTENSION_json, 'dictionary_qvvs_by_month', current=PATH_DataFiles)
