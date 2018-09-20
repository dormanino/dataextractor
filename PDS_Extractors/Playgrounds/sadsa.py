from PDS_Extractors.Data.DataPoint import DataPoint
from PDS_Extractors.Models.MonthYear import MonthYear
from PDS_Extractors.Reporting.ReportTrigger import ReportTrigger
from PDS_Extractors.Reporting.ReportType import ReportType

# report_type = ReportType.TechDocDeltaComponents
# filename = "tech_doc_delta_refactor_test"
path = DataPoint.PATH_DataFiles

year = 2018
months = [9, 10, 11, 12]
month_years = list(map(lambda m: MonthYear(m, year), months))
days_offset = 5

trigger = ReportTrigger()

reports = {
    "WAW_tech_doc_delta": ReportType.TechDocDeltaComponents,
    "WAW_tech_doc_inverted": ReportType.TechDocInvertedSequenceComponents,
    "WAW_tech_doc_no_conclusion": ReportType.TechDocNoConclusionComponents
}

for filename, report_type in reports.items():
    report_output = trigger.run(report_type, month_years, days_offset)
    report_output.write(filename, path)
