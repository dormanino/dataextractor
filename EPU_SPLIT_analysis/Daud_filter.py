from PDS_Extractors.Data.DataPoint import DataPoint
import pandas as pd


def litering(string):
    string_swaps = string[:1] + " " + string[1:]
    string_swaps = string_swaps[:5] + " " + string_swaps[5:]
    string_swaps = string_swaps[:9] + " " + string_swaps[9:]
    string_swaps = string_swaps[:12] + " " + string_swaps[12:]
    return string_swaps


df = pd.read_csv(DataPoint.data_EPU_SPLIT, low_memory=False)
with open('items_daud.csv', 'r+') as file:
    daud_data = list()
    for line in file:
        new_pn = line.rstrip('\n')
        new_pn = litering(new_pn)
        daud_data.append(new_pn)

print(df.head())

daud_df = df[df['Part Number'].isin(daud_data)]

print(daud_df.head())

months_header = ['Jan/2019', 'Feb/2019', 'Mar/2019', 'Apr/2019', 'May/2019', 'Jun/2019', 'Jul/2019', 'Aug/2019', 'Sep/2019', 'Oct/2019', 'Nov/2019', 'Dec/2019']
# dates_headers = list(df.columns.values)
daud_df['sum'] = daud_df[months_header].sum(axis=1)
# df2 = daud_df.loc[daud_df.reset_index().groupby(['Part Number'])['sum'].idxmax()]
df3 = daud_df.groupby(['Part Number'])['Jan/2019', 'Feb/2019', 'Mar/2019', 'Apr/2019', 'May/2019', 'Jun/2019', 'Jul/2019', 'Aug/2019', 'Sep/2019', 'Oct/2019', 'Nov/2019', 'Dec/2019'].apply(lambda x: x.astype(int).sum())
df4 = daud_df.groupby(['Part Number', 'Component Number'])['Jan/2019', 'Feb/2019', 'Mar/2019', 'Apr/2019', 'May/2019', 'Jun/2019', 'Jul/2019', 'Aug/2019', 'Sep/2019', 'Oct/2019', 'Nov/2019', 'Dec/2019'].apply(lambda x: x.astype(int).sum())

daud_df.to_csv(DataPoint.PATH_DataFiles + "\\Daud_volume_by_part_number_provider.csv", sep=',')

# df2.to_csv(DataPoint.PATH_DataFiles + "\\Daud_consolidated_by_highest_volume_provider.csv", sep='\t')

df3.to_csv(DataPoint.PATH_DataFiles + "\\Daud_consolidated_by_sum_of_volume_by_part_number_provider.csv", sep=',')

df4.to_csv(DataPoint.PATH_DataFiles + "\\Daud_consolidated_by_sum_of_volume_by_part_number_and_saa_provider.csv", sep=',')

# with open(DataPoint.PATH_DataFiles + "\\fuck.csv", "wb") as f:
#     writer = csv.writer(f, delimiter=",")
#     for df2_item in df2:
#         writer.writerow(df2_item)



