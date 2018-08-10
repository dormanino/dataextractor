from enum import Enum


class BaumusterDataKind(Enum):
    Vehicle = "vehicle"
    Aggregate = "aggregate"

    @staticmethod
    def from_str(label):
        sources = [BaumusterDataKind.Vehicle,
                   BaumusterDataKind.Aggregate]
        for source in sources:
            if label in source.value:
                return source
        raise NotImplementedError
