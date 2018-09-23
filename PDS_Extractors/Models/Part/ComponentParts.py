from typing import List

from PDS_Extractors.Models.Part.Part import Part


class ComponentParts:
    def __init__(self, component_id: str, parts_list: List[Part]):
        self.component_id: str = component_id
        self.parts_list: List[Part] = parts_list

    @classmethod
    def from_dict(cls, datadict):
        parts_list = []
        for part_dict in datadict[ComponentParts.JSONKeys.parts_list]:
            if part_dict is not None:  # ignore 'null' inside parts list
                parts_list.append(Part.from_dict(part_dict))

        return cls(
            datadict[ComponentParts.JSONKeys.component],
            parts_list
        )

    class JSONKeys:
        component = "source"
        parts_list = "regs"
