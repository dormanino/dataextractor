import csv
import datetime
import json

from PDS_Extractors.Models.DataSource.TechDocDataSource import TechDocDataSource
from PDS_Extractors.Data.DataPoint import DataPoint
from PDS_Extractors.Models.Baumuster.BaumusterCollection import BaumusterCollection
from PDS_Extractors.Models.Parts.ComponentsCollection import ComponentsCollection
from PDS_Extractors.TechDocValidation.DueDate.DueDateAnalysis import DueDateStatus
from PDS_Extractors.TechDocValidation.DueDate.DueDateValidator import DueDateValidator


# DATA POINTS
analysis_data_source = TechDocDataSource(BaumusterCollection.from_dict(json.load(open(DataPoint.data_sbc_vehicles))),
                                         BaumusterCollection.from_dict(json.load(open(DataPoint.data_jdf_vehicles))),
                                         BaumusterCollection.from_dict(json.load(open(DataPoint.data_sbc_aggregates))),
                                         BaumusterCollection.from_dict(json.load(open(DataPoint.data_jdf_aggregates))),
                                         ComponentsCollection.from_dict(json.load(open(DataPoint.data_3ca_sbc, encoding="utf-8"))),
                                         ComponentsCollection.from_dict(json.load(open(DataPoint.data_3ca_jdf, encoding="utf-8"))))

# PARAMETERS
num_months = [9, 10, 11, 12]
days_offset = 5
status_filter = [DueDateStatus.Modified_Valid, DueDateStatus.Modified_Invalid]

data_lines = []
for num_month in num_months:
    year = 2018
    ref_date = datetime.date(year, num_month, 1)

    for bm_data in analysis_data_source.sbc_vehicles_source.bm_data_list:
        for component in bm_data.components_list:
            due_data_analysis = DueDateValidator.component_status_on_date(component, ref_date, days_offset)
            if due_data_analysis.status in status_filter:
                data_lines.append([
                    num_month,
                    year,
                    bm_data.baumuster_id,
                    component.component_id,
                    component.kg,
                    component.grouping_type.value,
                    component.anz,
                    component.em_ab,
                    component.t_a,
                    component.em_bis,
                    component.t_b,
                    component.validation_rule,
                    due_data_analysis.status.value,
                    due_data_analysis.comment
                    ])


# Write the file
filename = DataPoint.PATH_DataFiles + '\\delta_components_test.csv'
output_file = open(filename, "w", newline="\n")
output_writer = csv.writer(output_file)
# output_writer.writerow(["sep=,"])  # hack to enforce coma separator
output_writer.writerow(["Month", "Year",
                        "Baumuster",
                        "Component", "KG", "Grouping", "ANZ",
                        "Pem AB", "Termin AB", "Pem BIS", "Termin BIS", "Codebedingungen",
                        "Status", "Comment"])  # headers
                        # "Part Number", "Part Vol", "MOFO"])  # headers
for data_line in data_lines:
    output_writer.writerow(data_line)
output_file.close()
print("Done!")
