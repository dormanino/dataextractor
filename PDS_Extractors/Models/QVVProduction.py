class QVVProduction:
    
    def __init__(self, qvv: str, bm: str, bu: str, family: str, volume: int, composition: [str]):
        self.qvv = qvv
        self.bm = bm
        self.bu = bu
        self.family = family
        self.volume = volume
        self.composition = composition
        
    @classmethod
    def from_dict(cls, datadict):
        return cls(
            datadict[QVVProduction.JSONKeys.qvv],
            datadict[QVVProduction.JSONKeys.bm],
            datadict[QVVProduction.JSONKeys.bu],
            datadict[QVVProduction.JSONKeys.family],
            datadict[QVVProduction.JSONKeys.volume],
            datadict[QVVProduction.JSONKeys.composition]
        )

    class JSONKeys:
        qvv = "qvv"
        bm = "bm"
        bu = "bu"
        family = "family"
        volume = "volume"
        composition = "composition"
