import json

from PDS_Extractors.Data.DataPoint import DataPoint
from PDS_Extractors.Models.SAA import SAA


class DataProvider:

        @staticmethod
        def load_saas():
            # TODO: fetch from external data provider
            data = json.load(open(DataPoint.data_agrmz))
            saas = []
            index = 0
            loop = True
            while loop:
                saa_data = data.get(str(index), None)
                if saa_data is None:
                    loop = False
                    continue
                saa_data["id"] = index
                saas.append(SAA.from_dict(saa_data))
                index += 1
            return saas
