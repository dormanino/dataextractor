from PDS_Extractors.Data.DataPoint import DataPoint
from PDS_Extractors.Models.MonthYear import MonthYear
from PDS_Extractors.Reporting.ReportTrigger import ReportTrigger
from PDS_Extractors.Reporting.ReportType import ReportType

path = DataPoint.PATH_DataFiles

year = 2019
# months_list = [1]
months_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

cache_bypass = False

if not cache_bypass:

    month_years = list(map(lambda m: MonthYear(m, year), months_list))
    reports = {
        # "EPU_Split": ReportType.EPUSplit
        # "2019_1_cost_analysis_QVAAs": ReportType.CostAnalysisComponents
        # "2019_1_cost_analysis_with_parts_QVAAs": ReportType.CostAnalysisComponentsAndParts
        # "SAA_SET_SBC": ReportType.ExtractSAAFromAGRMZ_SBC,
        # "SAA_SET_JDF": ReportType.ExtractSAAFromAGRMZ_JDF
        # "ExtractOptionalsPartsFrom3CA_SBC": ReportType.ExtractOptionalsPartsFrom3CA_SBC,
        # "ExtractOptionalsPartsFrom3CA_JDF": ReportType.ExtractOptionalsPartsFrom3CA_JDF
        "Tech Doc Delta_with parts_no saa filter": ReportType.TechDocDeltaComponentsAndParts
        # "Tech Doc Delta_saa only": ReportType.TechDocDeltaComponents
        # "SAAs and parts for BM SBC": ReportType.ExtractSAAandPartsfromBM_SBC
    }

    trigger = ReportTrigger()
    for filename, report_type in reports.items():
        report_output = trigger.run(report_type, month_years)
        report_output.write(filename, path)

else:

    for months in months_list:

        month_years = list(map(lambda m: MonthYear(m, year), [months]))
        reports = {
            # "2019_1_parts_by_family": ReportType.FamilyParts,
            # "2019_1_cost_analysis_with_parts_QVAAs" + str(months): ReportType.CostAnalysisComponentsAndParts
            # "Tech Doc Delta_with parts" + str(months): ReportType.TechDocDeltaComponentsAndParts
        }

        trigger = ReportTrigger()
        for filename, report_type in reports.items():
            report_output = trigger.run(report_type, month_years)
            report_output.write(filename, path)
