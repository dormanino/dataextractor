from datetime import datetime
from typing import List

from PDS_Extractors.Models.Analysis.AnalyzedComponent import AnalyzedComponent
from PDS_Extractors.Models.Analysis.AnalyzedPart import AnalyzedPart
from PDS_Extractors.Models.Component.Component import Component
from PDS_Extractors.Models.Part.Part import Part
from PDS_Extractors.Models.QVV.QVVProduction import QVVProduction
from PDS_Extractors.TechDoc.Validation.CodeRuleValidator import CodeRuleValidator
from PDS_Extractors.TechDoc.Validation.DueDate.DueDateAnalysis import DueDateAnalysis
from PDS_Extractors.TechDoc.Validation.DueDate.DueDateValidator import DueDateValidator


class TechDocValidator:
    def __init__(self):
        self.parts_due_date_cache = dict()
        self.component_due_date_cache = dict()
        self.component_code_rule_cache = dict()

    # PART
    def analyze_part(self, part: Part, ref_date: datetime.date) -> AnalyzedPart:
        due_date_analysis = self.part_due_date_analysis(part, ref_date)
        return AnalyzedPart(part, due_date_analysis, ref_date)

    def part_due_date_analysis(self, part: Part, ref_date: datetime.date) -> DueDateAnalysis:
        cache_key = ref_date.strftime("%d%m%y") + str(hash(part))
        cached = self.parts_due_date_cache.get(cache_key, None)
        if cached is None:
            due_date_analysis = DueDateValidator.part_status_on_date(part, ref_date)
            self.parts_due_date_cache[cache_key] = due_date_analysis
            return due_date_analysis
        else:
            return cached

    # COMPONENT
    def validate_code_rule(self, component: Component, qvv: QVVProduction) -> bool:
        cache_key = qvv.qvv_id + str(hash(component))
        cached = self.component_code_rule_cache.get(cache_key, None)
        if cached is None:
            code_rule_analysis = CodeRuleValidator.validate(component.validation_rule, qvv.composition)
            self.component_code_rule_cache[cache_key] = code_rule_analysis
            return code_rule_analysis
        else:
            return cached

    def analyze_component(self, component: Component, parts: List[AnalyzedPart], ref_date: datetime.date) -> AnalyzedComponent:
        due_date_analysis = self.component_due_date_analysis(component, ref_date)
        return AnalyzedComponent(component, parts, due_date_analysis, ref_date)

    def component_due_date_analysis(self, component: Component, ref_date: datetime.date) -> DueDateAnalysis:
        cache_key = ref_date.strftime("%d%m%y") + str(hash(component))
        cached = self.component_due_date_cache.get(cache_key, None)
        if cached is None:
            due_date_analysis = DueDateValidator.component_status_on_date(component, ref_date)
            self.component_due_date_cache[cache_key] = due_date_analysis
            return due_date_analysis
        else:
            return cached
