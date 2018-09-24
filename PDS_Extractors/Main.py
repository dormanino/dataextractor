from PDS_Extractors.Data.DataPoint import DataPoint
from PDS_Extractors.Models.MonthYear import MonthYear
from PDS_Extractors.Reporting.ReportTrigger import ReportTrigger
from PDS_Extractors.Reporting.ReportType import ReportType

path = DataPoint.PATH_DataFiles

year = 2018
months = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
# months = [9, 10]
month_years = list(map(lambda m: MonthYear(m, year), months))

reports = {
    # "EPU_Split_test_2": ReportType.EPUSplit,
    "2018_cost_analysis_components": ReportType.CostAnalysisComponents,
    # "2018_cost_analysis_components+parts": ReportType.CostAnalysisComponentsAndParts,
}

trigger = ReportTrigger()
for filename, report_type in reports.items():
    report_output = trigger.run(report_type, month_years)
    report_output.write(filename, path)
