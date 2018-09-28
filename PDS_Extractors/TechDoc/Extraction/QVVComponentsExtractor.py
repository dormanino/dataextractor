import datetime
from typing import Dict, List

from PDS_Extractors.Models.Component.Component import Component
from PDS_Extractors.Models.Plant import Plant
from PDS_Extractors.TechDoc.Validation.TechDocValidator import TechDocValidator
from PDS_Extractors.Models.Analysis.AnalyzedQVVComponents import AnalyzedQVVComponents
from PDS_Extractors.Models.Component.ComponentGroupingType import ComponentGroupingType
from PDS_Extractors.Models.DataSource.TechDocDataSource import TechDocDataSource
from PDS_Extractors.Models.QVV.QVVProduction import QVVProduction
from PDS_Extractors.TechDoc.Extraction.ComponentsExtractor import ComponentsExtractor


class QVVComponentsExtractor:
    def __init__(self, tech_doc_data_source: TechDocDataSource):
        self.tech_doc_data_source = tech_doc_data_source
        self.tech_doc_validator = TechDocValidator()
        self.components_extractor = ComponentsExtractor(self.tech_doc_data_source, self.tech_doc_validator)
        self.grouped_components_for_qvv_cache = dict()

    def validate_acello_cabin(self, components, qvv, plant):
        cleaned_up_composition = qvv.composition.copy()
        for code in self.tech_doc_data_source.cabin_codes_to_ignore:
            if code in cleaned_up_composition:
                cleaned_up_composition.remove(code)

        rectified_composition = cleaned_up_composition.copy()
        swap_fa0 = "FA0"
        swap_fr0 = "FR0"
        if plant == Plant.SBC:
            if swap_fr0 in rectified_composition:
                rectified_composition.remove(swap_fr0)
            if swap_fa0 not in rectified_composition:
                rectified_composition.append(swap_fa0)
        elif plant == Plant.JDF:
            if swap_fa0 in rectified_composition:
                rectified_composition.remove(swap_fa0)
            if swap_fr0 not in rectified_composition:
                rectified_composition.append(swap_fr0)

        rectified_qvv = QVVProduction(qvv.qvv_id, qvv.baumuster_id, qvv.business_unit, qvv.family, qvv.volume, rectified_composition)
        return list(filter(lambda c: self.tech_doc_validator.validate_code_rule(c, rectified_qvv), components))

    def grouped_components_for_qvv(self, qvv: QVVProduction) -> Dict[str, List[Component]]:
        cache_key = qvv.baumuster_id + qvv.qvv_id
        cached = self.grouped_components_for_qvv_cache.get(cache_key, None)
        if cached is None:
            qvv_components = dict()

            vehicles_source = self.components_extractor.vehicles_source_for_family(qvv.family)
            vehicle_bm = self.components_extractor.find_baumuster_data_for_id_in_source(qvv.baumuster_id, vehicles_source)

            vehicle_components = self.components_extractor.grouped_vehicle_components(vehicle_bm)
            for grouping, components in vehicle_components.items():
                qvv_components[grouping] = list(filter(lambda ac: self.tech_doc_validator.validate_code_rule(ac, qvv), components))

            vehicle_aggregates = vehicle_components[ComponentGroupingType.Aggregate.name]
            for grouping, components in self.components_extractor.grouped_aggregates_for_vehicle_components(vehicle_aggregates).items():
                # SPECIAL RULE FOR D979811 ACELLO CABIN
                if "D979811" in grouping and Plant.SBC.name in grouping:
                    valid_components = self.validate_acello_cabin(components, qvv, Plant.SBC)
                elif "D979811" in grouping and Plant.JDF.name in grouping:
                    valid_components = self.validate_acello_cabin(components, qvv, Plant.JDF)
                else:
                    valid_components = list(filter(lambda c: self.tech_doc_validator.validate_code_rule(c, qvv), components))

                if grouping in qvv_components.keys():
                    qvv_components[grouping].extend(valid_components)
                else:
                    qvv_components[grouping] = valid_components

            self.grouped_components_for_qvv_cache[cache_key] = qvv_components
            return qvv_components
        else:
            return cached

    def analyzed_qvv_components(self, qvv: QVVProduction, ref_date: datetime.date, include_parts: bool) -> AnalyzedQVVComponents:
        grouped_components = self.grouped_components_for_qvv(qvv)
        analyzed_groupings = self.components_extractor.grouped_analyzed_components(grouped_components, ref_date, include_parts)
        return AnalyzedQVVComponents(qvv, analyzed_groupings, ref_date)

    def valid_qvv_components(self, qvv: QVVProduction, ref_date: datetime.date, include_parts: bool) -> AnalyzedQVVComponents:
        analyzed_qvv = self.analyzed_qvv_components(qvv, ref_date, include_parts)
        valid_groupings = self.components_extractor.grouped_valid_components(analyzed_qvv.components)
        return AnalyzedQVVComponents(qvv, valid_groupings, ref_date)
