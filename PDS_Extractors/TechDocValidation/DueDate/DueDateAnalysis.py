from PDS_Extractors.TechDocValidation.DueDate.DueDateStatus import DueDateStatus


class DueDateAnalysis:
    def __init__(self, status: DueDateStatus, comment: str):
        self.status: DueDateStatus = status
        self.comment: str = comment

    def is_valid(self) -> bool:
        return self.status in (DueDateStatus.Valid,
                               DueDateStatus.Modified_Valid,
                               DueDateStatus.New)

    def should_cross_aggregates(self) -> bool:
        return self.status in (DueDateStatus.Valid,
                               DueDateStatus.Modified_Valid,
                               DueDateStatus.Modified_Invalid,
                               DueDateStatus.New)
