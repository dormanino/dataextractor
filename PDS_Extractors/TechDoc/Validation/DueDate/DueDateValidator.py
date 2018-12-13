from datetime import datetime
from PDS_Extractors.Helpers.MainframeDateConverter import MainframeDateConverter
from PDS_Extractors.Models.Component.Component import Component
from PDS_Extractors.Models.Part.Part import Part
from PDS_Extractors.TechDoc.Validation.DueDate.DueDateAnalysis import DueDateAnalysis
from PDS_Extractors.TechDoc.Validation.DueDate.DueDateComment import DueDateComment
from PDS_Extractors.TechDoc.Validation.DueDate.DueDateStatus import DueDateStatus


class DueDateValidator:
    @staticmethod
    def component_status_on_date(component: Component, date: datetime.date, days_offset: int = 16) -> DueDateAnalysis:
        return DueDateValidator.reg_status_on_date(component.t_a, component.t_b, component.em_ab, component.em_bis, date, days_offset)

    @staticmethod
    def part_status_on_date(part: Part, date: datetime.date, days_offset: int = 16) -> DueDateAnalysis:
        return DueDateValidator.reg_status_on_date(part.t_a, part.t_b, part.em_ab, part.em_bis, date, days_offset)

    @staticmethod
    def reg_status_on_date(t_a, t_b, em_ab, em_bis, date, days_offset: int) -> DueDateAnalysis:
        no_deadline = 99999
        from_date = int(t_a.replace(" ", ""))
        to_date = int(t_b.replace(" ", ""))
        apa_from = em_ab
        apa_to = em_bis
        ref_date = MainframeDateConverter.date_to_mainframe(date)
        int_ref_date = int(ref_date)

        if apa_from.replace(' ', '') in ['U0', 'R0'] or from_date < (int_ref_date - days_offset):
            if apa_to is None:
                return DueDateAnalysis(DueDateStatus.Valid, DueDateComment.ok())
            else:
                if to_date == no_deadline:
                    return DueDateAnalysis(DueDateStatus.Valid, DueDateComment.modified_no_due_date_apa_to(apa_to))
                elif (int_ref_date - days_offset) <= to_date <= (int_ref_date + days_offset):
                    # TODO: Break into Modified_Invalid, New or Canceled by looking for next version of component
                    return DueDateAnalysis(DueDateStatus.Modified_Invalid, DueDateComment.modified_or_canceled(apa_to))
                elif to_date > (int_ref_date + days_offset):
                    return DueDateAnalysis(DueDateStatus.Valid, DueDateComment.modified_with_due_date(to_date, apa_to))
                elif to_date < (int_ref_date - days_offset):
                    return DueDateAnalysis(DueDateStatus.Invalid, DueDateComment.out_of_reference())
                else:
                    return DueDateAnalysis(DueDateStatus.NoConclusion, DueDateComment.no_conclusion(1))

        elif from_date == no_deadline:
            if apa_to is None:
                return DueDateAnalysis(DueDateStatus.Invalid, DueDateComment.modified_no_due_date_apa_from(apa_from))
            else:
                if to_date != no_deadline:
                    return DueDateAnalysis(DueDateStatus.InvertedSequence, DueDateComment.inverted_sequence())
                else:
                    return DueDateAnalysis(DueDateStatus.Invalid, DueDateComment.modified_no_effect(apa_to))

        elif from_date > (int_ref_date + days_offset):
            if apa_to is None:
                return DueDateAnalysis(DueDateStatus.Invalid, DueDateComment.future_modified_with_due_date(apa_from, from_date))
            else:
                if to_date == no_deadline:
                    return DueDateAnalysis(DueDateStatus.Invalid, DueDateComment.future_modified_no_due_date_apa_to(apa_to))
                elif from_date > to_date:
                    return DueDateAnalysis(DueDateStatus.InvertedSequence, DueDateComment.future_inverted_sequence())
                elif (int_ref_date - days_offset) <= to_date <= (int_ref_date + days_offset):
                    return DueDateAnalysis(DueDateStatus.NoEffect, DueDateComment.future_modified_no_effect(apa_from, apa_to))
                elif to_date > (int_ref_date + days_offset):
                    return DueDateAnalysis(DueDateStatus.Invalid, DueDateComment.modified_with_due_date(to_date, apa_to))
                elif to_date < (int_ref_date - days_offset):
                    return DueDateAnalysis(DueDateStatus.Invalid, DueDateComment.out_of_reference())
                else:
                    return DueDateAnalysis(DueDateStatus.NoConclusion, DueDateComment.no_conclusion(2))

        elif (int_ref_date - days_offset) <= from_date <= (int_ref_date + days_offset):
            if apa_to is None:
                return DueDateAnalysis(DueDateStatus.Modified_Valid, DueDateComment.applied_recently(apa_from))
            else:
                if to_date == no_deadline:
                    return DueDateAnalysis(DueDateStatus.Modified_Valid, DueDateComment.future_modified_no_due_date_apa_to(apa_to))
                if (int_ref_date - days_offset) <= to_date <= (int_ref_date + days_offset):
                    return DueDateAnalysis(DueDateStatus.NoEffect, DueDateComment.future_modified_no_effect(apa_from, apa_to))
                elif to_date > (int_ref_date + days_offset):
                    return DueDateAnalysis(DueDateStatus.Modified_Valid, DueDateComment.modified_with_due_date(to_date, apa_to))
                elif to_date < (int_ref_date - days_offset):
                    return DueDateAnalysis(DueDateStatus.InvertedSequence, DueDateComment.inverted_sequence())
                else:
                    return DueDateAnalysis(DueDateStatus.NoConclusion, DueDateComment.no_conclusion(3))

        else:
            return DueDateAnalysis(DueDateStatus.NoConclusion, DueDateComment.no_conclusion(4))
