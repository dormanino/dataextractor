import datetime
from typing import List, Optional

from PDS_Extractors.Analysis.ComponentsPartsAnalyzer import ComponentsPartsAnalyzer
from PDS_Extractors.Models.Analysis.AnalyzedQVVComponents import AnalyzedQVVComponents
from PDS_Extractors.Models.Component.ComponentGroupingType import ComponentGroupingType
from PDS_Extractors.Models.DataSource.TechDocDataSource import TechDocDataSource
from PDS_Extractors.Models.QVV.QVVProduction import QVVProduction
from PDS_Extractors.TechDocValidation.DueDate.DueDateStatus import DueDateStatus
from PDS_Extractors.Analysis.QVVComponentsExtractor import QVVComponentsExtractor


class QVVComponentsAnalyzer:
    def __init__(self, tech_data_source: TechDocDataSource):
        self.qvv_components_extractor = QVVComponentsExtractor(tech_data_source)

    def analyzed_qvv_components(self, qvv: QVVProduction, ref_date: datetime.date,
                                status_filter: Optional[List[DueDateStatus]] = None) -> AnalyzedQVVComponents:
        analyzed_groupings = dict()
        grouped_components = self.qvv_components_extractor.grouped_components_for_qvv(qvv, ref_date)
        for grouping, components in grouped_components.items():
            analyzed_components = list(map(lambda c: ComponentsPartsAnalyzer.analyze_component(c, ref_date), components))
            if status_filter is None or not status_filter:
                analyzed_groupings[grouping] = analyzed_components
            else:
                analyzed_groupings[grouping] = list(filter(lambda ac: ac.due_date_analysis.status in status_filter, analyzed_components))
        return AnalyzedQVVComponents(qvv, analyzed_groupings)

    def valid_qvv_components(self, qvv: QVVProduction, ref_date: datetime.date) -> AnalyzedQVVComponents:
        valid_groupings = dict()
        for grouping, components in self.analyzed_qvv_components(qvv, ref_date).components.items():
            if grouping == ComponentGroupingType.Aggregate.name:
                continue
            valid_components = list(filter(lambda ac: ac.due_data_analysis.is_valid(), components))
            valid_groupings[grouping] = valid_components
        return AnalyzedQVVComponents(qvv, valid_groupings)
