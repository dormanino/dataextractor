class PartCostData:
    def __init__(self, part_id, es1, es2, plant, supplynbr, dmcsupplcode, supplier, prdcountry, supcountry, currency,
                 totalprice, addon):
        self.part_id: str = part_id
        self.es1: str = es1
        self.es2: str = es2
        self.plant: str = plant
        self.supplynbr: str = supplynbr
        self.dmcsupplcode: str = dmcsupplcode
        self.supplier: str = supplier
        self.prdcountry: str = prdcountry
        self.supcountry: str = supcountry
        self.currency: str = currency
        self.totalprice: str = totalprice
        self.addon: str = addon
