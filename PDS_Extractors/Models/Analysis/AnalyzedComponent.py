from datetime import datetime
from typing import List

from PDS_Extractors.Models.Analysis.AnalyzedPart import AnalyzedPart
from PDS_Extractors.Models.Component.Component import Component
from PDS_Extractors.TechDocValidation.DueDate.DueDateAnalysis import DueDateAnalysis


class AnalyzedComponent:
    def __init__(self, component: Component, parts: List[AnalyzedPart],
                 ref_date: datetime.date, due_date_analysis: DueDateAnalysis):
        self.component = component
        self.parts = parts
        self.ref_date = ref_date
        self.due_date_analysis = due_date_analysis
