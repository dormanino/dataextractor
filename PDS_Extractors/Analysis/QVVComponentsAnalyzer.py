import datetime
from typing import List, Optional

from PDS_Extractors.Analysis.ComponentsPartsAnalyzer import ComponentsPartsAnalyzer
from PDS_Extractors.Models.Analysis.AnalyzedComponent import AnalyzedComponent
from PDS_Extractors.Models.Analysis.AnalyzedQVVComponents import AnalyzedQVVComponents
from PDS_Extractors.Models.Component.ComponentGroupingType import ComponentGroupingType
from PDS_Extractors.Models.DataSource.TechDocDataSource import TechDocDataSource
from PDS_Extractors.Models.QVV.QVVProduction import QVVProduction
from PDS_Extractors.TechDocValidation.DueDate.DueDateStatus import DueDateStatus
from PDS_Extractors.Analysis.QVVComponentsExtractor import QVVComponentsExtractor


class QVVComponentsAnalyzer:
    def __init__(self, tech_data_source: TechDocDataSource):
        self.components_parts_analyzer = ComponentsPartsAnalyzer()
        self.qvv_components_extractor = QVVComponentsExtractor(tech_data_source, self.components_parts_analyzer)
        self.cache_valid_components_for_qvv = dict()

    def analyzed_qvv_components(self, qvv: QVVProduction, ref_date: datetime.date, include_parts: bool,
                                status_filter: Optional[List[DueDateStatus]] = None) -> AnalyzedQVVComponents:
        analyzed_groupings = dict()
        grouped_components = self.qvv_components_extractor.grouped_components_for_qvv(qvv)
        for grouping, components in grouped_components.items():
            analyzed_components = []
            for component in components:
                analyzed_parts = []
                if include_parts:
                    try:
                        parts = self.qvv_components_extractor.parts_for_component(component)
                        analyzed_parts = list(map(lambda p: self.components_parts_analyzer.analyze_part(p, ref_date), parts))
                    except ValueError:
                        continue
                analyzed_component = self.components_parts_analyzer.analyze_component(component, analyzed_parts, ref_date)
                analyzed_components.append(analyzed_component)

            if status_filter is None or not status_filter:
                analyzed_groupings[grouping] = analyzed_components
            else:
                analyzed_groupings[grouping] = list(filter(lambda ac: ac.due_date_analysis.status in status_filter, analyzed_components))
        return AnalyzedQVVComponents(qvv, analyzed_groupings)

    def valid_qvv_components(self, qvv: QVVProduction, ref_date: datetime.date, include_parts: bool) -> AnalyzedQVVComponents:
        cache_key = ref_date.strftime("%d%m%y") + qvv.baumuster_id + qvv.qvv_id
        cached = self.cache_valid_components_for_qvv.get(cache_key, None)
        if cached is None:

            valid_groupings = dict()
            for grouping, components in self.analyzed_qvv_components(qvv, ref_date, include_parts).components.items():
                if grouping == ComponentGroupingType.Aggregate.name:
                    continue

                # for each valid component, rectify parts list
                valid_components = []
                for component in list(filter(lambda ac: ac.due_date_analysis.is_valid(), components)):
                    valid_parts = list(filter(lambda ap: ap.due_date_analysis.is_valid(), component.parts))
                    valid_component = AnalyzedComponent(component.component, valid_parts, component.ref_date, component.due_date_analysis)
                    valid_components.append(valid_component)

                valid_groupings[grouping] = valid_components

            valid_qvv_components = AnalyzedQVVComponents(qvv, valid_groupings)
            self.cache_valid_components_for_qvv[cache_key] = valid_qvv_components
            return valid_qvv_components

        else:
            return cached
