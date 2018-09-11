from BPM_STAR_Extractors.Models.QVVPartialSalesData import QVVPartialSalesData


class QVVPartialVolumeData:

    def __init__(self, months, year, qvv_partial_volume_data):
        self.months = months
        self.year = year
        self.qvv_partial_volume_data = qvv_partial_volume_data

    @classmethod
    def from_dict(cls, datadict):
        info = list(map(QVVPartialSalesData.from_dict, datadict[QVVPartialVolumeData.JSONKeys.qvv_partial_volume_data]))
        return cls(
            datadict.get(list(map(info, datadict[QVVPartialVolumeData.JSONKeys.months]))),
            list(map(info, datadict[QVVPartialVolumeData.JSONKeys.year]))
        )

    class JSONKeys:
        months = "months"
        year = "year"
        qvv_partial_volume_data = "data"
