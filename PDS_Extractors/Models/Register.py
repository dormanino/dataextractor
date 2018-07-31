class Register:
    def __init__(self, abm_saa, em_ab, em_bis, t_a, t_b,
                 anz, asa, asb, pos,
                 codebedingungen, benennung):
        self.abm_saa = abm_saa
        self.em_ab = em_ab
        self.em_bis = em_bis
        self.t_a = t_a
        self.t_b = t_b
        self.anz = anz
        self.asa = asa
        self.asb = asb
        self.pos = pos
        self.codebedingungen = codebedingungen
        self.benennung = benennung

    @classmethod
    def from_dict(cls, datadict):
        return cls(
            datadict[Register.JSONKeys.abm_saa],
            datadict[Register.JSONKeys.em_ab],
            datadict[Register.JSONKeys.em_bis],
            datadict[Register.JSONKeys.t_a],
            datadict[Register.JSONKeys.t_b],
            datadict.get(Register.JSONKeys.anz, None),
            datadict[Register.JSONKeys.asa],
            datadict[Register.JSONKeys.asb],
            datadict[Register.JSONKeys.pos],
            datadict.get(Register.JSONKeys.codebedingungen, None),
            datadict.get(Register.JSONKeys.benennung, None)
        )

    class JSONKeys:
        abm_saa = "abm_saa"  # conjunto de montagem - pacote de componentes
        em_ab = "em_ab"  # aviso de aplicacao a partir de
        em_bis = "em_bis"  # aviso de aplicacao ate
        t_a = "t_a"  # prazo a partir de
        t_b = "t_b"  # prazo ate
        anz = "anz"
        asa = "asa"
        asb = "asb"
        pos = "pos"
        codebedingungen = "CODEBEDINGUNGEN"  # restricoes de code -- regra de validacao
        benennung = "benennung"  # nome do code
