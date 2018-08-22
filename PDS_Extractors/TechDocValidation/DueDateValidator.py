from datetime import datetime
from enum import Enum
from PDS_Extractors.Helpers.MainframeDateConverter import MainframeDateConverter
from PDS_Extractors.Models.Component import Component
from PDS_Extractors.Models.Part import Part


class DueDateStatus(Enum):
    Valid = "Valido"
    Invalid = "Invalido"
    Canceled = "Cancelado"
    Updated = "Modificado"


class DueDateAnalysis:
    def __init__(self, status: DueDateStatus, comment: str):
        self.status: DueDateStatus = status
        self.comment: str = comment

    def is_valid(self) -> bool:
        return self.status == DueDateStatus.Valid


class DueDateValidator:

    @staticmethod
    def component_status_on_date(component: Component, date: datetime.date, days_offset: int = 5) -> DueDateAnalysis:
        return DueDateValidator.reg_status_on_date(component.t_a, component.t_b, component.em_ab, component.em_bis, date, days_offset)

    @staticmethod
    def part_status_on_date(part: Part, date: datetime.date, days_offset: int = 5) -> DueDateAnalysis:
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
                return DueDateAnalysis(DueDateStatus.Valid, 'OK')
            else:
                if to_date == no_deadline:
                    return DueDateAnalysis(DueDateStatus.Valid, "Modificacao sem prazo vide APA " + apa_to)
                elif (int_ref_date - days_offset) <= to_date <= (int_ref_date + days_offset):
                    # TODO: Break into Updated or Canceled by looking for next version of component
                    return DueDateAnalysis(DueDateStatus.Invalid, "Modificado/Cancelado vide APA " + apa_to)
                elif to_date > (int_ref_date + days_offset):
                    return DueDateAnalysis(DueDateStatus.Valid, "Modificacao com prazo em " + str(to_date) + " vide APA " + apa_to)
                elif to_date < (int_ref_date - days_offset):
                    return DueDateAnalysis(DueDateStatus.Invalid, "Prazo fora de referencia")
                else:
                    print("Analise Incoclusiva 1")
                    return DueDateAnalysis(DueDateStatus.Invalid, "Analise Incoclusiva 1")

        elif from_date == no_deadline:
            if apa_to is None:
                return DueDateAnalysis(DueDateStatus.Invalid, "Modificacao sem prazo vide APA " + apa_from)
            else:
                if to_date != no_deadline:
                    return DueDateAnalysis(DueDateStatus.Invalid, "Inversao de sequencia")
                else:
                    return DueDateAnalysis(DueDateStatus.Invalid, "Modificao sem efeito, alterada por APA " + apa_to)

        elif from_date > (int_ref_date + days_offset):
            if apa_to is None:
                return DueDateAnalysis(DueDateStatus.Invalid, "Modificacao futura com prazo vide APA " + apa_from + " e " + str(from_date))
            else:
                if to_date == no_deadline:
                    return DueDateAnalysis(DueDateStatus.Invalid, "Modificao com alteracao futura sem prazo vide APA" + apa_to)
                elif from_date > to_date:
                    return DueDateAnalysis(DueDateStatus.Invalid, "Inversao de sequencia futura")
                elif (int_ref_date - days_offset) <= to_date <= (int_ref_date + days_offset):
                    return DueDateAnalysis(DueDateStatus.Invalid, "Modificao com alteracao futura sem efeito vide APAs" + apa_from + " e " + apa_to)
                elif to_date > (int_ref_date + days_offset):
                    return DueDateAnalysis(DueDateStatus.Invalid, "Modificacao com prazo em " + str(to_date) + " vide APA " + apa_to)
                elif to_date < (int_ref_date - days_offset):
                    return DueDateAnalysis(DueDateStatus.Invalid, "Prazo fora de referencia")
                else:
                    print("Analise Incoclusiva 2")
                    return DueDateAnalysis(DueDateStatus.Invalid, "Analise Incoclusiva 2")

        elif (int_ref_date - days_offset) <= from_date <= (int_ref_date + days_offset):
            if apa_to is None:
                return DueDateAnalysis(DueDateStatus.Valid, 'Aplicado recentemente vide APA' + apa_from)
            else:
                if to_date == no_deadline:
                    return DueDateAnalysis(DueDateStatus.Valid, "Modificao com alteracao futura sem prazo vide APA" + apa_to)
                if (int_ref_date - days_offset) <= to_date <= (int_ref_date + days_offset):
                    return DueDateAnalysis(DueDateStatus.Invalid, "Modificao com alteracao futura sem efeito vide APAs" + apa_from + " e " + apa_to)
                elif to_date > (int_ref_date + days_offset):
                    return DueDateAnalysis(DueDateStatus.Valid, "Modificacao com prazo em " + str(to_date) + " vide APA " + apa_to)
                elif to_date < (int_ref_date - days_offset):
                    return DueDateAnalysis(DueDateStatus.Invalid, "Inversao de sequencia")
                else:
                    print("Analise Incoclusiva 3")
                    return DueDateAnalysis(DueDateStatus.Invalid, "Analise Incoclusiva 3")

        else:
            print("Analise Incoclusiva 4")
            return DueDateAnalysis(DueDateStatus.Invalid, "Analise Incoclusiva 4")

    # @staticmethod
    # def saa_status_between_dates(duedatesource, start_date, end_date=None):
    #
    #     no_deadline = "99999"
    #     from_date = duedatesource.t_a.replace(" ", "")
    #     to_date = duedatesource.t_b.replace(" ", "")
    #     start_ref_date = MainframeDateConverter.date_to_mainframe(start_date)
    #     if end_date is None:
    #         end_ref_date = start_ref_date
    #     else:
    #         end_ref_date = MainframeDateConverter.date_to_mainframe(end_date)
    #
    #     if duedatesource.em_bis is None:
    #         if start_ref_date <= from_date <= end_ref_date:
    #             return True
    #     else:
    #         if start_ref_date <= from_date <= end_ref_date \
    #                 and start_ref_date <= to_date <= end_ref_date:
    #             return True
    #     return False
    #
    # @staticmethod
    # def find_next_cu_for_saa(saa, saa_list):
    #     if saa.em_bis is None:
    #         return None
    #     # TODO: Look for component
    #     return saa
