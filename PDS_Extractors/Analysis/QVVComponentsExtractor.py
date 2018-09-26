from typing import Dict, List

from PDS_Extractors.Analysis.ComponentsPartsAnalyzer import ComponentsPartsAnalyzer
from PDS_Extractors.Models.DataSource.TechDocDataSource import TechDocDataSource
from PDS_Extractors.Models.Baumuster.BaumusterCollection import BaumusterCollection
from PDS_Extractors.Models.Baumuster.BaumusterData import BaumusterData
from PDS_Extractors.Models.Component.Component import Component
from PDS_Extractors.Models.Component.ComponentGroupingType import ComponentGroupingType
from PDS_Extractors.Models.Part.ComponentParts import ComponentParts
from PDS_Extractors.Models.Part.ComponentsCollection import ComponentsCollection
from PDS_Extractors.Models.Part.Part import Part
from PDS_Extractors.Models.Plant import Plant
from PDS_Extractors.Models.QVV.QVVProduction import QVVProduction


class QVVComponentsExtractor:
    def __init__(self, tech_doc_data_source: TechDocDataSource, components_parts_analyzer: ComponentsPartsAnalyzer):
        self.tech_doc_data_source: TechDocDataSource = tech_doc_data_source
        self.components_parts_analyzer = components_parts_analyzer
        self.cache_baumuster = dict()
        self.cache_parts = dict()
        self.cache_grouped_components_for_qvv = dict()

    def vehicles_source_for_family(self, family: str) -> BaumusterCollection:
        if family in self.tech_doc_data_source.jdf_families:
            return self.tech_doc_data_source.jdf_vehicles_source
        else:
            return self.tech_doc_data_source.sbc_vehicles_source

    def aggregates_source_for_aggregate_component(self, aggregate: Component) -> (BaumusterCollection, BaumusterCollection):
        if aggregate.clean_component_id in self.tech_doc_data_source.cabin_bms:
            main_source = self.tech_doc_data_source.jdf_aggregates_collection
            secondary_source = self.tech_doc_data_source.sbc_aggregates_collection
        else:
            main_source = self.tech_doc_data_source.sbc_aggregates_collection
            secondary_source = self.tech_doc_data_source.jdf_aggregates_collection
        return main_source, secondary_source

    def parts_source_for_component(self, component: Component) -> ComponentsCollection:
        if component.em_ab[0] == "U":
            return self.tech_doc_data_source.sbc_component_parts_collection
        else:  # if component.em_ab[0] == "R":
            return self.tech_doc_data_source.jdf_component_parts_collection

    def find_baumuster_for_id_in_source(self, baumuster_id: str, source: BaumusterCollection) -> BaumusterData:
        cache_key = str(hash(source)) + baumuster_id
        not_found_value = "not_found"
        not_found_error = "Couldn't find Baumuster " + baumuster_id

        cached_baumuster = self.cache_baumuster.get(cache_key, None)
        if cached_baumuster == not_found_value:
            raise ValueError(not_found_error)
        if cached_baumuster is None:
            baumuster = next(filter(lambda b: b.baumuster_id == baumuster_id, source.bm_data_list), None)
            if baumuster is not None:
                self.cache_baumuster[cache_key] = baumuster
                return baumuster
            else:
                self.cache_baumuster[cache_key] = not_found_value
                raise ValueError(not_found_error)
        else:
            return cached_baumuster

    def find_parts_for_component_in_source(self, component: Component, source: ComponentsCollection) -> ComponentParts:
        cache_key = str(hash(source)) + str(hash(component))
        not_found_value = "not_found"
        not_found_error = "Couldn't find parts for Component " + component.component_id

        cached_parts = self.cache_parts.get(cache_key, None)
        if cached_parts == not_found_value:
            raise ValueError(not_found_error)
        if cached_parts is None:
            parts = next(filter(lambda c: c.component_id == component.component_id, source.component_parts_list), None)
            if parts is not None:
                self.cache_parts[cache_key] = parts
                return parts
            else:
                self.cache_parts[cache_key] = not_found_value
                raise ValueError(not_found_error)
        else:
            return cached_parts

    def grouped_components_for_qvv(self, qvv: QVVProduction) -> Dict[str, List[Component]]:
        cache_key = qvv.baumuster_id + qvv.qvv_id
        cached = self.cache_grouped_components_for_qvv.get(cache_key, None)
        if cached is None:

            vehicles_source = self.vehicles_source_for_family(qvv.family)
            vehicle_bm = self.find_baumuster_for_id_in_source(qvv.baumuster_id, vehicles_source)

            vehicle_components = self.grouped_vehicle_components(vehicle_bm)
            valid_vehicle_components = dict()
            for grouping, components in vehicle_components.items():
                valid_vehicle_components[grouping] = list(filter(lambda ac: self.components_parts_analyzer.validate_code_rule(ac, qvv), components))
            vehicle_aggregates = vehicle_components[ComponentGroupingType.Aggregate.name]
            aggregate_components = self.grouped_aggregate_components(qvv, vehicle_aggregates)

            for key in aggregate_components.keys():
                if key in valid_vehicle_components.keys():
                    valid_vehicle_components[key].extend(aggregate_components[key])
                else:
                    valid_vehicle_components[key] = aggregate_components[key]

            self.cache_grouped_components_for_qvv[cache_key] = valid_vehicle_components
            return valid_vehicle_components

        else:
            return cached

    def grouped_vehicle_components(self, vehicle_bm: BaumusterData) -> Dict[str, List[Component]]:
        groupings = [ComponentGroupingType.SAA, ComponentGroupingType.LEG, ComponentGroupingType.General, ComponentGroupingType.Aggregate]
        return self.components_by_grouping(vehicle_bm, groupings)

    def grouped_aggregate_components(self, qvv: QVVProduction,
                                     vehicle_aggregates: List[Component]) -> Dict[str, List[Component]]:
        valid_aggregate_components = dict()
        for component in vehicle_aggregates:
            main, secondary = self.aggregates_source_for_aggregate_component(component)

            try:
                if component.clean_component_id in self.tech_doc_data_source.cabin_bms:
                    aggregate_components = self.grouped_cabin_aggr_components(component, qvv, main, secondary)
                else:
                    aggregate_components = self.grouped_non_cabin_aggr_components(component, main, secondary)

                for grouping, components in aggregate_components.items():
                    valid_components = list(filter(lambda c: self.components_parts_analyzer.validate_code_rule(c, qvv), components))
                    if grouping in valid_aggregate_components.keys():
                        valid_aggregate_components[grouping].extend(valid_components)
                    else:
                        valid_aggregate_components[grouping] = valid_components

            except Exception as error:
                print(error)
                continue

        return valid_aggregate_components

    def grouped_cabin_aggr_components(self, component: Component, qvv: QVVProduction,
                                      main_aggr_src: BaumusterCollection,
                                      sec_aggr_src: BaumusterCollection) -> Dict[str, List[Component]]:
        component_id = component.clean_component_id

        cleaned_up_composition = qvv.composition.copy()
        for code in self.tech_doc_data_source.cabin_codes_to_ignore:
            if code in cleaned_up_composition:
                cleaned_up_composition.remove(code)

        first_aggr_bm = self.find_baumuster_for_id_in_source(component_id, main_aggr_src)
        second_aggr_bm = self.find_baumuster_for_id_in_source(component_id, sec_aggr_src)

        groupings = [ComponentGroupingType.SAA, ComponentGroupingType.LEG, ComponentGroupingType.General]
        prefix = "Aggr"

        # SPECIAL RULE FOR D979811 ACELLO CABIN
        if component_id == "D979811":
            if first_aggr_bm is None or second_aggr_bm is None:
                raise ValueError("Couldn't find Aggregate Baumuster " + component_id)

            swap_FA0 = "FA0"
            swap_FR0 = "FR0"

            jdf_composition = cleaned_up_composition.copy()
            if swap_FA0 in jdf_composition:
                jdf_composition.remove(swap_FA0)
            if swap_FR0 not in jdf_composition:
                jdf_composition.append(swap_FR0)
            jdf_aggr_bm = first_aggr_bm if main_aggr_src.plant == Plant.JDF else second_aggr_bm
            jdf_components = self.components_by_grouping(jdf_aggr_bm, groupings, prefix, component_id)

            sbc_composition = cleaned_up_composition.copy()
            if swap_FR0 in sbc_composition:
                sbc_composition.remove(swap_FR0)
            if swap_FA0 not in sbc_composition:
                sbc_composition.append(swap_FA0)
            sbc_aggr_bm = second_aggr_bm if sec_aggr_src.plant == Plant.SBC else first_aggr_bm
            sbc_components = self.components_by_grouping(sbc_aggr_bm, groupings, prefix, component_id)
            for key in sbc_components.keys():
                if key in jdf_components.keys():
                    jdf_components[key].extend(sbc_components[key])
                else:
                    jdf_components[key] = sbc_components[key]
            return jdf_components

        else:
            master_components_list: List[Component] = []
            if first_aggr_bm is not None:
                master_components_list.extend(first_aggr_bm.components_list)
            if second_aggr_bm is not None:
                master_components_list.extend(second_aggr_bm.components_list)
            if not master_components_list:
                raise ValueError("Couldn't find Aggregate Baumuster " + component_id)

            mashed_bm_data = BaumusterData(component_id, master_components_list)
            return self.components_by_grouping(mashed_bm_data, groupings, prefix, component_id)

    def grouped_non_cabin_aggr_components(self, component: Component, main_aggr_src: BaumusterCollection,
                                          sec_aggr_src: BaumusterCollection) -> Dict[str, List[Component]]:
        component_id = component.clean_component_id
        aggregates_bm = self.find_baumuster_for_id_in_source(component_id, main_aggr_src)
        if aggregates_bm is None:  # search in fallback
            aggregates_bm = self.find_baumuster_for_id_in_source(component_id, sec_aggr_src)
        if aggregates_bm is None:
            raise ValueError("Couldn't find Aggregate Baumuster " + component_id)
        groupings = [ComponentGroupingType.SAA, ComponentGroupingType.LEG, ComponentGroupingType.General]
        return self.components_by_grouping(aggregates_bm, groupings, "Aggr", component_id)

    @staticmethod
    def components_by_grouping(bm_data: BaumusterData, groupings: List[ComponentGroupingType],
                               prefix: str = "", suffix: str = "") -> Dict[str, List[Component]]:
        components = dict()
        for grouping in groupings:
            grouping_name = (prefix + " " + grouping.name + " " + suffix).strip()
            components[grouping_name] = bm_data.extract_grouping(grouping)
        return components

    def parts_for_component(self, component: Component) -> List[Part]:
        parts_source = self.parts_source_for_component(component)
        component_parts = self.find_parts_for_component_in_source(component, parts_source)
        return component_parts.parts_list
