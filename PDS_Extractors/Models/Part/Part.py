class Part:
    def __init__(self, part_number: str, part_description: str, component_id: str,
                 quantity: str, es1: str, es2: str, pos: str, aesa: str, aesb: str, structure_index: str,
                 bza: str, da: str, w: str, em_ab: str, em_bis: str, t_a: str, t_b: str, ehm: str):
        self.part_number: str = part_number
        self.part_description: str = part_description
        self.component_id: str = component_id
        self.quantity: str = quantity.replace(",", ".")
        self.es1 = es1
        self.es2 = es2
        self.pos = pos
        self.aesa = aesa
        self.aesb = aesb
        self.structure_index = structure_index
        self.bza = bza
        self.da = da
        self.w = w
        self.em_ab = em_ab
        self.em_bis = em_bis
        self.t_a = t_a
        self.t_b = t_b
        self.ehm = ehm

    @classmethod
    def from_dict(cls, datadict):
        return cls(
            datadict[Part.JSONKeys.part_number],
            datadict[Part.JSONKeys.part_description],
            datadict[Part.JSONKeys.component_id],
            datadict[Part.JSONKeys.quantity],
            datadict[Part.JSONKeys.es1],
            datadict[Part.JSONKeys.es2],
            datadict[Part.JSONKeys.pos],
            datadict[Part.JSONKeys.aesa],
            datadict[Part.JSONKeys.aesb],
            datadict[Part.JSONKeys.structure_index],
            datadict[Part.JSONKeys.bza],
            datadict[Part.JSONKeys.da],
            datadict[Part.JSONKeys.w],
            datadict[Part.JSONKeys.em_ab],
            datadict[Part.JSONKeys.em_bis],
            datadict[Part.JSONKeys.t_a],
            datadict[Part.JSONKeys.t_b],
            datadict[Part.JSONKeys.ehm]
        )

    class JSONKeys:
        part_number = 'part_number'
        part_description = 'part_description'
        component_id = 'component_id'
        quantity = 'quantity'
        es1 = 'es1'
        es2 = 'es2'
        pos = 'pos'
        aesa = 'aesa'
        aesb = 'aesb'
        structure_index = 'str'
        bza = 'bza'
        da = 'da'
        w = 'w'
        em_ab = 'em-ab'
        em_bis = 'em-bis'
        t_a = 't_a'
        t_b = 't_b'
        ehm = 'ehm'

    def __eq__(self, other):
        return self.part_number == other.part_number \
               and self.component_id == other.component_id \
               and self.pos == other.pos \
               and self.aesa == other.aesa \
               and self.aesb == other.aesb \
               and self.em_ab == other.em_ab \
               and self.em_bis == other.em_bis

    def __hash__(self):
        return hash((
            self.part_number,
            self.component_id,
            self.pos,
            self.aesa,
            self.aesb,
            self.em_ab,
            self.em_bis
        ))
