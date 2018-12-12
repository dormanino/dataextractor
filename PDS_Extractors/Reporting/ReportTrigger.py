import json

from PDS_Extractors.Models.Baumuster.BaumusterInfo import BaumusterInfo
from PDS_Extractors.Models.Plant import Plant
from PDS_Extractors.Reports.FamilyParts import FamilyPartsReport
from PDS_Extractors.TechDoc.Extraction.BaumusterComponentsExtractor import BaumusterComponentsExtractor
from PDS_Extractors.TechDoc.Extraction.QVVComponentsExtractor import QVVComponentsExtractor
from PDS_Extractors.Data.DataPoint import DataPoint
from PDS_Extractors.Models.Baumuster.BaumusterCollection import BaumusterCollection
from PDS_Extractors.Models.DataSource.TechDocDataSource import TechDocDataSource
from PDS_Extractors.Models.Part.ComponentsCollection import ComponentsCollection
from PDS_Extractors.Models.Production.Production import Production
from PDS_Extractors.Reporting.ReportGroupings import ReportGroupings
from PDS_Extractors.Reporting.ReportOutput import ReportOutput
from PDS_Extractors.Reporting.ReportType import ReportType
from PDS_Extractors.Reports.CostAnalysisReport import CostAnalysisReport
from PDS_Extractors.Reports.EPUSplitReport import EPUSplitReport
from PDS_Extractors.Reports.TechDocStatusReport import TechDocStatusReport
from PDS_Extractors.TechDoc.Validation.DueDate.DueDateStatus import DueDateStatus
from PDS_Extractors.Reports.SAAsExtractionReport import SAAsExtractionReport
from PDS_Extractors.Reports.OptionalsPartNumberReport import OptionalsPartNumberReport


class ReportTrigger:
    def __init__(self):
        baumusters_dict = json.load(open(DataPoint.data_info_bm))
        self.baumusters_list = []
        for key, value in baumusters_dict.items():
            if key[0] == "C":
                self.baumusters_list.append(BaumusterInfo(key, value[0], value[1]))

        self.production = Production.from_dict(json.load(open(DataPoint.production)))
        self.tech_doc_data_source = TechDocDataSource(BaumusterCollection.from_dict(json.load(open(DataPoint.data_sbc_vehicles))),
                                                      BaumusterCollection.from_dict(json.load(open(DataPoint.data_jdf_vehicles))),
                                                      BaumusterCollection.from_dict(json.load(open(DataPoint.data_sbc_aggregates))),
                                                      BaumusterCollection.from_dict(json.load(open(DataPoint.data_jdf_aggregates))),
                                                      ComponentsCollection.from_dict(json.load(open(DataPoint.data_3ca_sbc, encoding="utf-8"))),
                                                      ComponentsCollection.from_dict(json.load(open(DataPoint.data_3ca_jdf, encoding="utf-8"))))
        self.qvv_components_extractor = QVVComponentsExtractor(self.tech_doc_data_source)
        self.baumuster_components_extractor = BaumusterComponentsExtractor(self.tech_doc_data_source)

    @staticmethod
    def write_csv(filename, report_output, path):
        report_output.write(filename, path)

    def run(self, report_type, month_years) -> ReportOutput:

        include_parts = False
        if report_type in ReportGroupings.parts_reports:
            include_parts = True

        # COST ANALYSIS
        if report_type in ReportGroupings.cost_analysis_reports:
            report = CostAnalysisReport(self.production, self.qvv_components_extractor)
            return report.run(month_years, include_parts)

        # EPU SPLIT
        if report_type == ReportType.EPUSplit:
            report = EPUSplitReport(self.production, self.qvv_components_extractor)
            return report.run(month_years)

        # FAMILY EXCLUSIVE PARTS
        if report_type == ReportType.FamilyExclusiveParts:
            report = FamilyPartsReport(self.baumusters_list, self.baumuster_components_extractor)
            return report.run(month_years)

        # FAMILY PARTS
        if report_type == ReportType.FamilyParts:
            report = FamilyPartsReport(self.baumusters_list, self.baumuster_components_extractor)
            return report.run(month_years)

        # TECH DOC
        elif report_type in ReportGroupings.tech_doc_reports:

            status_filter = None
            if report_type in ReportGroupings.tech_doc_inverted_sequence_reports:
                status_filter = [DueDateStatus.InvertedSequence]
            elif report_type in ReportGroupings.tech_doc_no_conclusion_reports:
                status_filter = [DueDateStatus.NoConclusion]

            report = TechDocStatusReport(self.production, self.qvv_components_extractor)
            return report.run(month_years, include_parts, status_filter)

        # Tech doc Deltas
        elif report_type in ReportGroupings.tech_doc_delta_reports:
            status_filter = None
            if report_type in ReportGroupings.tech_doc_delta_reports:
                status_filter = [DueDateStatus.Modified_Valid, DueDateStatus.Modified_Invalid, DueDateStatus.New, DueDateStatus.Canceled]

            report = TechDocStatusReport(self.production, self.qvv_components_extractor)
            return report.run(month_years, include_parts, status_filter)

        # SAA extraction from AGRMZ data
        if report_type in ReportGroupings.extract_saa_reports:
            report = SAAsExtractionReport(self.tech_doc_data_source)
            if report_type is ReportType.ExtractSAAFromAGRMZ_SBC:
                return report.run(Plant.SBC)
            elif report_type is ReportType.ExtractSAAFromAGRMZ_JDF:
                return report.run(Plant.JDF)

        # Optionals extraction from 3CA data
        if report_type in ReportGroupings.extract_optionals_reports:
            report = OptionalsPartNumberReport(self.tech_doc_data_source)
            if report_type is ReportType.ExtractSAAFromAGRMZ_SBC:
                return report.run(Plant.SBC)
            elif report_type is ReportType.ExtractSAAFromAGRMZ_JDF:
                return report.run(Plant.JDF)

