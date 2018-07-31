import json
import Settings
from PDS_Extractors.Helpers.LatestFileVersion import LatestFileVersion
from PDS_Extractors.Models.Production import Production

path = Settings.PROJECT_DATA_FILES
file = LatestFileVersion.latest_file_version('json', 'dictionary_qvvs_by_month', current=path)
data = json.load(open(file))

production = Production.from_dict(data)
# print("VOLUME TOTAL: " + str(production.total_volume() / 2))
for family, volume in production.volume_by_family().items():
    print(family, volume)
