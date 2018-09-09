import csv
import json

from PDS_Extractors.Analysis.AnalysisDataSource import AnalysisDataSource
from PDS_Extractors.Analysis.ProductionAnalysis import ProductionAnalysis
from PDS_Extractors.Data.DataPoint import DataPoint
# from PDS_Extractors.Helpers.MonthsHelper import MonthsHelper
from PDS_Extractors.Models.BaumusterCollection import BaumusterCollection
from PDS_Extractors.Models.ComponentsCollection import ComponentsCollection
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
for month, qvv_prod_components_list in production_analysis.qvv_prod_components_by_month(num_months).items():
    for qvv_prod_components in qvv_prod_components_list:
        qvv_prod = qvv_prod_components.qvv_production
        for grouping, components in qvv_prod_components.components.items():
            for component in components:
                split_mont_year = month.split('/')

                data_lines.append([
                    split_mont_year[0] + '.01.' + split_mont_year[1],
                    qvv_prod.qvv,
                    qvv_prod.baumuster_id,
                    qvv_prod.family,
                    qvv_prod.business_unit,
                    qvv_prod.volume,
                    component.kg,
                    component.component_id,
                    component.clean_component_id,
                    component.bg,
                    component.anz,
                    component.em_ab,
                    component.t_a,
                    component.em_bis,
                    component.t_b,
                    component.validation_rule,
                    grouping
                ])

# Write the file
filename = DataPoint.PATH_DataFiles + '\\analysis_test.csv'
output_file = open(filename, "w", newline="\n")
output_writer = csv.writer(output_file)
# output_writer.writerow(["sep=,"])  # hack to enforce coma separator
output_writer.writerow(["Date", "QVV", "Baumuster", "Vehicle Family", "Business Unit", "Volume",
                        "KG", "SAA", "SAA Clean", "BG", "Amount of assembly turns for given SAA", "Pem AB", "Termin AB",
                        "Pem BIS", "Termin BIS", "Codebedingungen", "Type"])  # headers
for data_line in data_lines:
    output_writer.writerow(data_line)
output_file.close()
print("Done!")
