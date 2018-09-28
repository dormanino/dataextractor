from datetime import datetime

from PDS_Extractors.Models.Part.Part import Part
from PDS_Extractors.TechDoc.Validation.DueDate.DueDateAnalysis import DueDateAnalysis


class AnalyzedPart:
    def __init__(self, part: Part, due_date_analysis: DueDateAnalysis, ref_date: datetime.date):
        self.part = part
        self.due_date_analysis = due_date_analysis
        self.ref_date = ref_date
