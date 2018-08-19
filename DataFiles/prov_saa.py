import json
import csv
import os

tres_ca_file = json.load(open(os.getcwd()+'\\180815_jdf_3ca_parsed_final.json', encoding='utf-8'))
saa_data = tres_ca_file['data']
list_final = []
for saa in saa_data:
    regs = saa['regs']
    for r in regs:
        if r:
            list_final.append((saa['source'], r['part_number'], r['r'], r['bza'], r['quantity'], r['da'], r['em-ab'],
                               r['em-bis'], r['t_a'], r['t_b'], r['ehm'], r['w']))
        else:
            list_final.append((saa['source'], 'empty'))

filename = os.getcwd() + '\\3ca_jdf_analysis_test.csv'
output_file = open(filename, "w", newline="\n")
output_writer = csv.writer(output_file)
# output_writer.writerow(["sep=,"])  # hack to enforce coma separator
output_writer.writerow(["saa", "part_number", "grau_maturidade", "mod. fornec.", "qt", "da",
                        "apa_de", "apa_ate", "pzo_de", "pzo_ate", "unidade", "opc"])

for data_line in list_final:
    output_writer.writerow(data_line)

output_file.close()

tres_ca_file = json.load(open(os.getcwd()+'\\180813_sbc_3ca_parsed_final.json', encoding='utf-8'))
saa_data = tres_ca_file['data']
list_final = []
for saa in saa_data:
    regs = saa['regs']
    for r in regs:
        if r:
            list_final.append((saa['source'], r['part_number'], r['r'], r['bza'], r['quantity'], r['da'], r['em-ab'],
                               r['em-bis'], r['t_a'], r['t_b'], r['ehm'], r['w']))
        else:
            list_final.append((saa['source'], 'empty'))

filename = os.getcwd() + '\\3ca_sbc_analysis_test.csv'
output_file = open(filename, "w", newline="\n")
output_writer = csv.writer(output_file)
# output_writer.writerow(["sep=,"])  # hack to enforce coma separator
output_writer.writerow(["saa", "part_number", "grau_maturidade", "mod. fornec.", "qt", "da",
                        "apa_de", "apa_ate", "pzo_de", "pzo_ate", "unidade", "opc"])

for data_line in list_final:
    output_writer.writerow(data_line)

output_file.close()
