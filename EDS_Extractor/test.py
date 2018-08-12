import os

with open(os.getcwd() + '\\data.csv', 'r') as file:
    data_partnumbers = [line.rstrip() for line in file.readlines()]

print(data_partnumbers)
