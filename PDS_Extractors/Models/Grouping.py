from PDS_Extractors.Models.GroupingType import GroupingType
from PDS_Extractors.Models.KG import KG


class Grouping:
    def __init__(self, type: GroupingType, kg_list: [KG]):
        self.type = type
        self.kg_list = kg_list

    @classmethod
    def from_dict(cls, datadict):
        return cls(
            GroupingType.from_str(datadict[Grouping.JSONKeys.type]),
            list(map(KG.from_dict, datadict[Grouping.JSONKeys.kg_list]))
        )

    class JSONKeys:
        type = "type"
        kg_list = "data"

    def flattened_registers(self):
        registers = []
        for register_list in map(lambda x: x.reg_list, self.kg_list):
            registers.extend(register_list)
        return registers
