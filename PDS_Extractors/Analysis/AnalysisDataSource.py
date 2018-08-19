from typing import List, Optional
from PDS_Extractors.Models.BaumusterCollection import BaumusterCollection
from PDS_Extractors.Models.ComponentsCollection import ComponentsCollection


class AnalysisDataSource:
    def __init__(self,
                 sbc_vehicles_source: BaumusterCollection,
                 jdf_vehicles_source: BaumusterCollection,
                 sbc_aggregates_collection: BaumusterCollection,
                 jdf_aggregates_collection: BaumusterCollection,
                 sbc_component_parts_collection: Optional[ComponentsCollection] = None,
                 jdf_component_parts_collection: Optional[ComponentsCollection] = None):
        self.sbc_vehicles_source: BaumusterCollection = sbc_vehicles_source
        self.jdf_vehicles_source: BaumusterCollection = jdf_vehicles_source
        self.sbc_aggregates_collection: BaumusterCollection = sbc_aggregates_collection
        self.jdf_aggregates_collection: BaumusterCollection = jdf_aggregates_collection
        self.sbc_component_parts_collection: ComponentsCollection = sbc_component_parts_collection
        self.jdf_component_parts_collection: ComponentsCollection = jdf_component_parts_collection

        # Fixed parameters
        self.jdf_families: List[str] = ["Actros"]
        self.cabin_bms: List[str] = ["D979820", "D979811", "D960840", "D960820", "D943899", "D958860", "D958870", "D958880"]
        self.cabin_codes_to_disconsider = ["ZJ4"]

        # # Safe checks
        # if (vehicles_collection_sbc.kind is not BaumusterDataKind.Vehicle or vehicles_collection_sbc.plant is not Plant.SBC) \
        #         or (aggregates_collection_sbc.kind is not BaumusterDataKind.Aggregate or aggregates_collection_sbc.plant is not Plant.SBC) \
        #         or (vehicles_collection_jdf.kind is not BaumusterDataKind.Vehicle or vehicles_collection_jdf.plant is not Plant.JDF) \
        #         or (aggregates_collection_jdf.kind is not BaumusterDataKind.Aggregate or aggregates_collection_jdf.plant is not Plant.JDF):
        #     print("Bad data!")
        #     sys.exit()
