from datetime import datetime
from typing import List

from PDS_Extractors.Models.Analysis.AnalyzedPart import AnalyzedPart
from PDS_Extractors.Models.Component.Component import Component
from PDS_Extractors.TechDoc.Validation.DueDate.DueDateAnalysis import DueDateAnalysis


class AnalyzedComponent:
    def __init__(self, component: Component, parts: List[AnalyzedPart],
                 due_date_analysis: DueDateAnalysis, ref_date: datetime.date):
        self.component = component
        self.parts = parts
        self.due_date_analysis = due_date_analysis
        self.ref_date = ref_date
