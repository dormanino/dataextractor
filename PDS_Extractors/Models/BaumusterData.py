from PDS_Extractors.Models.Grouping import Grouping
from PDS_Extractors.Models.GroupingType import GroupingType


class BaumusterData:
    def __init__(self, bm: str, grouping_list: [Grouping]):
        self.bm = bm
        self.grouping_list = grouping_list

    @classmethod
    def from_dict(cls, datadict):
        return cls(
            datadict[BaumusterData.JSONKeys.bm],
            list(map(Grouping.from_dict, datadict[BaumusterData.JSONKeys.grouping_list]))
        )

    class JSONKeys:
        bm = "bm"
        grouping_list = "data"

    def extract_grouping(self, grouping_type: GroupingType):
        return next(filter(lambda x: x.type == grouping_type, self.grouping_list), None)
