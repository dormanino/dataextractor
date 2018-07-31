from collections import Counter
from PDS_Extractors.Models.MonthlyProduction import MonthlyProduction


class Production:

    def __init__(self, monthly_production_list: [MonthlyProduction]):
        self.monthly_production_list = monthly_production_list

    def total_volume(self) -> int:
        return sum(monthly_production.total_volume() for monthly_production in self.monthly_production_list)

    def volume_by_family(self):
        monthly_family_volumes = map(lambda x: x.volume_by_family(), self.monthly_production_list)
        volume_by_family = dict()
        for monthly_family_volume in monthly_family_volumes:
            volume_by_family = Counter(volume_by_family) + Counter(monthly_family_volume)
        return volume_by_family

    @classmethod
    def from_dict(cls, datadict):
        monthly_production = list(map(MonthlyProduction.from_dict, datadict[Production.JSONKeys.monthly_production_list]))
        return cls(
            filter(lambda x: x.month != 'total', monthly_production)  # ignore 'total' month
        )

    class JSONKeys:
        monthly_production_list = "production"
