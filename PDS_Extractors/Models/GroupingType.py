from enum import Enum


class GroupingType(Enum):
    SAA = "SAA"
    LEG = "LEG"
    Code = "Code"
    General = "General"
    Aggregate = "Aggregate"

    @staticmethod
    def from_str(label):
        kinds = [GroupingType.SAA,
                 GroupingType.LEG,
                 GroupingType.Code,
                 GroupingType.General,
                 GroupingType.Aggregate]
        for kind in kinds:
            if label in kind.value:
                return kind
        raise NotImplementedError
