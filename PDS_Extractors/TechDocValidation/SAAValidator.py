from enum import Enum

from PDS_Extractors.Helpers.MainframeDateConverter import MainframeDateConverter


class SAAStatus(Enum):
    Valid = "Valido"
    Invalid = "Invalido"
    Canceled = "Cancelado"
    Updated = "Modificado"


class SAAAnalysis:
    def __init__(self, status, comment):
        self.status = status
        self.comment = comment

    def is_valid(self):
        return self.status == SAAStatus.Valid


class SAAValidator:

    @staticmethod
    def saa_status_on_date(saa, date):
        no_deadline = "99999"
        from_date = saa.t_a.replace(" ", "")
        to_date = saa.t_b.replace(" ", "")
        ref_date = MainframeDateConverter.date_to_mainframe(date)

        if to_date < from_date:
            return SAAAnalysis(SAAStatus.Invalid, "Inversao de sequencia")
        if from_date == no_deadline:
            return SAAAnalysis(SAAStatus.Invalid, "Sem data de inicio")
        if from_date > ref_date:
            return SAAAnalysis(SAAStatus.Invalid, "Fora de vigencia")

        if saa.em_bis is None:
            if to_date < ref_date:
                return SAAAnalysis(SAAStatus.Invalid, "Expirado")
            if saa.em_ab.replace(" ", "") == "U0":
                return SAAAnalysis(SAAStatus.Valid, "OK")
            if from_date <= ref_date:
                return SAAAnalysis(SAAStatus.Valid, "OK")
        else:
            if to_date == no_deadline:
                return SAAAnalysis(SAAStatus.Valid, "Modificacao sem prazo")
            if to_date >= ref_date:
                return SAAAnalysis(SAAStatus.Valid, "Modificao com prazo")
            if to_date < ref_date:
                next_saa = SAAValidator.find_next_cu_for_saa(saa, [])
                if next_saa is None:
                    return SAAAnalysis(SAAStatus.Canceled, "Cancelado em APA " + saa.em_bis)
                else:
                    return SAAAnalysis(SAAStatus.Updated, "Modificado em APA " + saa.em_bis)

        return SAAAnalysis(SAAStatus.Invalid, "Analise inconclusiva")

    @staticmethod
    def find_next_cu_for_saa(saa, saa_list):
        if saa.em_bis is None:
            return None
        # TODO: Look for register
        return saa
