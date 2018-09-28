class DueDateComment:
    @staticmethod
    def ok() -> str:
        return "OK"

    @staticmethod
    def applied_recently(apa_from) -> str:
        return "Aplicado recentemente vide APA " + apa_from

    @staticmethod
    def modified_or_canceled(apa_to) -> str:
        return "Modificado/Cancelado vide APA " + apa_to

    # NO DUE DATE
    @staticmethod
    def modified_no_due_date_apa_from(apa_from) -> str:
        return "Modificacao sem prazo vide APA " + apa_from

    @staticmethod
    def modified_no_due_date_apa_to(apa_to) -> str:
        return "Modificacao sem prazo vide APA " + apa_to

    @staticmethod
    def future_modified_no_due_date_apa_to(apa_to) -> str:
        return "Modificacao com alteracao futura sem prazo vide APA " + apa_to

    # DUE DATE
    @staticmethod
    def modified_with_due_date(to_date, apa_to) -> str:
        return "Modificacao com prazo em " + str(to_date) + " vide APA " + apa_to

    @staticmethod
    def future_modified_with_due_date(apa_from, from_date) -> str:
        return "Modificacao futura com prazo vide APA " + apa_from + " e " + str(from_date)

    # NO EFFECT
    @staticmethod
    def modified_no_effect(apa_to) -> str:
        return "Modificacao sem efeito, alterada por APA " + apa_to

    @staticmethod
    def future_modified_no_effect(apa_from, apa_to) -> str:
        return "Modificacao com alteracao futura sem efeito vide APAs " + apa_from + " e " + apa_to

    # OUT OF REFERENCE
    @staticmethod
    def out_of_reference() -> str:
        return "Prazo fora de referencia"

    # INVERTED SEQUENCE
    @staticmethod
    def inverted_sequence() -> str:
        return "Inversao de sequencia"

    @staticmethod
    def future_inverted_sequence() -> str:
        return "Inversao de sequencia futura"

    # NO CONCLUSION
    @staticmethod
    def no_conclusion(index) -> str:
        return "Analise Inconclusiva " + index
