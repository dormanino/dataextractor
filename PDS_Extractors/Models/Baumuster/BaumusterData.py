from typing import List

from PDS_Extractors.Models.Component.Component import Component
from PDS_Extractors.Models.Component.ComponentGroupingType import ComponentGroupingType


class BaumusterData:
    def __init__(self, baumuster_id: str, components_list: List[Component]):
        self.baumuster_id: str = baumuster_id
        self.components_list: List[Component] = components_list

    @classmethod
    def from_dict(cls, datadict):

        # Flatten Grouping and KG data from json into Component
        components_list = []
        for grouping_dict in datadict[BaumusterData.JSONKeys.bm_grouping_list]:
            grouping_type = ComponentGroupingType.from_str(grouping_dict[BaumusterData.JSONKeys.grouping_type])
            for kg_dict in grouping_dict[BaumusterData.JSONKeys.grouping_kg_list]:
                kg = kg_dict[BaumusterData.JSONKeys.kg_name]
                for reg_dict in kg_dict[BaumusterData.JSONKeys.kg_reg_list]:
                    reg_dict[Component.JSONKeys.grouping_type] = grouping_type
                    reg_dict[Component.JSONKeys.kg] = kg.strip()
                    components_list.append(Component.from_dict(reg_dict))

        return cls(
            datadict[BaumusterData.JSONKeys.baumuster_id],
            components_list
        )

    class JSONKeys:
        baumuster_id = "bm"
        bm_grouping_list = "data"
        grouping_type = "type"
        grouping_kg_list = "data"
        kg_name = "kg"
        kg_reg_list = "regs"

    def extract_grouping(self, grouping_type: ComponentGroupingType) -> List[Component]:
        return list(filter(lambda component: component.grouping_type == grouping_type, self.components_list))
