from datetime import datetime
from typing import Dict, List, Optional

from PDS_Extractors.Analysis.ComponentsPartsAnalyzer import ComponentsPartsAnalyzer
from PDS_Extractors.Models.DataSource.TechDocDataSource import TechDocDataSource
from PDS_Extractors.Models.Baumuster.BaumusterCollection import BaumusterCollection
from PDS_Extractors.Models.Baumuster.BaumusterData import BaumusterData
from PDS_Extractors.Models.Component.Component import Component
from PDS_Extractors.Models.Component.ComponentGroupingType import ComponentGroupingType
from PDS_Extractors.Models.Plant import Plant
from PDS_Extractors.Models.QVV.QVVProduction import QVVProduction


class QVVComponentsExtractor:
    def __init__(self, tech_doc_data_source: TechDocDataSource):
        self.tech_doc_data_source: TechDocDataSource = tech_doc_data_source

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

    @staticmethod
    def find_baumuster_for_id_in_source(baumuster_id: str, vehicles_source: BaumusterCollection) -> Optional[BaumusterData]:
        return next(filter(lambda x: x.baumuster_id == baumuster_id, vehicles_source.bm_data_list), None)

    def grouped_components_for_qvv(self, qvv: QVVProduction, ref_date: datetime.date,) -> Dict[str, List[Component]]:
        vehicles_source = self.vehicles_source_for_family(qvv.family)

        vehicle_bm = self.find_baumuster_for_id_in_source(qvv.baumuster_id, vehicles_source)
        if vehicle_bm is None:
            raise ValueError("Couldn't find Vehicle Baumuster " + qvv.baumuster_id)

        vehicle_components = self.grouped_vehicle_components(vehicle_bm)
        valid_rule_vehicle_components = dict()
        for grouping, components in vehicle_components.items():
            valid_rule_vehicle_components[grouping] = list(filter(lambda ac: ComponentsPartsAnalyzer.validate_code_rule(ac, qvv), components))
        vehicle_aggregates = vehicle_components[ComponentGroupingType.Aggregate.name]
        aggregate_components = self.grouped_aggregate_components(qvv, ref_date, vehicle_aggregates)

        for key in aggregate_components.keys():
            if key in valid_rule_vehicle_components.keys():
                valid_rule_vehicle_components[key].extend(aggregate_components[key])
            else:
                valid_rule_vehicle_components[key] = aggregate_components[key]
        return valid_rule_vehicle_components

    def grouped_vehicle_components(self, vehicle_bm: BaumusterData) -> Dict[str, List[Component]]:
        groupings = [ComponentGroupingType.SAA, ComponentGroupingType.LEG, ComponentGroupingType.General, ComponentGroupingType.Aggregate]
        return self.components_by_grouping(vehicle_bm, groupings)

    def grouped_aggregate_components(self, qvv: QVVProduction, ref_date: datetime.date,
                                     vehicle_aggregates: List[Component]) -> Dict[str, List[Component]]:
        valid_rule_aggregate_components = dict()
        for component in vehicle_aggregates:
            main, secondary = self.aggregates_source_for_aggregate_component(component)

            if ComponentsPartsAnalyzer.analyze_component(component, ref_date).due_date_analysis.should_cross_aggregates():

                try:
                    if component.clean_component_id in self.tech_doc_data_source.cabin_bms:
                        aggregate_components = self.grouped_cabin_aggr_components(component, qvv, main, secondary)
                    else:
                        aggregate_components = self.grouped_non_cabin_aggr_components(component, main, secondary)

                    for grouping, components in aggregate_components.items():
                        valid_rule_components = list(filter(lambda c: ComponentsPartsAnalyzer.validate_code_rule(c, qvv), components))
                        if grouping in valid_rule_aggregate_components.keys():
                            valid_rule_aggregate_components[grouping].extend(valid_rule_components)
                        else:
                            valid_rule_aggregate_components[grouping] = valid_rule_components

                except Exception as error:
                    print(error)
                    continue

        return valid_rule_aggregate_components

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
