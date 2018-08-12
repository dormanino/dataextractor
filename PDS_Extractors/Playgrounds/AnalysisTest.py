import csv
import datetime
import json
import sys

from PDS_Extractors.Data.DataPoint import DataPoint
from PDS_Extractors.Helpers.MonthsHelper import MonthsHelper
from PDS_Extractors.Models.BaumusterCollection import BaumusterCollection
from PDS_Extractors.Models.BaumusterDataKind import BaumusterDataKind
from PDS_Extractors.Models.GroupingType import GroupingType
from PDS_Extractors.Models.Plant import Plant
from PDS_Extractors.Models.Production import Production
from PDS_Extractors.TechDocValidation.QVVCompositionValidator import QVVCompositionValidator

production = Production.from_dict(json.load(open(DataPoint.production)))
vehicles_sbc = BaumusterCollection.from_dict(json.load(open(DataPoint.data_vehicles_sbc)))
aggregates_sbc = BaumusterCollection.from_dict(json.load(open(DataPoint.data_aggregates_sbc)))
vehicles_jdf = BaumusterCollection.from_dict(json.load(open(DataPoint.data_vehicles_jdf)))
aggregates_jdf = BaumusterCollection.from_dict(json.load(open(DataPoint.data_aggregates_jdf)))

# Safe checks
if (vehicles_sbc.kind is not BaumusterDataKind.Vehicle or vehicles_sbc.plant is not Plant.SBC) \
        or (aggregates_sbc.kind is not BaumusterDataKind.Aggregate or aggregates_sbc.plant is not Plant.SBC) \
        or (vehicles_jdf.kind is not BaumusterDataKind.Vehicle or vehicles_jdf.plant is not Plant.JDF) \
        or (aggregates_jdf.kind is not BaumusterDataKind.Aggregate or aggregates_jdf.plant is not Plant.JDF):
    print("Bad data!")
    sys.exit()

JDF_Families = ["Actros"]
cabin_bms = ["D979820", "D979811", "D960840", "D960820", "D943899", "D958860", "D958870", "D958880"]

