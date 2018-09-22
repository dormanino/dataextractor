from BPM_STAR_Extractors.Models.QVVPartialVariantData import QVVPartialVariantData


class QVVPartialMainData:

    def __init__(self, extraction_date, header, main_option, periodicity,
                 ref_date, resume_type, variant_data):
        self.extraction_date = extraction_date
        self.header = header
        self.main_option = main_option
        self.periodicity = periodicity
        self.ref_date = ref_date
        self.resume_type = resume_type
        self.variant_data = variant_data

    @classmethod
    def from_dict(cls, datadict):
        return cls(
            datadict[QVVPartialMainData.JSONKeys.extraction_date],
            datadict[QVVPartialMainData.JSONKeys.header],
            datadict[QVVPartialMainData.JSONKeys.main_option],
            datadict[QVVPartialMainData.JSONKeys.periodicity],
            datadict[QVVPartialMainData.JSONKeys.ref_date],
            datadict[QVVPartialMainData.JSONKeys.resume_type],
            list(map(QVVPartialVariantData.from_dict, datadict[QVVPartialMainData.JSONKeys.variant_data]))
        )

    class JSONKeys:
        extraction_date = "extraction_date"
        header = "header"
        main_option = "main_option"
        periodicity = "periodicity"
        ref_date = "ref_date"
        resume_type = "resume_type"
        variant_data = "variant_data"
