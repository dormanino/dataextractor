import os
import LatestFileVersion


class DataPoint:

    path = 'C:\\Users\\vravagn\\PycharmProjects\\DataExtractor\\PDS_Extractors'
    current_working_directory = os.getcwd()
    data_agrmz = LatestFileVersion.latest_file_version('json', 'PDS_KGS_AGR_final', current=path)
    data_0e = LatestFileVersion.latest_file_version('json', '_PDS_0E', current=path)
    data_acc = LatestFileVersion.latest_file_version('json', '_PDS_ACC', current=path)
