from PDS_Extractors.Models.GroupingType import GroupingType


class Component:
    def __init__(self, component_id: str, component_description: str, bg: str, grouping_type: GroupingType, kg: str, validation_rule: str,
                 em_ab, em_bis, t_a, t_b, anz, asa, asb, pos):
        self.component_id: str = component_id
        self.clean_component_id: str = Component.clean_component_id(component_id)
        self.component_description: str = component_description
        self.bg = bg
        self.grouping_type: GroupingType = grouping_type
        self.kg: str = kg
        self.validation_rule: str = validation_rule
        self.em_ab = em_ab
        self.em_bis = em_bis
        self.t_a = t_a
        self.t_b = t_b
        self.anz = anz
        self.asa = asa
        self.asb = asb
        self.pos = pos

    @classmethod
    def from_dict(cls, datadict):
        return cls(
            datadict[Component.JSONKeys.component_id],
            datadict.get(Component.JSONKeys.component_description, "(No Description)"),
            datadict.get(Component.JSONKeys.bg, None),
            datadict[Component.JSONKeys.grouping_type],
            datadict[Component.JSONKeys.kg],
            datadict.get(Component.JSONKeys.validation_rule, None),
            datadict[Component.JSONKeys.em_ab],
            datadict[Component.JSONKeys.em_bis],
            datadict[Component.JSONKeys.t_a],
            datadict[Component.JSONKeys.t_b],
            datadict.get(Component.JSONKeys.anz, None),
            datadict[Component.JSONKeys.asa],
            datadict[Component.JSONKeys.asb],
            datadict[Component.JSONKeys.pos]
        )

    class JSONKeys:
        component_id = "abm_saa"
        component_description = "benennung"
        bg = "bg_codebedingungen"
        grouping_type = "grouping_type"
        kg = "kg"
        validation_rule = "CODEBEDINGUNGEN"
        em_ab = "em_ab"  # aviso de aplicacao a partir de
        em_bis = "em_bis"  # aviso de aplicacao ate
        t_a = "t_a"  # prazo a partir de
        t_b = "t_b"  # prazo ate
        anz = "anz"
        asa = "asa"
        asb = "asb"
        pos = "pos"

    @staticmethod
    def clean_component_id(component_id: str) -> str:
        clean = component_id
        for char in [' ', '.', '/', ',']:
            clean = clean.replace(char, "")
        return clean
