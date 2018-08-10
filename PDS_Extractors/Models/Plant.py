from enum import Enum


class Plant(Enum):
    SBC = "sbc"
    JDF = "jdf"

    @staticmethod
    def from_str(label):
        sources = [Plant.SBC,
                   Plant.JDF]
        for source in sources:
            if label in source.value:
                return source
        raise NotImplementedError
