import csv
import datetime
import json

from PDS_Extractors.Models.DataSource.TechDocDataSource import TechDocDataSource
from PDS_Extractors.OLD.ProductionAnalysis import ProductionAnalysis
from PDS_Extractors.Data.DataPoint import DataPoint
from PDS_Extractors.Helpers.MonthsHelper import MonthsHelper
from PDS_Extractors.Models.Baumuster.BaumusterCollection import BaumusterCollection
from PDS_Extractors.Models.Part.ComponentsCollection import ComponentsCollection
from PDS_Extractors.Models.Production.Production import Production
from PDS_Extractors.TechDocValidation.DueDate.DueDateValidator import DueDateValidator


# Data Points
analysis_data_source = TechDocDataSource(BaumusterCollection.from_dict(json.load(open(DataPoint.data_sbc_vehicles))),
                                         BaumusterCollection.from_dict(json.load(open(DataPoint.data_jdf_vehicles))),
                                         BaumusterCollection.from_dict(json.load(open(DataPoint.data_sbc_aggregates))),
                                         BaumusterCollection.from_dict(json.load(open(DataPoint.data_jdf_aggregates))),
                                         ComponentsCollection.from_dict(json.load(open(DataPoint.data_3ca_sbc, encoding="utf-8"))),
                                         ComponentsCollection.from_dict(json.load(open(DataPoint.data_3ca_jdf, encoding="utf-8"))))

production_analysis = ProductionAnalysis(Production.from_dict(json.load(open(DataPoint.production))),
                                         analysis_data_source)

production_months = ["abr"]
# num_months = list(map(lambda x: MonthsHelper.numeric[x], production_months))
num_months = [4]

data_lines = []
for month_year, qvv_prod_components_list in production_analysis.qvv_prod_components_by_month(num_months).items():
    # REFDATE FOR PARTS VALIDATION HACK
    month_year_data = month_year.split("/")
    year = int(month_year_data[1])
    month_num = MonthsHelper.numeric[month_year_data[0]]
    ref_date = datetime.date(year, month_num, 1)

    for qvv_prod_components in qvv_prod_components_list:
        qvv_prod = qvv_prod_components.qvv_production
        for grouping, components in qvv_prod_components.components.items():
            for component in components:
                if component.em_ab[0] == "U":
                    parts_source = analysis_data_source.sbc_component_parts_collection
                else:  # if component.em_ab[0] == "R":
                    parts_source = analysis_data_source.jdf_component_parts_collection

                component_parts = next(filter(lambda x: x.component_id == component.component_id, parts_source.component_parts_list), None)
                if component_parts is None:
                    continue

                valid_parts = list(filter(lambda p: DueDateValidator.part_status_on_date(p, ref_date).is_valid(), component_parts.parts_list))

                for part in valid_parts:
                    data_lines.append([
                        month_year,
                        qvv_prod.qvv,
                        qvv_prod.baumuster_id,
                        qvv_prod.family,
                        qvv_prod.business_unit,
                        qvv_prod.volume,
                        component.kg,
                        component.component_id,
                        component.anz,
                        component.em_ab,
                        component.t_a,
                        component.em_bis,
                        component.t_b,
                        component.validation_rule,
                        grouping,
                        part.part_number,
                        part.quantity,
                        part.bza
                    ])


# Write the file
filename = DataPoint.PATH_DataFiles + '\\parts_analysis_test.csv'
output_file = open(filename, "w", newline="\n")
output_writer = csv.writer(output_file)
# output_writer.writerow(["sep=,"])  # hack to enforce coma separator
output_writer.writerow(["Date", "QVV", "Baumuster", "Vehicle Family", "Business Unit", "Volume",
                        "SAA", "Amount of assembly turns for given SAA", "Pem AB", "Termin AB",
                        "Pem BIS", "Termin BIS", "Codebedingungen", "Type",
                        "Part Number", "Part Vol", "MOFO"])  # headers
for data_line in data_lines:
    output_writer.writerow(data_line)
output_file.close()
print("Done!")
