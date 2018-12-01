from typing import List, Dict

from PDS_Extractors.Models.Analysis.AnalyzedBaumusterComponents import AnalyzedBaumusterComponents
from PDS_Extractors.Models.Baumuster.BaumusterInfo import BaumusterInfo
from PDS_Extractors.Models.Part.Part import Part
from PDS_Extractors.Reporting.ReportOutput import ReportOutput
from PDS_Extractors.TechDoc.Extraction.BaumusterComponentsExtractor import BaumusterComponentsExtractor
from PDS_Extractors.Models.MonthYear import MonthYear


class FamilyExclusivePartsReport:
    headers = [
        "Month/Year",
        "Family", "Baumuster",
        "Component Number",
        "Part Number", "Part Description"
    ]

    # dependency injection (pass the parameters to construct the object construction - helps in the TDD)
    def __init__(self, baumuster_list: List[BaumusterInfo], baumuster_components_extractor: BaumusterComponentsExtractor):
        self.baumuster_list = baumuster_list
        self.baumuster_components_extractor = baumuster_components_extractor

    def run(self, month_years: List[MonthYear]) -> ReportOutput:
        all_data = []
        for month_year in month_years:
            try:
                month_data = self.run_month(month_year)
                all_data.extend(month_data)
            except ValueError as error:
                print(error)
                continue
        return ReportOutput(self.headers, all_data)

    def run_month(self, month_year: MonthYear):

        analyzed_baumusters = list(map(lambda b: self.baumuster_components_extractor.valid_baumuster_components(b, month_year.to_date(), True),
                                       self.baumuster_list))

        parts_by_family = dict()
        for family in list(set(map(lambda ab: ab.baumuster_info.family, analyzed_baumusters))):
            parts_by_family[family] = self.parts_for_family(family, analyzed_baumusters)

        data_rows = []
        for analyzed_baumuster in analyzed_baumusters:
            for analyzed_components in analyzed_baumuster.components.values():
                for analyzed_component in analyzed_components:
                    for analyzed_part in analyzed_component.parts:
                        if self.is_part_exclusive_for_family(analyzed_part.part, analyzed_baumuster.baumuster_info.family, parts_by_family):
                            data_row = [
                                month_year.to_str(),
                                analyzed_baumuster.baumuster_info.family,
                                analyzed_baumuster.baumuster_info.baumuster_id,
                                analyzed_component.component.component_id,
                                analyzed_part.part.part_number,
                                analyzed_part.part.part_description
                            ]

                            data_rows.append(data_row)
        return data_rows

    @staticmethod
    def parts_for_family(family: str, analyzed_baumusters: List[AnalyzedBaumusterComponents]) -> Dict[int, Part]:
        family_components = dict()
        for analyzed_baumuster in list(filter(lambda ab: ab.baumuster_info.family == family, analyzed_baumusters)):
            for components in analyzed_baumuster.components.values():
                for analyzed_component in components:
                    for analyzed_part in analyzed_component.parts:
                        dict_key = analyzed_part.part.part_number
                        if dict_key not in family_components.keys():
                            family_components[dict_key] = analyzed_part.part
        return family_components

    @staticmethod
    def is_part_exclusive_for_family(part: Part, family: str, parts_by_family: Dict[str, Dict[int, Part]]) -> bool:
        # Check if part is in desired family
        parts_by_family_copy = parts_by_family.copy()
        if part.part_number not in parts_by_family_copy.pop(family).keys():
            return False
        for parts in parts_by_family_copy.values():
            if part.part_number in parts:
                return False
        return True
