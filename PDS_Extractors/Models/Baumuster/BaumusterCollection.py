from typing import List
from PDS_Extractors.Models.Baumuster.BaumusterData import BaumusterData
from PDS_Extractors.Models.Baumuster.BaumusterDataKind import BaumusterDataKind
from PDS_Extractors.Models.Plant import Plant


class BaumusterCollection:
    def __init__(self, kind: int, plant: Plant, bm_data_list: List[BaumusterData]):
        self.kind: BaumusterDataKind = kind
        self.plant: Plant = plant
        self.bm_data_list: List[BaumusterData] = bm_data_list

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
