from datetime import datetime

from PDS_Extractors.Models.Analysis.AnalyzedComponent import AnalyzedComponent
from PDS_Extractors.Models.Analysis.AnalyzedPart import AnalyzedPart
from PDS_Extractors.Models.Component.Component import Component
from PDS_Extractors.Models.Parts.Part import Part
from PDS_Extractors.Models.QVV.QVVProduction import QVVProduction
from PDS_Extractors.TechDocValidation.CodeRuleValidator import CodeRuleValidator
from PDS_Extractors.TechDocValidation.DueDate.DueDateValidator import DueDateValidator


class ComponentsPartsAnalyzer:

    @staticmethod
    def analyze_component(component: Component, ref_date: datetime.date) -> AnalyzedComponent:
        due_date_analysis = DueDateValidator.component_status_on_date(component, ref_date)
        return AnalyzedComponent(component, ref_date, due_date_analysis)

    @staticmethod
    def analyze_part(part: Part, ref_date: datetime.date) -> AnalyzedPart:
        due_date_analysis = DueDateValidator.part_status_on_date(part, ref_date)
        return AnalyzedPart(part, ref_date, due_date_analysis)

    @staticmethod
    def validate_code_rule(component: Component, qvv: QVVProduction) -> bool:
        return CodeRuleValidator.validate(component.validation_rule, qvv.composition)
