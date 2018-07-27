matrixo1 = [['1', '2', '3'], ['4', '5', '6']]
matrixo = [['', '', ''], ['', '', '']]
dicto = {0: 'a', 1: 'b', 2: 'c'}
dicto2 = {1: 'd', 2: 'e', 3: 'f'}
dicto3 = {0: 'a', 1: 'b', 2: 'c', 3: 'a', 4: 'b', 5: 'c', 6: 'a', 7: 'b', 8: 'c', 9: 'a', 10: 'b', 11: 'c'}


def create_matrix(data1, data2):
    return [([''] * data1)] * data2


for i, j in dicto3.items():
    matrixo2[0][i] = j


for item in matrixo1:
    print(item[0])

for i, j in dicto.items():
    matrixo[0][i] = j

print(matrixo)
