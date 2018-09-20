import datetime
from typing import Dict, List, Optional

from PDS_Extractors.Models.DataSource.TechDocDataSource import TechDocDataSource
from PDS_Extractors.OLD.QVVComponentsValidator import QVVComponentsValidator
from PDS_Extractors.Helpers.MonthsHelper import MonthsHelper
from PDS_Extractors.Models.Production.MonthlyProduction import MonthlyProduction
from PDS_Extractors.Models.Production.Production import Production
from PDS_Extractors.Models.QVV.QVVProductionComponents import QVVProductionComponents


class ProductionAnalysis:

    def __init__(self, production: Production, data_source: TechDocDataSource):
        self.production = production
        self.qvv_valid_components_extractor = QVVComponentsValidator(data_source)

    def qvv_prod_components_by_month(self, months: Optional[List[int]] = None) -> Dict[str, List[QVVProductionComponents]]:
        result = dict()

        monthly_prods = []
        if months is None or not months:
            monthly_prods = self.production.monthly_production_list
        else:
            for month in months:
                monthly_prod = self.extract_monthly_production(month)
                if monthly_prod is not None:
                    monthly_prods.append(monthly_prod)

        for monthly_prod in monthly_prods:
            date_key = MonthsHelper.english[monthly_prod.month] + '/' + str(self.production.year)
            result[date_key] = self.monthly_qvv_production_components(monthly_prod)
        return result

    def extract_monthly_production(self, month_number: int) -> Optional[MonthlyProduction]:
        return next(filter(lambda x: MonthsHelper.numeric[x.month] == month_number, self.production.monthly_production_list), None)

    def monthly_qvv_production_components(self, monthly_production: MonthlyProduction) -> List[QVVProductionComponents]:
        year = self.production.year
        month = MonthsHelper.numeric[monthly_production.month]
        ref_date = datetime.date(year, month, 1)

        result = []
        for qvv_prod in monthly_production.qvv_production_list:
            try:
                valid_components = self.qvv_valid_components_extractor.valid_components_for_qvv_prod(qvv_prod, ref_date)
                result.append(QVVProductionComponents(qvv_prod, valid_components))
            except Exception as error:
                print(error)
                continue
        return result
