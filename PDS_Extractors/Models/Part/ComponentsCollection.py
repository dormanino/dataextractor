from typing import List

from PDS_Extractors.Models.Part.ComponentParts import ComponentParts
from PDS_Extractors.Models.Plant import Plant


class ComponentsCollection:
    def __init__(self, plant: Plant, componment_parts_list: List[ComponentParts]):
        self.plant: Plant = plant
        self.component_parts_list: List[ComponentParts] = componment_parts_list

    @classmethod
    def from_dict(cls, datadict):
        return cls(
            Plant.from_str(datadict[ComponentsCollection.JSONKeys.plant]),
            list(map(ComponentParts.from_dict, datadict[ComponentsCollection.JSONKeys.componment_parts_list]))
        )

    class JSONKeys:
        plant = "plant"
        componment_parts_list = "data"
