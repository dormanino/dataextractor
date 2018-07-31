from enum import Enum


class BaumusterDataSource(Enum):
    Vehicle = "vehicle"
    Aggregate = "aggregate"

    @staticmethod
    def from_str(label):
        sources = [BaumusterDataSource.Vehicle,
                   BaumusterDataSource.Aggregate]
        for source in sources:
            if label in source.value:
                return source
        raise NotImplementedError
