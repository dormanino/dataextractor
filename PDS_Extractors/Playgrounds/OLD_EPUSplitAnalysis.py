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


class Xablau:
    def __init__(self, line_data):
        self.line_data = line_data
        self.monthyear_vol = dict()


# Data Points
analysis_data_source = TechDocDataSource(BaumusterCollection.from_dict(json.load(open(DataPoint.data_sbc_vehicles))),
                                         BaumusterCollection.from_dict(json.load(open(DataPoint.data_jdf_vehicles))),
                                         BaumusterCollection.from_dict(json.load(open(DataPoint.data_sbc_aggregates))),
                                         BaumusterCollection.from_dict(json.load(open(DataPoint.data_jdf_aggregates))),
                                         ComponentsCollection.from_dict(json.load(open(DataPoint.data_3ca_sbc, encoding="utf-8"))),
                                         ComponentsCollection.from_dict(json.load(open(DataPoint.data_3ca_jdf, encoding="utf-8"))))

production_analysis = ProductionAnalysis(Production.from_dict(json.load(open(DataPoint.production))),
                                         analysis_data_source)

production_months = ["jan", "fev", "mar", "abr", "mai", "jun", "jul", "ago", "set", "out", "nov", "dez"]
# num_months = list(map(lambda x: MonthsHelper.numeric[x], production_months))
num_months = []

lines = dict()
month_years = []
for month_year, qvv_prod_components_list in production_analysis.qvv_prod_components_by_month(num_months).items():
    # REFDATE FOR PARTS VALIDATION HACK
    month_year_data = month_year.split("/")
    year = int(month_year_data[1])
    month_num = MonthsHelper.numeric[month_year_data[0]]
    ref_date = datetime.date(year, month_num, 1)

    month_years.append(month_year)

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

                    # GROUP LINES BY PART NUMBER, BAUMUSTER, SAA
                    line_key = (part.part_number + qvv_prod.baumuster_id + component.component_id+qvv_prod.qvv).replace(" ", "")

                    if line_key not in lines.keys():
                        print("NEW " + line_key)
                        line_data = [part.part_number, part.quantity, part.bza, part.da, part.w, part.ehm,
                                     qvv_prod.business_unit, qvv_prod.family, qvv_prod.baumuster_id,
                                     component.component_id, component.kg, component.anz, grouping, qvv_prod.qvv]
                        lines[line_key] = Xablau(line_data)
                    else:
                        print("FOUND " + line_key)

                    xablau = lines[line_key]
                    if month_year not in xablau.monthyear_vol.keys():
                        xablau.monthyear_vol[month_year] = 0

                    xablau.monthyear_vol[month_year] = xablau.monthyear_vol[month_year] + qvv_prod.volume

# Write the file
filename = DataPoint.PATH_DataFiles + '\\EPU_split_analysis_test.csv'
output_file = open(filename, "w", newline="\n")
output_writer = csv.writer(output_file)
# output_writer.writerow(["sep=,"])  # hack to enforce coma separator
headers = ["Part Number", "Quantity", "BZA", "DA", "W", "EHM",  # Part
           "Baumuster", "Business Unit", "Family",  # QVV Production
           "Component Number", "KG", "ANZ", "Grouping"]  # Component
headers.extend(month_years)  # Months
output_writer.writerow(headers)
for xablau_key in sorted(lines):
    xablau_data = lines[xablau_key]
    line_output = xablau_data.line_data.copy()
    for month_year in month_years:
        if month_year in xablau_data.monthyear_vol.keys():
            line_output.append(xablau_data.monthyear_vol[month_year])
        else:
            line_output.append(0)
    output_writer.writerow(line_output)
output_file.close()
print("Done!")
