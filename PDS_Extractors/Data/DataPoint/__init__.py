import Settings
from PDS_Extractors.Helpers.LatestFileVersion import LatestFileVersion


class DataPoint:
    path = Settings.PROJECT_DATA_FILES

    data_0e = LatestFileVersion.latest_file_version('json', '_PDS_0E', current=path)
    data_acc = LatestFileVersion.latest_file_version('json', '_PDS_ACC', current=path)

    data_02 = LatestFileVersion.latest_file_version('json', '_PDS_02', current=path)
    data_kgs_agr_vehicles = LatestFileVersion.latest_file_version('json', '_PDS_KGS_AGR_Vehicles', current=path)
    data_agrmz_raw_vehicles = LatestFileVersion.latest_file_version('json', '_PDS_BM´s_AGRMZ_Vehicles', current=path)
    data_agrmz_vehicles = LatestFileVersion.latest_file_version('json', '_PDS_AGRMZ_parsed_final_Vehicles', current=path)

    data_03 = LatestFileVersion.latest_file_version('json', '_PDS_03', current=path)
    data_kgs_agr_aggregates = LatestFileVersion.latest_file_version('json', '_PDS_KGS_AGR_Aggregates', current=path)
    data_agrmz_raw_aggregates = LatestFileVersion.latest_file_version('json', '_PDS_BM´s_AGRMZ_Aggregates', current=path)
    data_agrmz_aggregates = LatestFileVersion.latest_file_version('json', '_PDS_KGS_AGR_final_Aggregates', current=path)
