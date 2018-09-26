from PDS_Extractors.Models.Component.ComponentGroupingType import ComponentGroupingType


class Component:
    def __init__(self, component_id: str, component_description: str, baumuster_id: str,
                 bg: str, grouping_type: ComponentGroupingType, kg: str, validation_rule: str,
                 em_ab, em_bis, t_a, t_b, anz, asa, asb, pos):
        self.component_id: str = component_id
        self.clean_component_id: str = Component.clean_component_id(component_id)
        self.component_description: str = component_description
        self.baumuster_id: str = baumuster_id
        self.bg = bg
        self.grouping_type: ComponentGroupingType = grouping_type
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
            datadict[Component.JSONKeys.baumuster_id],
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
        component_description = "part_description"
        baumuster_id = "baumuster_id"
        bg = "bg_codebedingungen"
        grouping_type = "grouping_type"
        kg = "kg"
        validation_rule = "codebedingungen"
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

    def __eq__(self, other):
        return self.component_id == other.component_id \
               and self.baumuster_id == other.baumuster_id \
               and self.kg == other.kg \
               and self.pos == other.pos \
               and self.asa == other.asa \
               and self.asb == other.asb \
               and self.em_ab == other.em_ab \
               and self.em_bis == other.em_bis

    def __hash__(self):
        return hash((
            self.component_id,
            self.baumuster_id,
            self.kg,
            self.pos,
            self.asa,
            self.asb,
            self.em_ab,
            self.em_bis
        ))
