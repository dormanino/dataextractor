
from PDS_Extractors.Models.DataSource.TechDocDataSource import TechDocDataSource
from PDS_Extractors.Models.Plant import Plant
from PDS_Extractors.Reporting.ReportOutput import ReportOutput


class SAAsExtractionReport:
    fixed_headers = ["SAA", "SAA_clean"]

    def __init__(self, tech_doc_data_source: TechDocDataSource):
        self.tech_doc_data_source = tech_doc_data_source

    def run(self, plant: Plant):
        bm_collections = []
        saa_set = set()

        if plant is Plant.SBC:
            bm_collections = [self.tech_doc_data_source.sbc_vehicles_source,
                              self.tech_doc_data_source.sbc_aggregates_collection]

        elif plant is Plant.JDF:
            bm_collections = [self.tech_doc_data_source.jdf_vehicles_source,
                              self.tech_doc_data_source.jdf_aggregates_collection]

        for bm_collection in bm_collections:
            for bm_data in bm_collection.bm_data_list:
                for component in bm_data.components_list:
                    if component.grouping_type is component.grouping_type.SAA and "Z" in component.component_id:
                        if component.component_id not in saa_set:
                            saa_set.add((component.component_id, component.clean_component_id))

        saa_set_list = sorted(list(saa_set), key=lambda x: x)

        return ReportOutput(self.fixed_headers, saa_set_list)
