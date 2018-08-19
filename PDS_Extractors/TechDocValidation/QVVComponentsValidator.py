import datetime
from typing import Dict, List, Optional

from PDS_Extractors.Analysis.AnalysisDataSource import AnalysisDataSource
from PDS_Extractors.Models.BaumusterCollection import BaumusterCollection
from PDS_Extractors.Models.BaumusterData import BaumusterData
from PDS_Extractors.Models.Component import Component
from PDS_Extractors.Models.GroupingType import GroupingType
from PDS_Extractors.Models.Plant import Plant

from PDS_Extractors.Models.QVVProduction import QVVProduction
from PDS_Extractors.TechDocValidation.QVVCompositionValidator import QVVCompositionValidator


class QVVComponentsValidator:
    def __init__(self, data_source: AnalysisDataSource):
        self.data_source: AnalysisDataSource = data_source

    def vehicles_source_for_family(self, family: str) -> BaumusterCollection:
        if family in self.data_source.jdf_families:
            return self.data_source.jdf_vehicles_source
        else:
            return self.data_source.sbc_vehicles_source

    def aggregates_source_for_aggregate_component(self, aggregate: Component) -> (BaumusterCollection, BaumusterCollection):
        if aggregate.clean_component_id in self.data_source.cabin_bms:
            main_source = self.data_source.jdf_aggregates_collection
            secondary_source = self.data_source.sbc_aggregates_collection
        else:
            main_source = self.data_source.sbc_aggregates_collection
            secondary_source = self.data_source.jdf_aggregates_collection
        return main_source, secondary_source

    @staticmethod
    def find_baumuster_for_id_in_source(baumuster_id: str, vehicles_source: BaumusterCollection) -> Optional[BaumusterData]:
        return next(filter(lambda x: x.baumuster_id == baumuster_id, vehicles_source.bm_data_list), None)

    def valid_components_for_qvv_prod(self, qvv_production: QVVProduction, ref_date: datetime.date) -> Dict[str, List[Component]]:
        vehicles_source = self.vehicles_source_for_family(qvv_production.family)

        vehicle_bm = self.find_baumuster_for_id_in_source(qvv_production.baumuster_id, vehicles_source)
        if vehicle_bm is None:
            raise ValueError("Couldn't find Vehicle Baumuster " + qvv_production.baumuster_id)

        valid_vehicle_components = self.valid_vehicle_components_for_qvv_prod(qvv_production, ref_date, vehicle_bm)
        vehicle_aggregates: List[Component] = valid_vehicle_components.pop(GroupingType.Aggregate.name)
        valid_aggregate_components = self.valid_aggregate_components_for_qvv_prod(qvv_production, ref_date, vehicle_aggregates)

        for key in valid_aggregate_components.keys():
            if key in valid_vehicle_components.keys():
                valid_vehicle_components[key].extend(valid_aggregate_components[key])
            else:
                valid_vehicle_components[key] = valid_aggregate_components[key]
        return valid_vehicle_components

    def valid_vehicle_components_for_qvv_prod(self, qvv_production: QVVProduction, ref_date: datetime.date,
                                              vehicle_bm: BaumusterData) -> Dict[str, List[Component]]:
        groupings = [GroupingType.SAA, GroupingType.LEG, GroupingType.General, GroupingType.Aggregate]
        return self.get_valid_components_for_groupings(vehicle_bm, groupings, qvv_production.composition, ref_date)

    def valid_aggregate_components_for_qvv_prod(self, qvv_production: QVVProduction, ref_date: datetime.date,
                                                aggregate_components: List[Component]) -> Dict[str, List[Component]]:
        valid_components = dict()
        for component in aggregate_components:
            main, secondary = self.aggregates_source_for_aggregate_component(component)

            try:
                if component.clean_component_id in self.data_source.cabin_bms:
                    valid_aggr_components = self.valid_cabin_aggr_components_for_qvv_prod(component, qvv_production, ref_date, main, secondary)
                else:
                    valid_aggr_components = self.valid_no_cabin_aggr_components_for_qvv_prod(component, qvv_production, ref_date, main, secondary)

                for key, components in valid_aggr_components.items():
                    if key in valid_components.keys():
                        valid_components[key].extend(components)
                    else:
                        valid_components[key] = components

            except Exception as error:
                print(error)
                continue

        return valid_components

    def valid_cabin_aggr_components_for_qvv_prod(self, component: Component, qvv_production: QVVProduction,
                                                 ref_date: datetime.date, main_aggr_src: BaumusterCollection,
                                                 sec_aggr_src: BaumusterCollection) -> Dict[str, List[Component]]:
        component_id = component.clean_component_id

        cleaned_up_composition = qvv_production.composition.copy()
        for code in self.data_source.cabin_codes_to_disconsider:
            if code in cleaned_up_composition:
                cleaned_up_composition.remove(code)

        first_aggr_bm = self.find_baumuster_for_id_in_source(component_id, main_aggr_src)
        second_aggr_bm = self.find_baumuster_for_id_in_source(component_id, sec_aggr_src)

        groupings = [GroupingType.SAA, GroupingType.LEG, GroupingType.General]
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
            jdf_components = self.get_valid_components_for_groupings(jdf_aggr_bm, groupings, jdf_composition, ref_date, prefix, component_id)

            sbc_composition = cleaned_up_composition.copy()
            if swap_FR0 in sbc_composition:
                sbc_composition.remove(swap_FR0)
            if swap_FA0 not in sbc_composition:
                sbc_composition.append(swap_FA0)
            sbc_aggr_bm = second_aggr_bm if sec_aggr_src.plant == Plant.SBC else first_aggr_bm
            sbc_components = self.get_valid_components_for_groupings(sbc_aggr_bm, groupings, sbc_composition, ref_date, prefix, component_id)
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
            return self.get_valid_components_for_groupings(mashed_bm_data, groupings, cleaned_up_composition, ref_date, prefix, component_id)

    def valid_no_cabin_aggr_components_for_qvv_prod(self, component: Component, qvv_production: QVVProduction,
                                                    ref_date: datetime.date, main_aggr_src: BaumusterCollection,
                                                    sec_aggr_src: BaumusterCollection) -> Dict[str, List[Component]]:
        component_id = component.clean_component_id

        aggregates_bm = self.find_baumuster_for_id_in_source(component_id, main_aggr_src)
        if aggregates_bm is None:  # search in fallback
            aggregates_bm = self.find_baumuster_for_id_in_source(component_id, sec_aggr_src)
        if aggregates_bm is None:
            raise ValueError("Couldn't find Aggregate Baumuster " + component_id)

        groupings = [GroupingType.SAA, GroupingType.LEG, GroupingType.General]
        return self.get_valid_components_for_groupings(aggregates_bm, groupings, qvv_production.composition, ref_date, "Aggr", component_id)

    @staticmethod
    def get_valid_components_for_groupings(bm_data: BaumusterData, groupings: List[GroupingType], composition: List[str],
                                           ref_date: datetime.date, prefix: str = "", suffix: str = "") -> Dict[str, List[Component]]:
        valid_components = dict()
        for grouping_type in groupings:
            grouping_name = (prefix + " " + grouping_type.name + " " + suffix).strip()
            valid_components[grouping_name] = QVVCompositionValidator.validate(bm_data, grouping_type, composition, ref_date)
        return valid_components
