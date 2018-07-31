from PDS_Extractors.Models.BaumusterData import BaumusterData
from PDS_Extractors.Models.BaumusterDataSource import BaumusterDataSource


class BaumusterCollection:
    def __init__(self, source: BaumusterDataSource, bm_data_list: [BaumusterData]):
        self.source = source
        self.bm_data_list = bm_data_list

    @classmethod
    def from_dict(cls, datadict):
        return cls(
            BaumusterDataSource.from_str(datadict[BaumusterCollection.JSONKeys.source]),
            list(map(BaumusterData.from_dict, datadict[BaumusterCollection.JSONKeys.bm_data_list]))
        )

    class JSONKeys:
        source = "source"
        bm_data_list = "data"
