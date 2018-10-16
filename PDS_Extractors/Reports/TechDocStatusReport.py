from typing import List

from PDS_Extractors.Reporting.ReportOutput import ReportOutput
from PDS_Extractors.TechDoc.Extraction.QVVComponentsExtractor import QVVComponentsExtractor
from PDS_Extractors.Models.MonthYear import MonthYear
from PDS_Extractors.Models.Production.Production import Production


class TechDocStatusReport:
    fixed_headers = [
        "Month/Year",
        "Business Unit", "Family", "Baumuster", "QVV",  "Volume",
        "Component ID", "KG", "ANZ",
        "Pem AB", "Termin AB", "Pem BIS", "Termin BIS",
        "Grouping", "Component Description", "Codebedingungen",
        "Status", "Comment"
    ]
    part_headers = [
        "Part Number", "Part Description", "Part Quantity", "Part BZA",
        "Status", "Comment"
    ]

    def __init__(self, production: Production, qvv_components_analyzer: QVVComponentsExtractor):
        self.production = production
        self.qvv_components_analyzer = qvv_components_analyzer

    def run(self, month_years: List[MonthYear], include_parts: bool, status_filter) -> ReportOutput:
        all_data = []
        for month_year in month_years:
            try:
                month_data = self.run_month(month_year, include_parts, status_filter)
                all_data.extend(month_data)
            except Exception as error:
                print(error)
                continue
        final_headers = self.fixed_headers
        if include_parts:
            final_headers.extend(self.part_headers)
        return ReportOutput(final_headers, all_data)

    def run_month(self, month_year: MonthYear, include_parts: bool, status_filter):
        data_rows = []
        monthly_production = self.production.extract_monthly_production(month_year)
        for qvv in monthly_production.qvv_production_list:
            analyzed_qvv = self.qvv_components_analyzer.analyzed_qvv_components(qvv, month_year.to_date(), include_parts)
            for grouping, analyzed_components in analyzed_qvv.components.items():

                if status_filter is None or not status_filter:
                    filtered_components = analyzed_components
                else:
                    filtered_components = list(filter(lambda ac: ac.due_date_analysis.status in status_filter, analyzed_components))

                for analyzed_component in filtered_components:
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
                        analyzed_component.component.validation_rule,
                        analyzed_component.due_date_analysis.status.value,
                        analyzed_component.due_date_analysis.comment
                    ]

                    if include_parts:

                        if status_filter is None or not status_filter:
                            filtered_parts = analyzed_component.parts
                        else:
                            filtered_parts = list(filter(lambda ac: ac.due_date_analysis.status in status_filter, analyzed_component.parts))

                        for analyzed_part in filtered_parts:
                            part_data = [
                                analyzed_part.part.part_number,
                                analyzed_part.part.part_description,
                                analyzed_part.part.quantity,
                                analyzed_part.part.bza,
                                analyzed_part.due_date_analysis.status.name,
                                analyzed_part.due_date_analysis.comment
                            ]
                            extended_data_row = data_row.copy()
                            extended_data_row.extend(part_data)
                            data_rows.append(extended_data_row)

                    else:
                        data_rows.append(data_row)

        return data_rows