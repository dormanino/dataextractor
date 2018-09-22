from PDS_Extractors.Analysis.ProductionAnalyzer import ProductionAnalyzer
from PDS_Extractors.Analysis.QVVComponentsAnalyzer import QVVComponentsAnalyzer
from PDS_Extractors.Reporting.ReportTrigger import ReportOutput


class TechDocStatusReport:
    headers = ["Month/Year",
               "Baumuster", "QVV", "Business Unit", "Family", "Volume",
               "Component", "KG", "ANZ", "Grouping",
               "Pem AB", "Termin AB", "Pem BIS", "Termin BIS",
               "Codebedingungen",
               "Status", "Comment"]

    def __init__(self, production, tech_doc_data_source, month_years, days_offset, status_filter):
        self.production = production
        self.tech_doc_data_source = tech_doc_data_source
        self.qvv_components_analyzer = QVVComponentsAnalyzer(tech_doc_data_source)
        self.month_years = month_years
        self.days_offset = days_offset
        self.status_filter = status_filter

    def run(self) -> ReportOutput:
        data_rows = []
        for month_year in self.month_years:
            try:
                monthly_production = ProductionAnalyzer.extract_monthly_production(month_year, self.production)
            except Exception as error:
                print(error)
                continue

            for qvv in monthly_production.qvv_production_list:
                analyzed_qvv = self.qvv_components_analyzer.analyzed_qvv_components(qvv, month_year.to_date(), self.status_filter)
                for grouping, analyzed_components in analyzed_qvv.components.items():
                    for analyzed_component in analyzed_components:
                        data_rows.append([
                            month_year.to_str(),
                            qvv.baumuster_id,
                            qvv.qvv_id,
                            qvv.business_unit,
                            qvv.family,
                            qvv.volume,
                            analyzed_component.component.component_id,
                            analyzed_component.component.kg,
                            analyzed_component.component.anz,
                            grouping,
                            analyzed_component.component.em_ab,
                            analyzed_component.component.t_a,
                            analyzed_component.component.em_bis,
                            analyzed_component.component.t_b,
                            analyzed_component.component.validation_rule,
                            analyzed_component.due_date_analysis.status.value,
                            analyzed_component.due_date_analysis.comment
                        ])

        return ReportOutput(TechDocStatusReport.headers, data_rows)
