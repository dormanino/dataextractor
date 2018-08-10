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
    SUFFIX_data_vehicle = str(BaumusterDataKind.Vehicle.value) + SUFFIX_data_agrmz
    SUFFIX_data_aggregate = str(BaumusterDataKind.Aggregate.value) + SUFFIX_data_agrmz

    # Final Data Points
    production = LatestFileVersion.latest_file_version(EXT_json, 'dictionary_qvvs_by_month', current=PATH_DataFiles)
    data_vehicles_sbc = LatestFileVersion.latest_file_version(EXT_json, SUFFIX_sbc + SUFFIX_data_vehicle, current=PATH_DataFiles)
    data_aggregates_sbc = LatestFileVersion.latest_file_version(EXT_json, SUFFIX_sbc + SUFFIX_data_aggregate, current=PATH_DataFiles)
    data_vehicles_jdf = LatestFileVersion.latest_file_version(EXT_json, SUFFIX_jdf + SUFFIX_data_vehicle, current=PATH_DataFiles)
    data_aggregates_jdf = LatestFileVersion.latest_file_version(EXT_json, SUFFIX_jdf + SUFFIX_data_aggregate, current=PATH_DataFiles)

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
