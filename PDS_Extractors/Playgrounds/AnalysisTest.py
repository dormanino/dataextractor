import csv
import datetime
import json
import sys

from PDS_Extractors.Data.DataPoint import DataPoint
from PDS_Extractors.Models.BaumusterCollection import BaumusterCollection
from PDS_Extractors.Models.BaumusterDataSource import BaumusterDataSource
from PDS_Extractors.Models.IDKKind import IDKKind
from PDS_Extractors.Models.Production import Production
from PDS_Extractors.TechDocValidation.CodeRuleValidator import CodeRuleValidator
from PDS_Extractors.TechDocValidation.SAAValidator import SAAValidator

vehicles_data = json.load(open(DataPoint.data_agrmz_vehicles))
aggregates_data = json.load(open(DataPoint.data_agrmz_aggregates))
production_data = json.load(open(DataPoint.production))

vehicles = BaumusterCollection.from_dict(vehicles_data)
aggregates = BaumusterCollection.from_dict(aggregates_data)
production = Production.from_dict(production_data)

# safe checks
if vehicles.source is not BaumusterDataSource.Vehicle or aggregates.source is not BaumusterDataSource.Aggregate:
    print("Bad data!")
    sys.exit()

months = dict(jan=1, fev=2, mar=3, abr=4, mai=5, jun=6,
              jul=7, ago=8, set=9, out=10, nov=11, dez=12)

result = []
production_year = 2018
production_months = ["jan", "fev", "mar", "abr", "mai", "jun", "jul", "ago", "set", "out", "nov", "dez"]
for monthly_production in list(filter(lambda x: x.month in production_months, production.monthly_production_list)):
    month = months[monthly_production.month]
    ref_date = datetime.date(production_year, month, 1)

    for qvv_production in monthly_production.qvv_production_list:
        bm = next(filter(lambda x: x.bm == qvv_production.bm, vehicles.bm_data_list), None)
        if bm is None:
            print(bm)
            continue
        # TODO: Reuse register already analyzed
        saa_registers = bm.extract_idk(IDKKind.SAA)
        if saa_registers is None:
            continue
        flattened_saas = saa_registers.flattened_registers()
        valid_saas = list(filter(lambda x: SAAValidator.saa_status_on_date(x, ref_date).is_valid(), flattened_saas))
        for register in filter(lambda x: x.codebedingungen is not None, valid_saas):
            code_rule_is_valid = CodeRuleValidator.validate(register.codebedingungen, valid_saas)

            result.append([
                monthly_production.month,
                qvv_production.qvv,
                qvv_production.bm,
                qvv_production.family,
                qvv_production.bu,
                qvv_production.volume,
                register.abm_saa,
                register.anz,
                register.em_ab,
                register.t_a,
                register.em_bis,
                register.t_b,
                register.codebedingungen,
                code_rule_is_valid
            ])

# Write the file
filename = DataPoint.PATH_DataFiles + '\\analysis_test.csv'
outputFile = open(filename, "w", newline="\n")
outputWriter = csv.writer(outputFile)
outputWriter.writerow(["sep=,"])  # hack to enforce coma separator
outputWriter.writerow(["mes", "qvv", "bm", "veh.family", "business_unit", "volume", "abm_saa", "anz",
                       "em_ab", "t_a", "em_bis", "t_b", "codebedingungen", "is_valid"])
for data_line in result:
    outputWriter.writerow(data_line)
outputFile.close()

print("Done!")
