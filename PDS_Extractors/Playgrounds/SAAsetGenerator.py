import csv
import json

from PDS_Extractors.Analysis.AnalysisDataSource import AnalysisDataSource
from PDS_Extractors.Analysis.ProductionAnalysis import ProductionAnalysis
from PDS_Extractors.Data.DataPoint import DataPoint
from PDS_Extractors.Helpers.MonthsHelper import MonthsHelper
from PDS_Extractors.Models.BaumusterCollection import BaumusterCollection
# from PDS_Extractors.Models.ComponentsCollection import ComponentsCollection
from PDS_Extractors.Models.Production import Production


# Data Points
analysis_data_source = AnalysisDataSource(BaumusterCollection.from_dict(json.load(open(DataPoint.data_sbc_vehicles))),
                                          BaumusterCollection.from_dict(json.load(open(DataPoint.data_jdf_vehicles))),
                                          BaumusterCollection.from_dict(json.load(open(DataPoint.data_sbc_aggregates))),
                                          BaumusterCollection.from_dict(json.load(open(DataPoint.data_jdf_aggregates))),
                                          # ComponentsCollection.from_dict(json.load(open(DataPoint.data_3ca_sbc, encoding="utf-8"))),
                                          # ComponentsCollection.from_dict(json.load(open(DataPoint.data_3ca_jdf, encoding="utf-8")))
                                          )

production_analysis = ProductionAnalysis(Production.from_dict(json.load(open(DataPoint.production))),
                                         analysis_data_source)

production_months = ["jan", "fev", "mar", "abr", "mai", "jun", "jul", "ago", "set", "out", "nov", "dez"]
# num_months = list(map(lambda x: MonthsHelper.numeric[x], production_months))
num_months = []

data_lines = []
saa_set = set()
# a_pn_set = set()


for month, qvv_prod_components_list in production_analysis.qvv_prod_components_by_month(num_months).items():
    for qvv_prod_components in qvv_prod_components_list:
        qvv_prod = qvv_prod_components.qvv_production
        for grouping, components in qvv_prod_components.components.items():
            for component in components:
                bg_data = component.bg
                if bg_data is None or "N" not in bg_data:
                    if component.em_ab[0] == "U":
                        clean = component.component_id
                        for char in [' ', '.', '/', ',']:
                            clean = clean.replace(char, "")
                        if str(clean)[0] == 'Z':
                            saa_set.add((component.component_id, clean))
                else:
                    print(component.component_id)
                # elif str(clean)[0] == 'A':
                #     a_pn_set.add((component.abm_saa, clean))  # TODO: include json

saa_set_list = list(saa_set)
saa_set_list = sorted(saa_set_list, key=lambda x: x)

data_lines = saa_set_list
filename = DataPoint.PATH_DataFiles + '\\SAA_SET.csv'
output_file = open(filename, "w", newline="\n")
output_writer = csv.writer(output_file)
# output_writer.writerow(["sep=,"])  # hack to enforce coma separator
output_writer.writerow(["SAA", "SAA2"])  # headers
for data_line in data_lines:
    output_writer.writerow(data_line)
output_file.close()

print("Done!")
