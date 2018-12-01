from PDS_Extractors.Data.DataPoint import DataPoint
import pandas as pd
import csv

df = pd.read_csv(DataPoint.data_EPU_SPLIT, low_memory=False)
months_header = ['Jan/2019', 'Feb/2019', 'Mar/2019', 'Apr/2019', 'May/2019', 'Jun/2019', 'Jul/2019', 'Aug/2019', 'Sep/2019', 'Oct/2019', 'Nov/2019', 'Dec/2019']
# dates_headers = list(df.columns.values)
df['sum'] = df[months_header].sum(axis=1)
df2 = df.loc[df.reset_index().groupby(['Part Number'])['sum'].idxmax()]
df3 = df.groupby(['Part Number'])['Jan/2019', 'Feb/2019', 'Mar/2019', 'Apr/2019', 'May/2019', 'Jun/2019', 'Jul/2019', 'Aug/2019', 'Sep/2019', 'Oct/2019', 'Nov/2019', 'Dec/2019'].apply(lambda x: x.astype(int).sum())
df4 = df.groupby(['Part Number', 'Component Number'])['Jan/2019', 'Feb/2019', 'Mar/2019', 'Apr/2019', 'May/2019', 'Jun/2019', 'Jul/2019', 'Aug/2019', 'Sep/2019', 'Oct/2019', 'Nov/2019', 'Dec/2019'].apply(lambda x: x.astype(int).sum())


df2.to_csv(DataPoint.PATH_DataFiles + "\\EPU_SPLIT_consolidated_by_highest_volume_provider.csv", sep='\t')

df3.to_csv(DataPoint.PATH_DataFiles + "\\EPU_SPLIT_consolidated_by_sum_of_volume_by_part_number_provider.csv", sep='\t')

df4.to_csv(DataPoint.PATH_DataFiles + "\\EPU_SPLIT_consolidated_by_sum_of_volume_by_part_number_and_saa_provider.csv", sep='\t')

print(df2.head())

# with open(DataPoint.PATH_DataFiles + "\\fuck.csv", "wb") as f:
#     writer = csv.writer(f, delimiter=",")
#     for df2_item in df2:
#         writer.writerow(df2_item)
