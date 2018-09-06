import Settings
from PDS_Extractors.Helpers.LatestFileVersion import LatestFileVersion
from PDS_Extractors.Models.BaumusterDataKind import BaumusterDataKind


class DataPoint:
    # Paths
    PATH_DataFiles = Settings.PROJECT_DATA_FILES

    # Extensions
    EXT_json = "json"

    # Suffixes
    SUFFIX_sbc = "_sbc_"
    SUFFIX_jdf = "_jdf_"
    SUFFIX_data_agrmz = "_PDS_AGRMZ_parsed_final"
    SUFFIX_data_parts_raw = "PDS_3CA"
    SUFFIX_data_parts = '3ca_parsed_final'
    SUFFIX_data_vehicles = str(BaumusterDataKind.Vehicle.value) + SUFFIX_data_agrmz
    SUFFIX_data_aggregates = str(BaumusterDataKind.Aggregate.value) + SUFFIX_data_agrmz

    # Final Data Points
    production = LatestFileVersion.latest_file_version(EXT_json, '_dictionary_qvvs_by_month', current=PATH_DataFiles)
    data_sbc_vehicles = LatestFileVersion.latest_file_version(EXT_json, SUFFIX_sbc + SUFFIX_data_vehicles, current=PATH_DataFiles)
    data_jdf_vehicles = LatestFileVersion.latest_file_version(EXT_json, SUFFIX_jdf + SUFFIX_data_vehicles, current=PATH_DataFiles)
    data_sbc_aggregates = LatestFileVersion.latest_file_version(EXT_json, SUFFIX_sbc + SUFFIX_data_aggregates, current=PATH_DataFiles)
    data_jdf_aggregates = LatestFileVersion.latest_file_version(EXT_json, SUFFIX_jdf + SUFFIX_data_aggregates, current=PATH_DataFiles)
    data_sbc_parts = LatestFileVersion.latest_file_version(EXT_json, SUFFIX_sbc + SUFFIX_data_parts, current=PATH_DataFiles)
    data_jdf_parts = LatestFileVersion.latest_file_version(EXT_json, SUFFIX_jdf + SUFFIX_data_parts, current=PATH_DataFiles)

    # Middle Data Points
    data_0e = LatestFileVersion.latest_file_version(EXT_json, '_PDS_0E', current=PATH_DataFiles)
    data_acc = LatestFileVersion.latest_file_version(EXT_json, '_PDS_ACC', current=PATH_DataFiles)

    data_02_sbc = LatestFileVersion.latest_file_version(EXT_json, '_sbc_PDS_02', current=PATH_DataFiles)
    data_02_jdf = LatestFileVersion.latest_file_version(EXT_json, '_jdf_PDS_02', current=PATH_DataFiles)
    data_kgs_agr_vehicles_sbc = LatestFileVersion.latest_file_version(EXT_json, '_sbc_vehicle_PDS_kgs', current=PATH_DataFiles)
    data_kgs_agr_vehicles_jdf = LatestFileVersion.latest_file_version(EXT_json, '_jdf_vehicle_PDS_kgs', current=PATH_DataFiles)
    data_agrmz_raw_vehicles_sbc = LatestFileVersion.latest_file_version(EXT_json, '_sbc_vehicle_PDS_agrmz', current=PATH_DataFiles)
    data_agrmz_raw_vehicles_jdf = LatestFileVersion.latest_file_version(EXT_json, '_jdf_vehicle_PDS_agrmz', current=PATH_DataFiles)

    data_03_sbc = LatestFileVersion.latest_file_version(EXT_json, '_sbc_PDS_03', current=PATH_DataFiles)
    data_03_jdf = LatestFileVersion.latest_file_version(EXT_json, '_jdf_PDS_03', current=PATH_DataFiles)
    data_kgs_agr_aggregates_sbc = LatestFileVersion.latest_file_version(EXT_json, '_sbc_aggregate_PDS_kgs', current=PATH_DataFiles)
    data_kgs_agr_aggregates_jdf = LatestFileVersion.latest_file_version(EXT_json, '_jdf_aggregate_PDS_kgs', current=PATH_DataFiles)
    data_agrmz_raw_aggregates_sbc = LatestFileVersion.latest_file_version(EXT_json, '_sbc_aggregate_PDS_agrmz', current=PATH_DataFiles)
    data_agrmz_raw_aggregates_jdf = LatestFileVersion.latest_file_version(EXT_json, '_jdf_aggregate_PDS_agrmz', current=PATH_DataFiles)
    data_saa = str(PATH_DataFiles + '\\SAA_SET.csv')
    data_3ca_raw_sbc = LatestFileVersion.latest_file_version(EXT_json, SUFFIX_sbc + SUFFIX_data_parts_raw, current=PATH_DataFiles)
    data_3ca_raw_jdf = LatestFileVersion.latest_file_version(EXT_json, SUFFIX_jdf + SUFFIX_data_parts_raw, current=PATH_DataFiles)
    data_3ca_sbc = LatestFileVersion.latest_file_version(EXT_json, SUFFIX_sbc + SUFFIX_data_parts, current=PATH_DataFiles)
    data_3ca_jdf = LatestFileVersion.latest_file_version(EXT_json, SUFFIX_jdf + SUFFIX_data_parts, current=PATH_DataFiles)
