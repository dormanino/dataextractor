dict0 = {'fear': [1, 2, 3, 4], 'no': 0}
lista = [1, 2, 3, 4, 5]

for key, val in dict0.items():
    if 'no' in dict0:
        dict0['no'] = [dict0['no'], 'youfuck']
    print(key, val)
