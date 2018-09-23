from typing import List

from BPM_STAR_Extractors.Models.QVVPartialSalesData import QVVPartialSalesData


class QVVPartialVariantData:
    def __init__(self, variant, variant_representation, volume_data):
        self.variant = variant
        self.variant_representation = variant_representation
        self.volume_data: List[QVVPartialSalesData] = volume_data

    @classmethod
    def from_dict(cls, datadict):
        return cls(
            datadict[QVVPartialVariantData.JSONKeys.variant],
            datadict[QVVPartialVariantData.JSONKeys.variant_representation],
            list(map(QVVPartialSalesData.from_dict, datadict[QVVPartialVariantData.JSONKeys.volume_data]))
        )

    class JSONKeys:
        variant = "variant"
        variant_representation = "variant_representation"
        volume_data = "volume_data"

    def total_volume(self) -> int:
        return sum(sd.total_volume for sd in self.volume_data)