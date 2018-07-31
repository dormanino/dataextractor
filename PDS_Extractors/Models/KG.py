from PDS_Extractors.Models.Register import Register


class KG:
    def __init__(self, name: str, reg_list: [Register]):
        self.name = name
        self.reg_list = reg_list

    @classmethod
    def from_dict(cls, datadict):
        return cls(
            datadict[KG.JSONKeys.name],
            list(map(Register.from_dict, datadict[KG.JSONKeys.reg_list]))
        )

    class JSONKeys:
        name = "kg"
        reg_list = "regs"
