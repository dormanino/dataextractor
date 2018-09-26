from collections import Counter
from typing import List, Dict

from PDS_Extractors.Helpers.MonthsHelper import MonthsHelper
from PDS_Extractors.Models.Production.MonthlyProduction import MonthlyProduction


class Production:
    def __init__(self, year: int, monthly_production_list: List[MonthlyProduction]):
        self.year: int = year
        self.monthly_production_list: List[MonthlyProduction] = monthly_production_list

    @classmethod
    def from_dict(cls, datadict):
        year = datadict[Production.JSONKeys.year]

        monthly_production = []
        for mp_dict in datadict[Production.JSONKeys.monthly_production_list]:
            pt_month_short_name = mp_dict[Production.JSONKeys.month]
            if pt_month_short_name == "total":
                continue  # ignore 'total' month_year
            en_us_short_name = MonthsHelper.english[pt_month_short_name]
            mp_dict[Production.JSONKeys.month] = MonthsHelper.get_ordinal_from_short_name(en_us_short_name)
            mp_dict[Production.JSONKeys.year] = year
            monthly_production.append(MonthlyProduction.from_dict(mp_dict))

        return cls(
            year,
            monthly_production
        )

    class JSONKeys:
        year = "year"
        month = "month"
        monthly_production_list = "production"

    def total_volume(self) -> int:
        return sum(mp.total_volume() for mp in self.monthly_production_list)

    def volume_by_family(self) -> Dict[str, int]:
        monthly_family_volumes = map(lambda mp: mp.volume_by_family(), self.monthly_production_list)
        volume_by_family = dict()
        for monthly_family_volume in monthly_family_volumes:
            volume_by_family = Counter(volume_by_family) + Counter(monthly_family_volume)
        return volume_by_family
