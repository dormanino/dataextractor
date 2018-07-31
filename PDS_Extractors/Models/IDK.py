from functools import reduce

from PDS_Extractors.Models.IDKKind import IDKKind
from PDS_Extractors.Models.KG import KG


class IDK:
    def __init__(self, kind: IDKKind, kg_list: [KG]):
        self.kind = kind
        self.kg_list = kg_list

    @classmethod
    def from_dict(cls, datadict):
        return cls(
            IDKKind.from_str(datadict[IDK.JSONKeys.kind]),
            list(map(KG.from_dict, datadict[IDK.JSONKeys.kg_list]))
        )

    class JSONKeys:
        kind = "type"
        kg_list = "data"

    def flattened_registers(self):
        registers = []
        for register_list in map(lambda x: x.reg_list, self.kg_list):
            registers.extend(register_list)
        return registers
