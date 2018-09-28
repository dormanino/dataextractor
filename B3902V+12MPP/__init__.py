import json

from PDS_Extractors.Data.DataPoint import DataPoint


data_variants = json.load(open(DataPoint.production))
dicto = data_variants['production']
dicto2 = dicto[0]


for item in dicto2:
    print(item)


