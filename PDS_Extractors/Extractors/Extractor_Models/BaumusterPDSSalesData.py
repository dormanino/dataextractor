import typing
from PDS_Extractors.Models.Component import ComponentGroupingType


class BaumusterPDSSalesData:
    def __init__(self, baumuster: str, benennung: str, verkaufbezeichnung: str, tieferverkaufbezeichnung: typing.List, family: str,
                 bg: str, grouping_type: ComponentGroupingType, kg: str, validation_rule: str,
                 em_ab, em_bis, t_a, t_b, anz, asa, asb, pos):

        self.baumuster: str = baumuster
        self.benennung: str = benennung
        self.verkaufbezeichnung: str = verkaufbezeichnung
        self.tieferverkaufbezeichnung: str = tieferverkaufbezeichnung
        self.family = family
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
