from datetime import datetime
from PDS_Extractors.Models.Parts.Part import Part
from PDS_Extractors.TechDocValidation.DueDate.DueDateAnalysis import DueDateAnalysis


class AnalyzedPart:
    def __init__(self, part: Part, ref_date: datetime.date, due_date_analysis: DueDateAnalysis):
        self.part = part
        self.ref_date = ref_date
        self.due_date_analysis = due_date_analysis