data_lines = []
saa_set = set()
a_pn_set = set()
# For each month of production
production_months = ["jan", "fev", "mar", "abr", "mai", "jun", "jul", "ago", "set", "out", "nov", "dez"]
for monthly_production in list(filter(lambda x: x.month in production_months, production.monthly_production_list)):
    year = production.year
    month = MonthsHelper.numeric[monthly_production.month]
    ref_date = datetime.date(production.year, month, 1)

    # Do analysis for each QVV production
    for qvv_prod in monthly_production.qvv_production_list:
        valid_regs = dict()

        # Pick the right vehicle data source based on family
        if qvv_prod.family in JDF_Families:
            vehicles_source = vehicles_jdf
        else:
            vehicles_source = vehicles_sbc

        # Find the Baumuster for Vehicle
        vehicle_bm = next(filter(lambda x: x.bm == qvv_prod.bm, vehicles_source.bm_data_list), None)
        if vehicle_bm is None:
            print("Couldn't find Vehicle Baumuster " + qvv_prod.bm)
            continue

        # Get SAA/LEG/General
        for grouping_type in [GroupingType.SAA, GroupingType.LEG, GroupingType.General]:
            grouping_name = grouping_type.name
            valid_regs[grouping_name] = QVVCompositionValidator.validate(vehicle_bm, ref_date, grouping_type, qvv_prod.composition)

        # Find the Aggregates for Vehicle
        for aggregate in QVVCompositionValidator.validate(vehicle_bm, ref_date, GroupingType.Aggregate, qvv_prod.composition):
            aggr_abm_saa = aggregate.clean_abm_saa

            # Pick the right aggregate data source
            if aggr_abm_saa in cabin_bms:
                first_main_aggr_source = aggregates_jdf
                second_main_aggr_source = aggregates_sbc
                code_to_disconsider = 'ZJ4'
                first_aggr_bm = next(filter(lambda x: x.bm == aggr_abm_saa, first_main_aggr_source.bm_data_list), None)
                second_aggr_bm = next(filter(lambda x: x.bm == aggr_abm_saa, second_main_aggr_source.bm_data_list), None)
                agg_base_list = (first_aggr_bm, first_main_aggr_source), (second_aggr_bm, second_main_aggr_source)

                for item in agg_base_list:
                    if item[0] is not None:
                        aggr_bm = next(filter(lambda x: x.bm == aggr_abm_saa, item[1].bm_data_list), None)
                    if item[0] is None:
                        print("Couldn't find Aggregate Baumuster " + aggr_abm_saa)
                        continue

                    qvv_cabin_code_removed = qvv_prod.composition
                    if code_to_disconsider in qvv_cabin_code_removed:
                        qvv_cabin_code_removed.remove(code_to_disconsider)

                    for grouping_type in [GroupingType.SAA, GroupingType.LEG, GroupingType.General]:
                        grouping_name = "Aggr " + grouping_type.name + " " + aggr_abm_saa
                        if grouping_name in valid_regs.keys():
                            valid_regs[grouping_name].extend(QVVCompositionValidator.validate(item[0], ref_date, grouping_type, qvv_cabin_code_removed))
                        else:
                            valid_regs[grouping_name] = QVVCompositionValidator.validate(item[0], ref_date, grouping_type, qvv_cabin_code_removed)
                    continue
            else:
                main_aggr_source = aggregates_sbc
                fallback_aggr_source = aggregates_jdf

                # Find the Baumuster for Aggregate
                aggr_bm = next(filter(lambda x: x.bm == aggr_abm_saa, main_aggr_source.bm_data_list), None)
                if aggr_bm is None and fallback_aggr_source is not None:  # search in fallback
                    aggr_bm = next(filter(lambda x: x.bm == aggr_abm_saa, fallback_aggr_source.bm_data_list), None)
                if aggr_bm is None:
                    print("Couldn't find Aggregate Baumuster " + aggr_abm_saa)
                    continue

                # Get SAA/LEG/General from Aggregates
                for grouping_type in [GroupingType.SAA, GroupingType.LEG, GroupingType.General]:
                    grouping_name = "Aggr " + grouping_type.name + " " + aggr_abm_saa
                    valid_regs[grouping_name] = QVVCompositionValidator.validate(aggr_bm, ref_date, grouping_type, qvv_prod.composition)

        # Append data line
        # append saa's into a set for further analysis
        for grouping, registers in valid_regs.items():
            for register in registers:
                clean = register.abm_saa
                for char in [' ', '.', '/', ',']:
                    clean = clean.replace(char, "")
                if str(clean)[0] == 'Z':
                    saa_set.add((register.abm_saa, clean))
                elif str(clean)[0] == 'A':
                    a_pn_set.add((register.abm_saa, clean))  # TODO: include json
                data_lines.append([
                    MonthsHelper.english[monthly_production.month] + '/' + str(production.year),
                    qvv_prod.qvv,
                    qvv_prod.bm,
                    qvv_prod.family,
                    qvv_prod.bu,
                    qvv_prod.volume,
                    register.abm_saa,
                    register.anz,
                    register.em_ab,
                    register.t_a,
                    register.em_bis,
                    register.t_b,
                    register.codebedingungen,
                    grouping
                ])

saa_set_list = list(saa_set)
saa_set_list = sorted(saa_set_list, key=lambda x: x)
with open(DataPoint.PATH_DataFiles + '\\saa_set.json', 'w+') as f:
    json.dump(saa_set_list, f, indent=4, sort_keys=False, ensure_ascii=False)

# Write the file
filename = DataPoint.PATH_DataFiles + '\\analysis_test.csv'
outputFile = open(filename, "w", newline="\n")
outputWriter = csv.writer(outputFile)
# outputWriter.writerow(["sep=,"])  # hack to enforce coma separator
outputWriter.writerow(["Date", "QVV", "Baumuster", "Vehicle Family", "Business Unit", "Volume",
                        "SAA", "Amount of assembly turns for given SAA", "Pem AB", "Termin AB",
                        "Pem BIS", "Termin BIS", "Codebedingungen", "Type"])

for data_line in data_lines:
    outputWriter.writerow(data_line)

outputFile.close()

print("Done!")
