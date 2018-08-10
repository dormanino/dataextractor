from PDS_Extractors.Models.BaumusterData import BaumusterData
from PDS_Extractors.Models.BaumusterDataKind import BaumusterDataKind
from PDS_Extractors.Models.Plant import Plant


class BaumusterCollection:
    def __init__(self, kind: BaumusterDataKind, plant: Plant, bm_data_list: [BaumusterData]):
        self.kind = kind
        self.plant = plant
        self.bm_data_list = bm_data_list

    @classmethod
    def from_dict(cls, datadict):
        return cls(
            BaumusterDataKind.from_str(datadict[BaumusterCollection.JSONKeys.kind]),
            Plant.from_str(datadict[BaumusterCollection.JSONKeys.plant]),
            list(map(BaumusterData.from_dict, datadict[BaumusterCollection.JSONKeys.bm_data_list]))
        )

    class JSONKeys:
        kind = "source"
        plant = "plant"
        bm_data_list = "data"
