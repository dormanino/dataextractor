from PDS_Extractors.Data.DataPoint import DataPoint
import pandas as pd
import csv

df = pd.read_csv(DataPoint.data_EPU_SPLIT, low_memory=False)
dates_headers = list(df.columns.values)
df['sum'] = df[dates_headers].sum(axis=1)
df2 = df.loc[df.reset_index().groupby(['Part Number'])['sum'].idxmax()]
df2.to_csv(DataPoint.PATH_DataFiles + "\\EPU_SPLIT_consolidated_by_highest_volume_provider.csv", sep='\t')
print(df2.head())

# with open(DataPoint.PATH_DataFiles + "\\fuck.csv", "wb") as f:
#     writer = csv.writer(f, delimiter=",")
#     for df2_item in df2:
#         writer.writerow(df2_item)
