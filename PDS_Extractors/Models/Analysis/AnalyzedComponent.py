from datetime import datetime
from PDS_Extractors.Models.Component.Component import Component
from PDS_Extractors.TechDocValidation.DueDate.DueDateAnalysis import DueDateAnalysis


class AnalyzedComponent:
    def __init__(self, component: Component, ref_date: datetime.date, due_date_analysis: DueDateAnalysis):
        self.component = component
        self.ref_date = ref_date
        self.due_date_analysis = due_date_analysis
