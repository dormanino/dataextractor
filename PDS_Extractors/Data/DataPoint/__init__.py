import os
import LatestFileVersion


class DataPoint:

    path = 'C:\\Users\\vravagn\\PycharmProjects\\dataextractor\\PDS_Extractors'
    current_working_directory = os.getcwd()

    data_0e = LatestFileVersion.latest_file_version('json', '_PDS_0E', current=path)
    data_acc = LatestFileVersion.latest_file_version('json', '_PDS_ACC', current=path)
    data_02 = LatestFileVersion.latest_file_version('json', '_PDS_02', current=path)
    data_03 = LatestFileVersion.latest_file_version('json', '_PDS_03', current=path)
    data_kgs_agr = LatestFileVersion.latest_file_version('json', '_PDS_KGS_AGR', current=path)
    data_kgs_agr_aggregates = LatestFileVersion.latest_file_version('json', '_PDS_KGS_AGR_Aggregates', current=path)
    data_agrmz_raw = LatestFileVersion.latest_file_version('json', '_PDS_BM´s_AGRMZ', current=path)
    data_agrmz = LatestFileVersion.latest_file_version('json', '_PDS_KGS_AGR_final', current=path)
