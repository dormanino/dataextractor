from typing import List

from PDS_Extractors.Models.Part.ComponentParts import ComponentParts
from PDS_Extractors.Models.Plant import Plant


class ComponentsCollection:
    def __init__(self, plant: Plant, component_parts_list: List[ComponentParts]):
        self.plant: Plant = plant
        self.component_parts_list: List[ComponentParts] = component_parts_list

    @classmethod
    def from_dict(cls, datadict):
        return cls(
            Plant.from_str(datadict[ComponentsCollection.JSONKeys.plant]),
            list(map(ComponentParts.from_dict, datadict[ComponentsCollection.JSONKeys.component_parts_list]))
        )

    class JSONKeys:
        plant = "plant"
        component_parts_list = "data"

    def __eq__(self, other):
        return self.plant == other.plant

    def __hash__(self):
        return hash(self.plant.name)
