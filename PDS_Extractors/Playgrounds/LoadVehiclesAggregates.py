import json
from PDS_Extractors.Data.DataPoint import DataPoint
from PDS_Extractors.Models.BaumusterCollection import BaumusterCollection
from PDS_Extractors.Models.BaumusterDataSource import BaumusterDataSource

vehicles_data = json.load(open(DataPoint.data_agrmz_vehicles))
aggregates_data = json.load(open(DataPoint.data_agrmz_aggregates))
baumuster_collection = BaumusterCollection.from_dict(aggregates_data)

if baumuster_collection.source == BaumusterDataSource.Vehicle:
    print("Colecao de veiculo")
else:
    print("Colecao de agregados")
