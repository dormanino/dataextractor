from PDS_Extractors.TechDoc.Validation.DueDate.DueDateStatus import DueDateStatus


class DueDateAnalysis:
    def __init__(self, status: DueDateStatus, comment: str):
        self.status: DueDateStatus = status
        self.comment: str = comment

    def is_valid(self) -> bool:
        return self.status in (DueDateStatus.Valid,
                               DueDateStatus.Modified_Valid,
                               DueDateStatus.New)
