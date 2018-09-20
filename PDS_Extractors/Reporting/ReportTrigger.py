import json

from PDS_Extractors.Data.DataPoint import DataPoint
from PDS_Extractors.Models.Baumuster.BaumusterCollection import BaumusterCollection
from PDS_Extractors.Models.DataSource.TechDocDataSource import TechDocDataSource
from PDS_Extractors.Models.Parts.ComponentsCollection import ComponentsCollection
from PDS_Extractors.Models.Production.Production import Production
from PDS_Extractors.Reporting.ReportOutput import ReportOutput
from PDS_Extractors.Reporting.ReportType import ReportType
from PDS_Extractors.Reports.TechDocStatusReport import TechDocStatusReport
from PDS_Extractors.TechDocValidation.DueDate.DueDateStatus import DueDateStatus


class ReportTrigger:
    def __init__(self):
        self.production = Production.from_dict(json.load(open(DataPoint.production)))
        self.tech_doc_data_source = TechDocDataSource(BaumusterCollection.from_dict(json.load(open(DataPoint.data_sbc_vehicles))),
                                                      BaumusterCollection.from_dict(json.load(open(DataPoint.data_jdf_vehicles))),
                                                      BaumusterCollection.from_dict(json.load(open(DataPoint.data_sbc_aggregates))),
                                                      BaumusterCollection.from_dict(json.load(open(DataPoint.data_jdf_aggregates))),
                                                      ComponentsCollection.from_dict(json.load(open(DataPoint.data_3ca_sbc, encoding="utf-8"))),
                                                      ComponentsCollection.from_dict(json.load(open(DataPoint.data_3ca_jdf, encoding="utf-8"))))

    @staticmethod
    def write_csv(filename, report_output, path):
        report_output.write(filename, path)

    def run(self, report_type, month_years, days_offset) -> ReportOutput:
        report = None

        if report_type in [ReportType.TechDocDeltaComponents, ReportType.TechDocDeltaComponentsAndParts]:
            status_filter = [DueDateStatus.Modified_Valid, DueDateStatus.Modified_Invalid, DueDateStatus.New, DueDateStatus.Canceled]
            report = TechDocStatusReport(self.production, self.tech_doc_data_source, month_years, days_offset, status_filter)

        elif report_type in [ReportType.TechDocInvertedSequenceComponents, ReportType.TechDocInvertedSequenceComponentsAndParts]:
            status_filter = [DueDateStatus.InvertedSequence]
            report = TechDocStatusReport(self.production, self.tech_doc_data_source, month_years, days_offset, status_filter)

        elif report_type in [ReportType.TechDocNoConclusionComponents, ReportType.TechDocNoConclusionComponentsAndParts]:
            status_filter = [DueDateStatus.NoConclusion]
            report = TechDocStatusReport(self.production, self.tech_doc_data_source, month_years, days_offset, status_filter)

        return report.run()
