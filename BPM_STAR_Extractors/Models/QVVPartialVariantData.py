from BPM_STAR_Extractors.Models.QVVPartialMainData import QVVPartialMainData


class QVVPartialVariantData:
    def __init__(self, variant, variant_representation, volume_data):
        self.variant = variant
        self.variant_representation = variant_representation
        self.volume_data = volume_data

    @classmethod
    def from_dict(cls, datadict):
        return cls(
            list(map(QVVPartialMainData.from_dict, datadict[QVVPartialVariantData.JSONKeys.variant_data])),
            datadict[QVVPartialVariantData.JSONKeys.variant],
            datadict[QVVPartialVariantData.JSONKeys.variant_representation]
        )

    class JSONKeys:
        variant = "variant"
        variant_representation = "variant_representation"
        variant_data = "variant_data"
