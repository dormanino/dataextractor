import datetime
from typing import Dict, List

from PDS_Extractors.Models.Analysis.AnalyzedBaumusterComponents import AnalyzedBaumusterComponents
from PDS_Extractors.Models.Baumuster.BaumusterInfo import BaumusterInfo
from PDS_Extractors.Models.Component.Component import Component
from PDS_Extractors.TechDoc.Validation.TechDocValidator import TechDocValidator
from PDS_Extractors.Models.Component.ComponentGroupingType import ComponentGroupingType
from PDS_Extractors.Models.DataSource.TechDocDataSource import TechDocDataSource
from PDS_Extractors.TechDoc.Extraction.ComponentsExtractor import ComponentsExtractor


class BaumusterComponentsExtractor:
    def __init__(self, tech_data_source: TechDocDataSource):
        self.tech_doc_validator = TechDocValidator()
        self.components_extractor = ComponentsExtractor(tech_data_source, self.tech_doc_validator)
        self.grouped_components_for_baumuster_cache = dict()

    # COMPONENTS
    def grouped_components_for_baumuster(self, baumuster: BaumusterInfo) -> Dict[str, List[Component]]:
        cache_key = baumuster.baumuster_id
        cached = self.grouped_components_for_baumuster_cache.get(cache_key, None)
        if cached is None:
            baumuster_components = dict()

            vehicles_source = self.components_extractor.vehicles_source_for_family(baumuster.family)
            vehicle_bm = self.components_extractor.find_baumuster_data_for_id_in_source(baumuster.baumuster_id, vehicles_source)

            vehicle_components = self.components_extractor.grouped_vehicle_components(vehicle_bm)
            for grouping, components in vehicle_components.items():
                baumuster_components[grouping] = components

            vehicle_aggregates = vehicle_components[ComponentGroupingType.Aggregate.name]
            aggregate_components = self.components_extractor.grouped_aggregates_for_vehicle_components(vehicle_aggregates)
            for key in aggregate_components.keys():
                if key in baumuster_components.keys():
                    baumuster_components[key].extend(aggregate_components[key])
                else:
                    baumuster_components[key] = aggregate_components[key]

            self.grouped_components_for_baumuster_cache[cache_key] = baumuster_components
            return baumuster_components
        else:
            return cached

    def analyzed_baumuster_components(self, baumuster: BaumusterInfo, ref_date: datetime.date, include_parts: bool) -> AnalyzedBaumusterComponents:
        grouped_components = self.grouped_components_for_baumuster(baumuster)
        analyzed_groupings = self.components_extractor.grouped_analyzed_components(grouped_components, ref_date, include_parts)
        return AnalyzedBaumusterComponents(baumuster, analyzed_groupings, ref_date)

    def valid_baumuster_components(self, baumuster: BaumusterInfo, ref_date: datetime.date, include_parts: bool) -> AnalyzedBaumusterComponents:
        analyzed_baumuster = self.analyzed_baumuster_components(baumuster, ref_date, include_parts)
        valid_groupings = self.components_extractor.grouped_valid_components(analyzed_baumuster.components)
        return AnalyzedBaumusterComponents(baumuster, valid_groupings, ref_date)
