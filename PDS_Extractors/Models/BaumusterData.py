from PDS_Extractors.Models.IDK import IDK
from PDS_Extractors.Models.IDKKind import IDKKind


class BaumusterData:
    def __init__(self, bm: str, idk_list: [IDK]):
        self.bm = bm
        self.idk_list = idk_list

    @classmethod
    def from_dict(cls, datadict):
        return cls(
            datadict[BaumusterData.JSONKeys.bm],
            list(map(IDK.from_dict, datadict[BaumusterData.JSONKeys.idk_list]))
        )

    class JSONKeys:
        bm = "bm"
        idk_list = "data"

    def extract_idk(self, idk: IDKKind):
        return next(filter(lambda x: x.kind == idk, self.idk_list), None)
