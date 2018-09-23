from typing import List

from PDS_Extractors.Analysis.ProductionAnalyzer import ProductionAnalyzer
from PDS_Extractors.Analysis.QVVComponentsAnalyzer import QVVComponentsAnalyzer
from PDS_Extractors.Models.MonthYear import MonthYear
from PDS_Extractors.Models.Production.Production import Production
from PDS_Extractors.Reporting.ReportTrigger import ReportOutput


class CostAnalysisReport:
    fixed_headers = [
        "Month/Year",
        "Business Unit", "Family", "Baumuster", "QVV",  "Volume",
        "Component ID", "KG", "ANZ",
        "Pem AB", "Termin AB", "Pem BIS", "Termin BIS",
        "Grouping", "Component Description", "Codebedingungen"
    ]
    part_headers = [
        "Part Number", "Part Quantity", "Part BZA"
    ]

    def __init__(self, production: Production, qvv_components_analyzer: QVVComponentsAnalyzer):
        self.production = production
        self.qvv_components_analyzer = qvv_components_analyzer

    def run(self, month_years: List[MonthYear], include_parts: bool) -> ReportOutput:
        all_data = []
        for month_year in month_years:
            try:
                month_data = self.run_month(month_year, include_parts)
                all_data.extend(month_data)
            except ValueError as error:
                print(error)
                continue
        final_headers = self.fixed_headers
        if include_parts:
            final_headers.extend(self.part_headers)
        return ReportOutput(final_headers, all_data)

    def run_month(self, month_year: MonthYear, include_parts: bool):
        data_rows = []
        monthly_production = ProductionAnalyzer.extract_monthly_production(month_year, self.production)
        for qvv in monthly_production.qvv_production_list:
            analyzed_qvv = self.qvv_components_analyzer.valid_qvv_components(qvv, month_year.to_date(), include_parts)
            for grouping, analyzed_components in analyzed_qvv.components.items():
                for analyzed_component in analyzed_components:
                    data_row = [
                        month_year.to_str(),
                        qvv.business_unit,
                        qvv.family,
                        qvv.baumuster_id,
                        qvv.qvv_id,
                        qvv.volume,
                        analyzed_component.component.component_id,
                        analyzed_component.component.kg,
                        analyzed_component.component.anz,
                        analyzed_component.component.em_ab,
                        analyzed_component.component.t_a,
                        analyzed_component.component.em_bis,
                        analyzed_component.component.t_b,
                        grouping,
                        analyzed_component.component.component_description,
                        analyzed_component.component.validation_rule
                    ]

                    if include_parts:
                        for analyzed_part in analyzed_component.parts:
                            part_data = [
                                analyzed_part.part.part_number,
                                analyzed_part.part.quantity,
                                analyzed_part.part.bza
                            ]
                            data_row.extend(part_data)

                    data_rows.append(data_row)

        return data_rows
