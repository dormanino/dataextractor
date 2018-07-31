from PDS_Extractors.Models.QVVProduction import QVVProduction


class MonthlyProduction:
    def __init__(self, month: str, qvv_production_list: [QVVProduction]):
        self.month = month
        self.qvv_production_list = qvv_production_list

    @classmethod
    def from_dict(cls, datadict):
        return cls(
            datadict[MonthlyProduction.JSONKeys.month],
            list(map(QVVProduction.from_dict, datadict[MonthlyProduction.JSONKeys.qvv_production_list]))
        )

    class JSONKeys:
        month = "month"
        qvv_production_list = "data"

    def total_volume(self) -> int:
        return sum(qvv_production.volume for qvv_production in self.qvv_production_list)

    def volume_by_family(self):
        families = dict()
        for qvv_production in self.qvv_production_list:
            key = qvv_production.family
            if key in families.keys():
                families[key] += qvv_production.volume
            else:
                families[key] = qvv_production.volume
        return families
