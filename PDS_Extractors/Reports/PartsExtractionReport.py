from PDS_Extractors.Models.DataSource.TechDocDataSource import TechDocDataSource
from PDS_Extractors.Models.Plant import Plant
from PDS_Extractors.Reporting.ReportOutput import ReportOutput


class PartsExtractionReport:
    fixed_headers = ["SAA", "SAA_clean"]

    def __init__(self, tech_doc_data_source: TechDocDataSource, bm_list):
        self.tech_doc_data_source = tech_doc_data_source
        self.bm_list = bm_list

    def run(self, plant: Plant):
        bm_collections = []
        saas_list = []

        if plant is Plant.SBC:
            bm_collections = [self.tech_doc_data_source.sbc_vehicles_source,
                              self.tech_doc_data_source.sbc_aggregates_collection]

        elif plant is Plant.JDF:
            bm_collections = [self.tech_doc_data_source.jdf_vehicles_source,
                              self.tech_doc_data_source.jdf_aggregates_collection]

        for bm_collection in bm_collections:
            for bm_data in bm_collection.bm_data_list:
                if bm_data.baumuster_id in self.bm_list:
                    for component in bm_data.components_list:
                        saas_list.append((component.component_id,
                                          component.clean_component_id,
                                          component.baumuster_id,
                                          component.bg,
                                          component.em_ab,
                                          component.t_a,
                                          component.em_bis,
                                          component.t_b))

#        saa_set_list = sorted(list(saas_list), key=lambda x: x)

        return ReportOutput(self.fixed_headers, saas_list)
