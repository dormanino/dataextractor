from PDS_Extractors.Data.DataPoint import DataPoint
from PDS_Extractors.Models.MonthYear import MonthYear
from PDS_Extractors.Reporting.ReportTrigger import ReportTrigger
from PDS_Extractors.Reporting.ReportType import ReportType

path = DataPoint.PATH_DataFiles

year = 2019
# months = [1]
months = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
month_years = list(map(lambda m: MonthYear(m, year), months))


reports = {
    # "2019_1_family_parts": ReportType.FamilyParts,
    # "2019_1_cost_analysis_components_no_new": ReportType.CostAnalysisComponents
    # "NEW_EPU_Split_test": ReportType.EPUSplit
    "SAA_SET_SBC": ReportType.ExtractSAAFromAGRMZ_SBC,
    "SAA_SET_JDF": ReportType.ExtractSAAFromAGRMZ_JDF
}

trigger = ReportTrigger()
for filename, report_type in reports.items():
    report_output = trigger.run(report_type, month_years)
    report_output.write(filename, path)
