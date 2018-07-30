class SAA:

    # def __init__(self, id, codebedingungen, abm_saa, benennung, em_ab, em_bis, t_a, t_b):
    def __init__(self, id, abm_saa, benennung, em_ab, em_bis, t_a, t_b):
        self.id = id
        # self.codebedingungen = codebedingungen
        self.abm_saa = abm_saa
        self.benennung = benennung
        self.em_ab = em_ab
        self.em_bis = em_bis
        self.t_a = t_a
        self.t_b = t_b

    @classmethod
    def from_dict(cls, datadict):
        return cls(
            datadict[SAA.JSONKeys.id],
            # datadict[SAA.JSONKeys.codebedingungen],
            datadict[SAA.JSONKeys.abm_saa],
            datadict[SAA.JSONKeys.benennung],
            datadict[SAA.JSONKeys.em_ab],
            datadict[SAA.JSONKeys.em_bis],
            datadict[SAA.JSONKeys.t_a],
            datadict[SAA.JSONKeys.t_b]
        )

    class JSONKeys:
        id = "id"
        codebedingungen = "CODEBEDINGUNGEN"  # restricoes de code -- regra de validacao
        abm_saa = "abm_saa"  # conjunto de montagem - pacote de componentes
        #    "anz": "001",
        #    "asa": "004",
        #    "asb": "999",
        benennung = "benennung"  # nome do code
        #    "bg_CODEBEDINGUNGEN": null,
        #    "bu_su": "B NA0.000",
        em_ab = "em_ab"  # aviso de aplicacao a partir de
        em_bis = "em_bis"  # aviso de aplicacao ate
        #    "hwa": null,
        #    "la": null,
        #    "lt": null,
        #    "p": "N",
        #    "pos": "040",
        #    "r": null,
        #    "sp": null,
        t_a = "t_a"  # prazo a partir de
        t_b = "t_b"  #  prazo ate
        #    "trailing_t_ab": "T",
        #    "trailing_t_bis": null,
        #    "vkfbez": "--"
