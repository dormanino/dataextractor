from typing import List

from PDS_Extractors.Reporting.ReportOutput import ReportOutput
from PDS_Extractors.TechDoc.Extraction.QVVComponentsExtractor import QVVComponentsExtractor
from PDS_Extractors.Models.MonthYear import MonthYear
from PDS_Extractors.Models.Production.Production import Production


class PartVolumeData:
    def __init__(self, line_data):
        self.line_data = line_data
        self.month_year_vol = dict()


class EPUSplitReport:
    headers = [
        "Part Number", "Quantity", "BZA", "DA", "W", "EHM",  # Part
        "Baumuster", "BU", "Family", "QVV",  # QVV Production
        "Component Number", "KG", "ANZ", "Grouping", "Component BU", "Component Family",  # Component
    ]

    def __init__(self, production: Production, qvv_components_analyzer: QVVComponentsExtractor):
        self.production = production
        self.qvv_components_analyzer = qvv_components_analyzer

    def run(self, month_years: List[MonthYear]) -> ReportOutput:
        data_rows = dict()
        for month_year in month_years:
            monthly_production = self.production.extract_monthly_production(month_year)
            for qvv in monthly_production.qvv_production_list:
                analyzed_qvv = self.qvv_components_analyzer.valid_qvv_components(qvv, month_year.to_date(), True)
                for grouping, analyzed_components in analyzed_qvv.components.items():
                    for analyzed_component in analyzed_components:
                        for analyzed_part in analyzed_component.parts:
                            # GROUP LINES BY PART NUMBER, BAUMUSTER, SAA
                            line_key = (analyzed_part.part.part_number
                                        + qvv.baumuster_id
                                        + analyzed_component.component.component_id
                                        + qvv.qvv_id).replace(" ", "")

                            if line_key not in data_rows.keys():
                                line_data = [
                                    analyzed_part.part.part_number,
                                    analyzed_part.part.quantity,
                                    analyzed_part.part.bza,
                                    analyzed_part.part.da,
                                    analyzed_part.part.w,
                                    analyzed_part.part.ehm,
                                    qvv.baumuster_id,
                                    qvv.business_unit,
                                    qvv.family,
                                    qvv.qvv_id,
                                    analyzed_component.component.component_id,
                                    analyzed_component.component.kg,
                                    analyzed_component.component.anz,
                                    grouping,
                                    analyzed_component.component.business_unit,
                                    analyzed_component.component.family
                                ]
                                data_rows[line_key] = PartVolumeData(line_data)

                            part_volume_data = data_rows[line_key]
                            if month_year not in part_volume_data.month_year_vol.keys():
                                part_volume_data.month_year_vol[month_year] = 0

                            part_volume_data.month_year_vol[month_year] = qvv.volume  # part_volume_data.month_year_vol[month_year] +

        final_headers = self.headers.copy()
        month_years_str = list(map(lambda my: my.to_str(), month_years))
        final_headers.extend(month_years_str)

        all_data = []
        for part_volume_data_key in sorted(data_rows):
            part_volume_data_data = data_rows[part_volume_data_key]
            line_output = part_volume_data_data.line_data.copy()
            for month_year in month_years:
                if month_year in part_volume_data_data.month_year_vol.keys():
                    line_output.append(part_volume_data_data.month_year_vol[month_year])
                else:
                    line_output.append(0)
            all_data.append(line_output)

        return ReportOutput(final_headers, all_data)
