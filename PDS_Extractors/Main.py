from PDS_Extractors.Data.DataPoint import DataPoint
from PDS_Extractors.Models.MonthYear import MonthYear
from PDS_Extractors.Reporting.ReportTrigger import ReportTrigger
from PDS_Extractors.Reporting.ReportType import ReportType

path = DataPoint.PATH_DataFiles

year = 2019
months = [1]
# months = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
month_years = list(map(lambda m: MonthYear(m, year), months))


reports = {
    # "2019_1_parts_by_family": ReportType.FamilyParts,
    "2019_1_cost_analysis_with_parts_NEWWWWWWWw": ReportType.CostAnalysisComponentsAndParts
    # "EPU_Split": ReportType.EPUSplit
    # "SAA_SET_SBC": ReportType.ExtractSAAFromAGRMZ_SBC,
    # "SAA_SET_JDF": ReportType.ExtractSAAFromAGRMZ_JDF
    # "ExtractOptionalsPartsFrom3CA_SBC": ReportType.ExtractOptionalsPartsFrom3CA_SBC,
    # "ExtractOptionalsPartsFrom3CA_JDF": ReportType.ExtractOptionalsPartsFrom3CA_JDF
}

trigger = ReportTrigger()
for filename, report_type in reports.items():
    report_output = trigger.run(report_type, month_years)
    report_output.write(filename, path)
