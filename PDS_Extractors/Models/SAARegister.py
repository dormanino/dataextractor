from PDS_Extractors.Models.Register import Register


class SAARegister(Register):
    # def __init__(self, id, codebedingungen, abm_saa, benennung, em_ab, em_bis, t_a, t_b):
    def __init__(self, id, abm_saa, em_ab, em_bis, t_a, t_b):
        Register.__init__(self, id, abm_saa, em_ab, em_bis, t_a, t_b)
        # self.codebedingungen = codebedingungen
        # self.benennung = benennung

    @classmethod
    def from_dict(cls, datadict):
        return cls(
            datadict[Register.JSONKeys.id],
            datadict[Register.JSONKeys.abm_saa],
            datadict[Register.JSONKeys.em_ab],
            datadict[Register.JSONKeys.em_bis],
            datadict[Register.JSONKeys.t_a],
            datadict[Register.JSONKeys.t_b]
        # datadict[SAARegister.JSONKeys.codebedingungen],
        # datadict[SAARegister.JSONKeys.benennung],
        )

    class JSONKeys:
        codebedingungen = "CODEBEDINGUNGEN"  # restricoes de code -- regra de validacao
        benennung = "benennung"  # nome do code
