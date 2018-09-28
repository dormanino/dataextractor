from PDS_Extractors.Data.DataPoint import DataPoint
import pandas as pd

df = pd.read_csv(DataPoint.data_EPU_SPLIT, low_memory=False)
print(df.head())
