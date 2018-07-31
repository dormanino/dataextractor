from enum import Enum


class IDKKind(Enum):
    SAA = "SAA"
    LEG = "LEG"
    Code = "Code"
    General = "General"
    Aggregate = "Aggregate"

    @staticmethod
    def from_str(label):
        kinds = [IDKKind.SAA,
                 IDKKind.LEG,
                 IDKKind.Code,
                 IDKKind.General,
                 IDKKind.Aggregate]
        for kind in kinds:
            if label in kind.value:
                return kind
        raise NotImplementedError
