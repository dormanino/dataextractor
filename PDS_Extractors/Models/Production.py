import datetime
from collections import Counter
from typing import List, Dict
from PDS_Extractors.Models.MonthlyProduction import MonthlyProduction


class Production:
    def __init__(self, year: int, monthly_production_list: List[MonthlyProduction]):
        self.year: int = year
        self.monthly_production_list: List[MonthlyProduction] = monthly_production_list

    @classmethod
    def from_dict(cls, datadict):
        monthly_production = list(map(MonthlyProduction.from_dict, datadict[Production.JSONKeys.monthly_production_list]))
        return cls(
            datadict.get(Production.JSONKeys.year, datetime.datetime.now().year),  # fallback to current year
            list(filter(lambda mp: mp.month != 'total', monthly_production))  # ignore 'total' month_year
        )

    class JSONKeys:
        year = "year"
        monthly_production_list = "production"

    def total_volume(self) -> int:
        return sum(mp.total_volume() for mp in self.monthly_production_list)

    def volume_by_family(self) -> Dict[str, int]:
        monthly_family_volumes = map(lambda mp: mp.volume_by_family(), self.monthly_production_list)
        volume_by_family = dict()
        for monthly_family_volume in monthly_family_volumes:
            volume_by_family = Counter(volume_by_family) + Counter(monthly_family_volume)
        return volume_by_family
