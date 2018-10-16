from PDS_Extractors.Data.DataPoint import DataPoint
import pandas as pd

df = pd.read_csv(DataPoint.data_EPU_SPLIT, low_memory=False)
col_names = list(df.columns.values)
col_to_sum = ['Jan/2019', 'Feb/2019', 'Mar/2019', 'Apr/2019', 'May/2019', 'Jun/2019', 'Jul/2019', 'Aug/2019', 'Sep/2019', 'Oct/2019', 'Nov/2019', 'Dec/2019']
df['sum'] = df[col_to_sum].sum(axis=1)
df.set_index(['Part Number'])
print(col_names)
print(df.head())
