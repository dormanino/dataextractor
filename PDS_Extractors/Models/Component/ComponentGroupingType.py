from enum import Enum


class ComponentGroupingType(Enum):
    SAA = "SAA"
    LEG = "LEG"
    Code = "Code"
    General = "General"
    Aggregate = "Aggregate"

    @staticmethod
    def from_str(label: str):
        kinds = [ComponentGroupingType.SAA,
                 ComponentGroupingType.LEG,
                 ComponentGroupingType.Code,
                 ComponentGroupingType.General,
                 ComponentGroupingType.Aggregate]
        for kind in kinds:
            if label in kind.value:
                return kind
        raise NotImplementedError
