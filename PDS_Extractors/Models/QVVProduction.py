from typing import List


class QVVProduction:

    def __init__(self, qvv: str, baumuster_id: str, business_unit: str,
                 family: str, volume: int, composition: List[str]):
        self.qvv: str = qvv
        self.baumuster_id: str = baumuster_id
        self.business_unit: str = business_unit
        self.family: str = family
        self.volume: int = volume
        self.composition: List[str] = composition

    @classmethod
    def from_dict(cls, datadict):
        return cls(
            datadict[QVVProduction.JSONKeys.qvv],
            datadict[QVVProduction.JSONKeys.baumuster_id],
            datadict[QVVProduction.JSONKeys.business_unit],
            datadict[QVVProduction.JSONKeys.family],
            datadict[QVVProduction.JSONKeys.volume],
            datadict[QVVProduction.JSONKeys.composition]
        )

    class JSONKeys:
        qvv = "qvv"
        baumuster_id = "bm"
        business_unit = "bu"
        family = "family"
        volume = "volume"
        composition = "composition"
