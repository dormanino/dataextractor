from enum import Enum

from PDS_Extractors.Helpers.MainframeDateConverter import MainframeDateConverter


class RegisterStatus(Enum):
    Valid = "Valido"
    Invalid = "Invalido"
    Canceled = "Cancelado"
    Updated = "Modificado"


class RegisterAnalysis:
    def __init__(self, status, comment):
        self.status = status
        self.comment = comment

    def is_valid(self):
        return self.status == RegisterStatus.Valid


class RegisterStatusValidator:

    @staticmethod
    def register_status_on_date(register, date):
        no_deadline = "99999"
        from_date = register.t_a.replace(" ", "")
        to_date = register.t_b.replace(" ", "")
        apa_from = register.em_ab.replace(" ", "")
        ref_date = MainframeDateConverter.date_to_mainframe(date)

        # if to_date < from_date:
        #     return SAAAnalysis(SAAStatus.Invalid, "Inversao de sequencia")
        if from_date == no_deadline:
            return RegisterAnalysis(RegisterStatus.Invalid, "Sem data de inicio")

        if register.em_bis is None:
            if apa_from == "U0" or apa_from == "R0":
                return RegisterAnalysis(RegisterStatus.Valid, "OK")
            if from_date <= ref_date:
                return RegisterAnalysis(RegisterStatus.Valid, "OK")
            if from_date > ref_date:
                return RegisterAnalysis(RegisterStatus.Invalid, "Fora de vigencia")
        else:
            if apa_from == "U0" or apa_from == "R0" or from_date <= ref_date:
                if to_date == no_deadline:
                    return RegisterAnalysis(RegisterStatus.Valid, "Modificacao sem prazo")
                if to_date > ref_date:
                    return RegisterAnalysis(RegisterStatus.Valid, "Modificao com prazo")
                if to_date <= ref_date:
                    next_saa = RegisterStatusValidator.find_update_for_register(register, [])
                    if next_saa is None:
                        return RegisterAnalysis(RegisterStatus.Canceled, "Cancelado em APA " + register.em_bis)
                    else:
                        return RegisterAnalysis(RegisterStatus.Updated, "Modificado em APA " + register.em_bis)

        return RegisterAnalysis(RegisterStatus.Invalid, "Analise inconclusiva")

    @staticmethod
    def find_update_for_register(register, register_list):
        if register.em_bis is None:
            return None
        # TODO: Look for register
        return register
