from typing import List, Dict
from PDS_Extractors.Models.QVV.QVVProduction import QVVProduction


class MonthlyProduction:
    def __init__(self, month: int, year: int, qvv_production_list: List[QVVProduction]):
        self.month: int = month
        self.year: int = year
        self.qvv_production_list: List[QVVProduction] = qvv_production_list

    @classmethod
    def from_dict(cls, datadict):
        return cls(
            datadict[MonthlyProduction.JSONKeys.month],
            datadict[MonthlyProduction.JSONKeys.year],
            list(map(QVVProduction.from_dict, datadict[MonthlyProduction.JSONKeys.qvv_production_list]))
        )

    class JSONKeys:
        month = "month"
        year = "year"
        qvv_production_list = "data"

    def total_volume(self) -> int:
        return sum(qvv_production.volume for qvv_production in self.qvv_production_list)

    def volume_by_family(self) -> Dict[str, int]:
        families = dict()
        for qvv_production in self.qvv_production_list:
            key = qvv_production.family
            if key in families.keys():
                families[key] += qvv_production.volume
            else:
                families[key] = qvv_production.volume
        return families
