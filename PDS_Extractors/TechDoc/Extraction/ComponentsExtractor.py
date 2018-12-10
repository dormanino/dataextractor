import datetime
from typing import Dict, List
import sys

from PDS_Extractors.Models.Analysis.AnalyzedComponent import AnalyzedComponent
from PDS_Extractors.TechDoc.Validation.TechDocValidator import TechDocValidator
from PDS_Extractors.Models.DataSource.TechDocDataSource import TechDocDataSource
from PDS_Extractors.Models.Baumuster.BaumusterCollection import BaumusterCollection
from PDS_Extractors.Models.Baumuster.BaumusterData import BaumusterData
from PDS_Extractors.Models.Component.Component import Component
from PDS_Extractors.Models.Component.ComponentGroupingType import ComponentGroupingType
from PDS_Extractors.Models.Part.ComponentParts import ComponentParts
from PDS_Extractors.Models.Part.ComponentsCollection import ComponentsCollection
from PDS_Extractors.Models.Part.Part import Part
from PDS_Extractors.Models.Plant import Plant


class ComponentsExtractor:
    def __init__(self, tech_doc_data_source: TechDocDataSource, tech_doc_validator: TechDocValidator):
        self.tech_doc_data_source: TechDocDataSource = tech_doc_data_source
        self.tech_doc_validator = tech_doc_validator
        self.baumuster_data_cache = dict()
        self.component_parts_cache = dict()

    # SOURCE
    def vehicles_source_for_family(self, family: str) -> BaumusterCollection:
        if family in self.tech_doc_data_source.jdf_families:
            return self.tech_doc_data_source.jdf_vehicles_source
        else:
            return self.tech_doc_data_source.sbc_vehicles_source

    def aggregates_source_for_component(self, component: Component) -> (BaumusterCollection, BaumusterCollection):
        if component.grouping_type is not ComponentGroupingType.Aggregate:
            raise ValueError("Component " + component.component_id + " is not an Aggregate")

        if component.family in self.tech_doc_data_source.jdf_families:
            if component.clean_component_id in self.tech_doc_data_source.cabin_bms:
                main_source = self.tech_doc_data_source.jdf_aggregates_collection
                secondary_source = None
            else:
                main_source = self.tech_doc_data_source.jdf_aggregates_collection
                secondary_source = self.tech_doc_data_source.sbc_aggregates_collection
        else:
            if component.clean_component_id in self.tech_doc_data_source.cabin_bms:
                main_source = self.tech_doc_data_source.jdf_aggregates_collection
                secondary_source = self.tech_doc_data_source.sbc_aggregates_collection
            else:
                main_source = self.tech_doc_data_source.sbc_aggregates_collection
                secondary_source = None
        return main_source, secondary_source

    def parts_source_for_component(self, component: Component) -> ComponentsCollection:
        if component.em_ab[0] == "U":
            return self.tech_doc_data_source.sbc_component_parts_collection
        else:  # if component.em_ab[0] == "R":
            return self.tech_doc_data_source.jdf_component_parts_collection

    # PARTS
    def find_parts_for_component_in_source(self, component: Component, source: ComponentsCollection) -> ComponentParts:
        cache_key = str(hash(source)) + str(hash(component))
        not_found_value = "not_found"
        not_found_error = "Couldn't find parts for Component " + component.component_id

        cached_component_parts = self.component_parts_cache.get(cache_key, None)
        print(sys.getsizeof(self.component_parts_cache))
        if cached_component_parts == not_found_value:
            raise ValueError(not_found_error)
        elif cached_component_parts is None:
            parts = next(filter(lambda c: c.component_id == component.component_id, source.component_parts_list), None)
            if parts is not None:
                self.component_parts_cache[cache_key] = parts
                return parts
            else:
                self.component_parts_cache[cache_key] = not_found_value
                raise ValueError(not_found_error)
        else:
            return cached_component_parts

    def parts_for_component(self, component: Component) -> List[Part]:
        parts_source = self.parts_source_for_component(component)
        component_parts = self.find_parts_for_component_in_source(component, parts_source)
        return component_parts.parts_list

    # GENERAL
    def find_baumuster_data_for_id_in_source(self, baumuster_id: str, source: BaumusterCollection) -> BaumusterData:
        cache_key = str(hash(source)) + baumuster_id
        not_found_value = "not_found"
        not_found_error = "Couldn't find Baumuster " + baumuster_id

        cached_baumuster_data = self.baumuster_data_cache.get(cache_key, None)
        if cached_baumuster_data == not_found_value:
            raise ValueError(not_found_error)
        elif cached_baumuster_data is None:
            baumuster_data = next(filter(lambda b: b.baumuster_id == baumuster_id, source.bm_data_list), None)
            if baumuster_data is not None:
                self.baumuster_data_cache[cache_key] = baumuster_data
                return baumuster_data
            else:
                self.baumuster_data_cache[cache_key] = not_found_value
                raise ValueError(not_found_error)
        else:
            return cached_baumuster_data

    @staticmethod
    def extract_components_by_grouping(bm_data: BaumusterData, groupings: List[ComponentGroupingType],
                                       prefix: str = "", suffix: str = "") -> Dict[str, List[Component]]:
        components = dict()
        for grouping in groupings:
            grouping_name = (prefix + " " + grouping.name + " " + suffix).strip()
            components[grouping_name] = bm_data.extract_grouping(grouping)
        return components

    # ANALYZED COMPONENTS
    def grouped_analyzed_components(self, grouped_components: Dict[str, List[Component]],
                                    ref_date: datetime.date, include_parts: bool) -> Dict[str, List[AnalyzedComponent]]:
        analyzed_groupings = dict()
        for grouping, components in grouped_components.items():
            analyzed_components = []
            for component in components:
                analyzed_parts = []
                if include_parts:
                    try:
                        parts = self.parts_for_component(component)
                        analyzed_parts = list(map(lambda p: self.tech_doc_validator.analyze_part(p, ref_date), parts))
                    except ValueError:
                        pass
                analyzed_component = self.tech_doc_validator.analyze_component(component, analyzed_parts, ref_date)
                analyzed_components.append(analyzed_component)
                analyzed_groupings[grouping] = analyzed_components
        return analyzed_groupings

    def grouped_valid_components(self, grouped_analyzed_components: Dict[str, List[AnalyzedComponent]]) -> Dict[str, List[AnalyzedComponent]]:
        valid_groupings = dict()
        for grouping, components in grouped_analyzed_components.items():
            if grouping == ComponentGroupingType.Aggregate.name:
                continue
            else:
                valid_components = []
                for analyzed_component in list(filter(lambda ac: ac.due_date_analysis.is_valid(), components)):
                    if analyzed_component.parts:
                        valid_parts = list(filter(lambda ap: ap.due_date_analysis.is_valid(), analyzed_component.parts))
                        rectified_component = AnalyzedComponent(analyzed_component.component, valid_parts,
                                                                analyzed_component.due_date_analysis, analyzed_component.ref_date)
                        valid_components.append(rectified_component)
                    else:
                        valid_components.append(analyzed_component)
                valid_groupings[grouping] = valid_components
        return valid_groupings

    # VEHICLE COMPONENTS
    def grouped_vehicle_components(self, vehicle_bm: BaumusterData) -> Dict[str, List[Component]]:
        groupings = [ComponentGroupingType.SAA, ComponentGroupingType.LEG,
                     ComponentGroupingType.General, ComponentGroupingType.Aggregate]
        return self.extract_components_by_grouping(vehicle_bm, groupings)

    # AGGREGATE COMPONENTS
    def grouped_aggregates_for_vehicle_components(self, vehicle_components: List[Component]) -> Dict[str, List[Component]]:
        grouped_aggregates_for_vehicle = dict()
        for component in vehicle_components:
            try:
                grouped_aggregates = self.grouped_aggregates_for_component(component)
                for grouping, components in grouped_aggregates.items():
                    if grouping in grouped_aggregates_for_vehicle.keys():
                        grouped_aggregates_for_vehicle[grouping].extend(components)
                    else:
                        grouped_aggregates_for_vehicle[grouping] = components
            except ValueError as error:
                print(error)
                continue
        return grouped_aggregates_for_vehicle

    def grouped_aggregates_for_component(self, component: Component) -> Dict[str, List[Component]]:
        first_src, second_src = self.aggregates_source_for_component(component)

        baumuster_id = component.clean_component_id
        first_aggr_bm = None
        second_aggr_bm = None

        if first_src is not None:
            try:
                first_aggr_bm = self.find_baumuster_data_for_id_in_source(baumuster_id, first_src)
            except ValueError:
                pass
        if second_src is not None:
            try:
                second_aggr_bm = self.find_baumuster_data_for_id_in_source(baumuster_id, second_src)
            except ValueError:
                pass
        if first_aggr_bm is None and second_aggr_bm is None:
            raise ValueError("Couldn't find Aggregate Baumuster " + baumuster_id)

        groupings = [ComponentGroupingType.SAA, ComponentGroupingType.LEG, ComponentGroupingType.General]
        prefix = ComponentGroupingType.Aggregate.name

        sbc_components = dict()
        sbc_aggr_bm = first_aggr_bm if first_src.plant == Plant.SBC else second_aggr_bm
        if sbc_aggr_bm is not None:
            sbc_components = self.extract_components_by_grouping(sbc_aggr_bm, groupings, prefix, baumuster_id + " " + Plant.SBC.name)

        jdf_components = dict()
        jdf_aggr_bm = first_aggr_bm if first_src.plant == Plant.JDF else second_aggr_bm
        if jdf_aggr_bm is not None:
            jdf_components = self.extract_components_by_grouping(jdf_aggr_bm, groupings, prefix, baumuster_id + " " + Plant.JDF.name)

        return dict(sbc_components, **jdf_components)

        # if component.clean_component_id in self.tech_doc_data_source.cabin_bms:
        #     grouped_aggregate_components = self.grouped_cabin_aggr_components(component, main, secondary)
        # else:
        #     grouped_aggregate_components = self.grouped_non_cabin_aggr_components(component, main, secondary)
        # return grouped_aggregate_components

    # def grouped_cabin_aggr_components(self, component: Component,
    #                                   main_aggr_src: BaumusterCollection,
    #                                   sec_aggr_src: BaumusterCollection) -> Dict[str, List[Component]]:
    #     baumuster_id = component.clean_component_id
    #     first_aggr_bm = None
    #     second_aggr_bm = None
    #
    #     try:
    #         first_aggr_bm = self.find_baumuster_data_for_id_in_source(baumuster_id, main_aggr_src)
    #     except ValueError:
    #         pass
    #     try:
    #         second_aggr_bm = self.find_baumuster_data_for_id_in_source(baumuster_id, sec_aggr_src)
    #     except ValueError:
    #         pass
    #
    #     groupings = [ComponentGroupingType.SAA, ComponentGroupingType.LEG, ComponentGroupingType.General]
    #     prefix = ComponentGroupingType.Aggregate.name
    #
    #     # SPECIAL RULE FOR D979811 ACELLO CABIN
    #     if baumuster_id == "D979811":
    #         if first_aggr_bm is None or second_aggr_bm is None:
    #             raise ValueError("Couldn't find Aggregate Baumuster " + baumuster_id)
    #
    #         jdf_aggr_bm = first_aggr_bm if main_aggr_src.plant == Plant.JDF else second_aggr_bm
    #         jdf_components = self.extract_components_by_grouping(jdf_aggr_bm, groupings, prefix, baumuster_id + " " + Plant.JDF.name)
    #
    #         sbc_aggr_bm = second_aggr_bm if sec_aggr_src.plant == Plant.SBC else first_aggr_bm
    #         sbc_components = self.extract_components_by_grouping(sbc_aggr_bm, groupings, prefix, baumuster_id + " " + Plant.SBC.name)
    #
    #         for key in sbc_components.keys():
    #             if key in jdf_components.keys():
    #                 jdf_components[key].extend(sbc_components[key])
    #             else:
    #                 jdf_components[key] = sbc_components[key]
    #         return jdf_components
    #
    #     else:
    #         master_components_list: List[Component] = []
    #         if first_aggr_bm is not None:
    #             master_components_list.extend(first_aggr_bm.components_list)
    #         if second_aggr_bm is not None:
    #             master_components_list.extend(second_aggr_bm.components_list)
    #         if not master_components_list:
    #             raise ValueError("Couldn't find Aggregate Baumuster " + baumuster_id)
    #
    #         mashed_bm_data = BaumusterData(baumuster_id, component.business_unit, component.family, master_components_list)
    #         return self.extract_components_by_grouping(mashed_bm_data, groupings, prefix, baumuster_id)
    #
    # def grouped_non_cabin_aggr_components(self, component: Component, main_aggr_src: BaumusterCollection,
    #                                       sec_aggr_src: BaumusterCollection) -> Dict[str, List[Component]]:
    #     baumuster_id = component.clean_component_id
    #     aggregates_bm = None
    #
    #     try:
    #         aggregates_bm = self.find_baumuster_data_for_id_in_source(baumuster_id, main_aggr_src)
    #     except ValueError:
    #         pass
    #     if aggregates_bm is None:  # search in fallback
    #         try:
    #             aggregates_bm = self.find_baumuster_data_for_id_in_source(baumuster_id, sec_aggr_src)
    #         except ValueError:
    #             pass
    #     if aggregates_bm is None:
    #         raise ValueError("Couldn't find Aggregate Baumuster " + baumuster_id)
    #     groupings = [ComponentGroupingType.SAA, ComponentGroupingType.LEG, ComponentGroupingType.General]
    #     return self.extract_components_by_grouping(aggregates_bm, groupings, "Aggr", baumuster_id)
