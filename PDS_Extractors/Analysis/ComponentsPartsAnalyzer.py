from datetime import datetime
from typing import List

from PDS_Extractors.Models.Analysis.AnalyzedComponent import AnalyzedComponent
from PDS_Extractors.Models.Analysis.AnalyzedPart import AnalyzedPart
from PDS_Extractors.Models.Component.Component import Component
from PDS_Extractors.Models.Part.Part import Part
from PDS_Extractors.Models.QVV.QVVProduction import QVVProduction
from PDS_Extractors.TechDocValidation.CodeRuleValidator import CodeRuleValidator
from PDS_Extractors.TechDocValidation.DueDate.DueDateAnalysis import DueDateAnalysis
from PDS_Extractors.TechDocValidation.DueDate.DueDateStatus import DueDateStatus
from PDS_Extractors.TechDocValidation.DueDate.DueDateValidator import DueDateValidator


class ComponentsPartsAnalyzer:
    def __init__(self):
        self.cache_parts_due_date = dict()
        self.cache_component_due_date = dict()
        self.cache_component_code_rule = dict()
        self.cache_component_should_cross_aggregates = dict()

    def analyze_part(self, part: Part, ref_date: datetime.date) -> AnalyzedPart:
        due_date_analysis = self.part_due_date_analysis(part, ref_date)
        return AnalyzedPart(part, ref_date, due_date_analysis)

    def analyze_component(self, component: Component, parts: List[AnalyzedPart], ref_date: datetime.date) -> AnalyzedComponent:
        due_date_analysis = self.component_due_date_analysis(component, ref_date)
        return AnalyzedComponent(component, parts, ref_date, due_date_analysis)

    def validate_code_rule(self, component: Component, qvv: QVVProduction) -> bool:
        cache_key = qvv.qvv_id + component.component_id
        cached = self.cache_component_code_rule.get(cache_key, None)
        if cached is None:
            code_rule_analysis = CodeRuleValidator.validate(component.validation_rule, qvv.composition)
            self.cache_component_code_rule[cache_key] = code_rule_analysis
            return code_rule_analysis
        else:
            return cached

    def component_should_cross_agreggates(self, component: Component, ref_date: datetime.date) -> bool:
        due_date_analysis = self.component_due_date_analysis(component, ref_date)
        return due_date_analysis.status in [
                DueDateStatus.Valid,
                DueDateStatus.Modified_Valid,
                DueDateStatus.Modified_Invalid,
                DueDateStatus.New
            ]

    def part_due_date_analysis(self, part: Part, ref_date: datetime.date) -> DueDateAnalysis:
        cache_key = ref_date.strftime("%d%m%y") + part.part_number
        cached = self.cache_parts_due_date.get(cache_key, None)
        if cached is None:
            due_date_analysis = DueDateValidator.part_status_on_date(part, ref_date)
            self.cache_parts_due_date[cache_key] = due_date_analysis
            return due_date_analysis
        else:
            return cached

    def component_due_date_analysis(self, component: Component, ref_date: datetime.date) -> DueDateAnalysis:
        cache_key = ref_date.strftime("%d%m%y") + component.component_id
        cached = self.cache_component_due_date.get(cache_key, None)
        if cached is None:
            due_date_analysis = DueDateValidator.component_status_on_date(component, ref_date)
            self.cache_component_due_date[cache_key] = due_date_analysis
            return due_date_analysis
        else:
            return cached
