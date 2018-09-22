from typing import Optional

from PDS_Extractors.Models.MonthYear import MonthYear
from PDS_Extractors.Models.Production.MonthlyProduction import MonthlyProduction
from PDS_Extractors.Models.Production.Production import Production


class ProductionAnalyzer:

    @staticmethod
    def extract_monthly_production(month_year: MonthYear, production: Production) -> Optional[MonthlyProduction]:
        month = month_year.month
        year = month_year.year
        found = next(filter(lambda mp: mp.month == month and mp.year == year, production.monthly_production_list), None)
        if found is None:
            raise ValueError(month_year.to_str() + " not found in Production data")
        return found
