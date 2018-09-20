class QVVPartialVolumeData:

    def __init__(self, months, year):
        self.months = months
        self.year = year

    @classmethod
    def from_dict(cls, datadict):
        return cls(
            datadict[QVVPartialVolumeData.JSONKeys.months],
            datadict[QVVPartialVolumeData.JSONKeys.year]
        )

    class JSONKeys:
        months = "months"
        year = "year"
