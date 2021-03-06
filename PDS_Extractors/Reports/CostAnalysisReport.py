import sys
from typing import List, Dict

from PDS_Extractors.Reporting.ReportOutput import ReportOutput
from PDS_Extractors.TechDoc.Extraction.QVVComponentsExtractor import QVVComponentsExtractor
from PDS_Extractors.Models.MonthYear import MonthYear
from PDS_Extractors.Models.Production.Production import Production


class CostAnalysisReport:
    fixed_headers = [
        "Month/Year",
        "Baumuster", "BU", "Family", "QVV", "Volume",
        "Component ID", "KG", "ANZ",
        "Pem AB", "Termin AB", "Pem BIS", "Termin BIS",
        "Grouping", "Component BU", "Component Family", "Component Description", "Codebedingungen",
        "Status", "Comment"
    ]
    part_headers = [
        "Part Number", "Part Description", "Part Quantity", "Part BZA",
        "Status", "Comment"
    ]

    cost_headers = [
        "Part ID", "ES1", "ES2", "Plant", "Supplier Number", "Daimler Supplier Code", "Supplier", "Production Country",
        "Supplier Country", "Currency", "Total Price", "Add On"
    ]

    def __init__(self, production: Production, qvv_components_analyzer: QVVComponentsExtractor, parts_cost_data):
        self.production = production
        self.qvv_components_analyzer = qvv_components_analyzer
        self.parts_cost_data: Dict = parts_cost_data

    def run(self, month_years: List[MonthYear], include_parts: bool, include_costs: bool) -> ReportOutput:
        # sanity check: cost w/o parts as source
        if not include_parts and include_costs:
            sys.exit("Request cost data without including parts in the method is not possible")

        all_data = []
        for month_year in month_years:
            try:
                month_data = self.run_month(month_year, include_parts, include_costs)
                all_data.extend(month_data)
            except ValueError as error:
                print(error)
                continue
        final_headers = self.fixed_headers
        if include_parts:
            final_headers.extend(self.part_headers)
        return ReportOutput(final_headers, all_data)

    def run_month(self, month_year: MonthYear, include_parts: bool, include_costs: bool):
        data_rows = []
        monthly_production = self.production.extract_monthly_production(month_year)
        for qvv in monthly_production.qvv_production_list:
            if qvv.qvv_id[0:4] == "QVAA":
                continue
            try:
                analyzed_qvv = self.qvv_components_analyzer.valid_qvv_components(qvv, month_year.to_date(), include_parts)
            except ValueError as error:
                print(error)
                continue
            for grouping, analyzed_components in analyzed_qvv.components.items():
                for analyzed_component in analyzed_components:
                    data_row = [
                        month_year.to_str(),
                        qvv.baumuster_id,
                        qvv.business_unit,
                        qvv.family,
                        qvv.qvv_id,
                        qvv.volume,
                        analyzed_component.component.component_id,
                        analyzed_component.component.kg,
                        analyzed_component.component.anz,
                        # analyzed_component.component.em_ab,
                        # analyzed_component.component.t_a,
                        # analyzed_component.component.em_bis,
                        # analyzed_component.component.t_b,
                        grouping,
                        analyzed_component.component.business_unit,
                        analyzed_component.component.family,
                        # analyzed_component.component.component_description,
                        # analyzed_component.component.validation_rule,
                        # analyzed_component.due_date_analysis.status.name,
                        # analyzed_component.due_date_analysis.comment
                    ]

                    if include_parts:
                        for analyzed_part in analyzed_component.parts:

                            part_data = [
                                analyzed_part.part.part_number,
                                # analyzed_part.part.part_description,
                                analyzed_part.part.quantity,
                                analyzed_part.part.structure_index,
                                analyzed_part.part.bza,
                                analyzed_part.part.em_ab,
                                analyzed_part.part.t_a,
                                analyzed_part.part.em_bis,
                                analyzed_part.part.t_b,
                                # analyzed_part.due_date_analysis.status.name,
                                # analyzed_part.due_date_analysis.comment
                            ]
                            if include_costs:
                                part_id = part_data[0].replace(" ", "")
                                if part_id in self.parts_cost_data.keys():
                                    for part_cost_data in self.parts_cost_data[part_id]:
                                        part_data.extend(part_cost_data.to_list())
                                else:
                                    part_data.append("Cost data not found")

                            extended_data_row = data_row.copy()
                            extended_data_row.extend(part_data)
                            data_rows.append(extended_data_row)
                    else:
                        data_rows.append(data_row)
        return data_rows
