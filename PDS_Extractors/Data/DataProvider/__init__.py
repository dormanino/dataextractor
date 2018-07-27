import json
import LatestFileVersion
import datetime
from PDS_Extractors.Data.DataPoint import DataPoint
import collections


class DataProvider:

    @staticmethod
    def agrmz():
        # TODO: clean
        agrmz_file = LatestFileVersion.latest_file_version('json', 'PDS_KGS_AGRMZ',
                                                           current='C:\\Users\\SubarFernanOlivera\\PycharmProjects'
                                                                   '\\DataExtractor\\PDS_Extractors')

        # agrmz_file = LatestFileVersion.latest_file_version('json', 'PDS_KGS_AGRMZ',
        #                                                       current='C:\\Users\\vravagn\\PycharmProjects'
        #                                                       '\\DataExtractor\\PDS_Extractors')

        data_json = json.load(open(agrmz_file))

        swap_list = []
        swap_string = ''
        counter = 0
        i = 0
        pos_first_register_data = ''
        asa_ab_first_register_data = ''

        while i < len(data_json):

            if data_json[i]['data'][1] == '_' and counter is 0:  # reached a start of register

                swap_string += data_json[i]['data']  # include data on swap
                pos_first_register_data = data_json[i]['data'][39:42]  # pos (39, 42)
                asa_ab_first_register_data = data_json[i]['data'][55:58]  # asa_ab (55, 58)
            elif data_json[i]['data'][1] == '_' and counter is not 0:

                # check if the next register has the same content from previous
                pos_next_register_data = data_json[i]['data'][39:42]  # pos (39, 42)
                asa_ab_next_register_data = data_json[i]['data'][55:58]  # asa_ab (55, 58)

                if pos_first_register_data == pos_next_register_data and asa_ab_first_register_data == asa_ab_next_register_data:
                    counter += 1
                    i += 2
                    continue
                else:
                    swap_list.append(swap_string)
                    swap_string = ''
                    counter = 0  # restart counter with current line data for further correct analysis
                    continue
            else:
                counter += 1
                swap_string += data_json[i]['data']

            if i < len(data_json):  # advance line if  less then allowed range
                i += 1

        date = datetime.date.today()
        date_string = date.strftime('%y%m%d')

        with open(date_string + 'PDS_KGS_AGR_test.json', 'w', encoding='utf-8') as f:
            json.dump(swap_list, f, indent=4, sort_keys=True, ensure_ascii=False)

        slices = {
            1: {
                'abm_saa': (3, 23),
                'la': (23, 25),
                'lt': (26, 27),
                'bu_su': (29, 38),
                'pos': (39, 42),
                'hwa': (43, 47),
                'sp': (48, 50),
                'r': (51, 52),
                'p': (53, 54),
                'asa': (55, 58),
                'em_ab': (61, 67),
                'em_bis': (72, 79)
            },
            2: {
                'benennung': (3, 54),
                'asb': (55, 58),
                'trailing_t_ab': (62, 63),
                't_a': (63, 69),
                'trailing_t_bis': (73, 74),
                't_b': (74, 80)
            },
            3: {
                'vkfbez': (3, 55),
                'anz': (55, 58)
            },
            4: {
                'bg': (24, 26),
                'code': (28, 62)
            },
            5: {
                'bg': (23, 25),
                'code': (25, 80)
            },
            6: {
                'ZUSTEUERBED': (25, 80)
            },
            7: {
                'VERW.-ST': (13, 16),
                'VERW_Info': (16, 80)
            }
        }
        # ranges = [(int(r[0]), int(r[1])) for r in [s.split(':') for s in [slice_of_ranges.items() in [i in slices]]]]
        # TODO split codes, saas and bm's in separate files
        register = 0
        register_dict = {}

        for full_line in swap_list:

            amount_of_lines = int(len(full_line) / 80)  # finds the amount of data in the register (each line has 80 char)
            register_dict[register] = {}
            marker = False
            prior_substring = ''
            next_substring = ''
            analised_lines = []

            for line in range(1, amount_of_lines + 1):

                end_char = line * 80  # used to specify first char if the line to identify
                start_char = end_char - 80  # same idea as former but for the last char
                substring = full_line[start_char:end_char + 1]  # establish the sub range to parse

                if line > 1:
                    prior_line = line - 1
                    prior_end_char = prior_line * 80
                    prior_start_char = prior_end_char - 80
                    prior_substring = full_line[prior_start_char:prior_end_char + 1]

                if line < amount_of_lines:
                    next_line = line + 1
                    next_end_char = next_line * 80
                    next_start_char = next_end_char - 80
                    next_substring = full_line[next_start_char:next_end_char + 1]

                # in slices[line], the trigger line calls the slice and the dictionary key corresponding
                # for q, r in zip(slices[line].keys(), slices[line].values()):
                #     print(q, '----', r)

                if '_' in substring[1]:  # if the line is the first register

                    for q, r in zip(slices[1].keys(), slices[1].values()):
                        data = substring[r[0]:r[1]].strip()
                        if data == '':
                            data = None
                        register_dict[register].update({q: data})
                    analised_lines.append(line)

                elif not prior_substring.strip() == '' and '_' in prior_substring[1]:  # defines if you are in between the register header and

                    for q_1, r_1 in zip(slices[2].keys(), slices[2].values()):
                        data = substring[r_1[0]:r_1[1]].strip()
                        if data == '':
                            data = None
                        register_dict[register].update({q_1: data})
                    analised_lines.append(line)

                    if 'BG/BAUBARKEITSBED' not in next_substring and\
                            'BG/CODEBEDINGUNGEN' not in next_substring and\
                            'PB/ZUSTEUERBED' not in next_substring and\
                            'VERW.-ST' not in next_substring:
                        marker = True
                    else:
                        marker = False

                elif marker:

                    for q, r in zip(slices[3].keys(), slices[3].values()):
                        data = substring[r[0]:r[1]].strip()
                        if data == '':
                            data = None
                        register_dict[register].update({q: data})
                    analised_lines.append(line)
                    marker = False

                elif 'BG/CODEBEDINGUNGEN :' in substring:

                    dicto_CODEBEDINGUNGEN = slices[4]
                    dicto_data_0_CODEBEDINGUNGEN = dicto_CODEBEDINGUNGEN['bg']
                    dicto_data_1_CODEBEDINGUNGEN = dicto_CODEBEDINGUNGEN['code']
                    next_line_CODEBEDINGUNGEN = line

                    if substring[dicto_data_0_CODEBEDINGUNGEN[0]: dicto_data_0_CODEBEDINGUNGEN[1]].strip() == '':
                        bg_CODEBEDINGUNGEN = None
                    else:
                        bg_CODEBEDINGUNGEN = substring[dicto_data_0_CODEBEDINGUNGEN[0]: dicto_data_0_CODEBEDINGUNGEN[1]]

                    restriction_CODEBEDINGUNGEN = substring[dicto_data_1_CODEBEDINGUNGEN[0]: dicto_data_1_CODEBEDINGUNGEN[1]].strip()

                    if ';' not in restriction_CODEBEDINGUNGEN:
                        eof_CODEBEDINGUNGEN = False
                        next_line_CODEBEDINGUNGEN += 1
                    else:
                        eof_CODEBEDINGUNGEN = True

                    while not eof_CODEBEDINGUNGEN:
                        next_end_char_CODEBEDINGUNGEN = next_line_CODEBEDINGUNGEN * 80
                        next_start_char_CODEBEDINGUNGEN = next_end_char_CODEBEDINGUNGEN - 80
                        next_substring_CODEBEDINGUNGEN = full_line[next_start_char_CODEBEDINGUNGEN:next_end_char_CODEBEDINGUNGEN + 1]
                        next_substring_anal_CODEBEDINGUNGEN = next_substring_CODEBEDINGUNGEN[dicto_data_1_CODEBEDINGUNGEN[0]: dicto_data_1_CODEBEDINGUNGEN[1]].strip()
                        restriction_CODEBEDINGUNGEN = restriction_CODEBEDINGUNGEN + next_substring_anal_CODEBEDINGUNGEN
                        analised_lines.append(next_line_CODEBEDINGUNGEN)
                        if ';' not in next_substring_anal_CODEBEDINGUNGEN:
                            eof_CODEBEDINGUNGEN = False
                            next_line_CODEBEDINGUNGEN += 1
                        else:
                            eof_CODEBEDINGUNGEN = True

                    restriction_CODEBEDINGUNGEN = restriction_CODEBEDINGUNGEN.replace(' ', '')

                    register_dict[register].update({'bg_CODEBEDINGUNGEN': bg_CODEBEDINGUNGEN})
                    register_dict[register].update({'CODEBEDINGUNGEN': restriction_CODEBEDINGUNGEN})
                    analised_lines.append(line)

                elif 'BG/BAUBARKEITSBED' in substring:

                    dicto_BAUBARKEITSBED = slices[5]
                    dicto_data_0_BAUBARKEITSBED = dicto_BAUBARKEITSBED['bg']  # tuple
                    dicto_data_1_BAUBARKEITSBED = dicto_BAUBARKEITSBED['code']  # tuple
                    data_BAUBARKEITSBED = substring[dicto_data_1_BAUBARKEITSBED[0]:dicto_data_1_BAUBARKEITSBED[1]]  # codes data
                    next_line_BAUBARKEITSBED = line

                    if substring[dicto_data_0_BAUBARKEITSBED[0]: dicto_data_0_BAUBARKEITSBED[1]].strip() == '':
                        bg_BAUBARKEITSBED = None
                    else:
                        bg_BAUBARKEITSBED = substring[dicto_data_0_BAUBARKEITSBED[0]: dicto_data_0_BAUBARKEITSBED[1]]

                    restriction_BAUBARKEITSBED = substring[dicto_data_1_BAUBARKEITSBED[0]: dicto_data_1_BAUBARKEITSBED[1]].strip()

                    if ';' not in restriction_BAUBARKEITSBED:
                        eof_BAUBARKEITSBED = False
                        next_line_BAUBARKEITSBED += 1

                    else:
                        eof_BAUBARKEITSBED = True

                    while not eof_BAUBARKEITSBED:
                        next_end_char_BAUBARKEITSBED = next_line_BAUBARKEITSBED * 80
                        next_start_char_BAUBARKEITSBED = next_end_char_BAUBARKEITSBED - 80
                        next_substring_BAUBARKEITSBED = full_line[next_start_char_BAUBARKEITSBED:next_end_char_BAUBARKEITSBED + 1]
                        next_substring_anal_BAUBARKEITSBED = next_substring_BAUBARKEITSBED[dicto_data_1_BAUBARKEITSBED[0]: dicto_data_1_BAUBARKEITSBED[1]]
                        restriction_BAUBARKEITSBED = restriction_BAUBARKEITSBED + next_substring_anal_BAUBARKEITSBED
                        analised_lines.append(next_line_BAUBARKEITSBED)

                        if ';' not in next_substring_anal_BAUBARKEITSBED:
                            eof_BAUBARKEITSBED = False
                            next_line_BAUBARKEITSBED += 1
                        else:
                            eof_BAUBARKEITSBED = True

                    restriction_BAUBARKEITSBED = restriction_BAUBARKEITSBED.replace(' ', '')

                    register_dict[register].update({'bg_BAUBARKEITSBED': bg_BAUBARKEITSBED})
                    register_dict[register].update({'BAUBARKEITSBED': restriction_BAUBARKEITSBED})
                    analised_lines.append(line)

                elif 'PB/ZUSTEUERBED' in substring:
                    dicto_ZUSTEUERBED = slices[6]
                    dicto_data_ZUSTEUERBED = dicto_ZUSTEUERBED['ZUSTEUERBED']  # tuple
                    data_ZUSTEUERBED = substring[dicto_data_ZUSTEUERBED[0]:dicto_data_ZUSTEUERBED[1]]  # codes data
                    next_line_ZUSTEUERBED = line

                    restriction_ZUSTEUERBED = substring[dicto_data_ZUSTEUERBED[0]: dicto_data_ZUSTEUERBED[1]].strip()

                    if ';' not in restriction_ZUSTEUERBED:
                        eof_ZUSTEUERBED = False
                        next_line_ZUSTEUERBED += 1
                    else:
                        eof_ZUSTEUERBED = True

                    while not eof_ZUSTEUERBED:
                        next_end_char_ZUSTEUERBED = next_line_ZUSTEUERBED * 80
                        next_start_char_ZUSTEUERBED = next_end_char_ZUSTEUERBED - 80
                        next_substring_ZUSTEUERBED = full_line[next_start_char_ZUSTEUERBED:next_end_char_ZUSTEUERBED + 1]
                        next_substring_anal_ZUSTEUERBED = next_substring_ZUSTEUERBED[dicto_data_ZUSTEUERBED[0]: dicto_data_ZUSTEUERBED[1]].strip()
                        restriction_ZUSTEUERBED = restriction_ZUSTEUERBED + next_substring_anal_ZUSTEUERBED
                        analised_lines.append(next_line_ZUSTEUERBED)
                        if ';' not in next_substring_anal_ZUSTEUERBED:
                            eof_ZUSTEUERBED = False
                            next_line_ZUSTEUERBED += 1
                        else:
                            eof_ZUSTEUERBED = True

                    restriction_ZUSTEUERBED = restriction_ZUSTEUERBED.replace(' ', '')

                    register_dict[register].update({'ZUSTEUERBED': restriction_ZUSTEUERBED})

                    analised_lines.append(line)

                elif 'VERW.-ST.:' in substring:
                    dicto_VERW = slices[7]
                    dicto_0_data_VERW = dicto_VERW['VERW.-ST']  # tuple
                    dicto_1_data_VERW = dicto_VERW['VERW_Info']  # tuple
                    data_0_VERW = substring[dicto_0_data_VERW[0]:dicto_0_data_VERW[1]].strip()
                    data_1_VERW = substring[dicto_1_data_VERW[0]:dicto_1_data_VERW[1]].strip()
                    next_line_VERW = line
                    if line == amount_of_lines:
                        if data_0_VERW == '':
                            data_0_VERW = None
                        if data_1_VERW == '':
                            data_1_VERW = None

                        register_dict[register].update({'VERW.-ST': data_0_VERW})
                        register_dict[register].update({'VERW_Info': data_1_VERW})
                    else:
                        x = 1
                        pass  # TODO: make logic for

                    analised_lines.append(line)

                elif line not in analised_lines:
                    register_dict[register].update({'extra_info': substring.strip()})

            register += 1

        with open(date_string + 'PDS_KGS_AGR_final.json', 'w', encoding='utf-8') as f:
            json.dump(register_dict, f, indent=4, sort_keys=True, ensure_ascii=False)

            # data = {p: [v, None][v.isspace()] for p, v in [(p, substring[r[0]:r[1]]), r in slices[line].values()]}
            # params = [data_list[arg] if arg in data else None for arg in inspect.getfullargspec(PdsAGRMZDataModels).args[1:]]
            # agr = PdsAGRMZDataModels(*params)
        return print('concluded')

    @staticmethod
    def all_codes():
        all_codes_file = LatestFileVersion.latest_file_version('json', '_PDS_0E',
                                                               current='C:\\Users\\vravagn\\PycharmProjects\\DataExtractor\\PDS_Extractors')
        data_json = json.load(open(all_codes_file))
        all_code_list = []
        for item in data_json:
            all_code_list.append(item['text'][3:33].strip().replace(' ', ''))

        return all_code_list

    @staticmethod
    def acc():
        raw_acc_data = DataPoint.data_acc  # dict
        print(raw_acc_data, type(raw_acc_data))
        acc_dict = json.load(open(raw_acc_data))

        slices = {
            1: {
                'CU': (3, 14),  # ok
                'POS': (14, 18),   # ok
                'LA': (18, 21),  # ok
                'SP': (21, 24),  # ok
                'code_bed': (24, 54),  # ok
                'asa': (55, 59),  # ok
                'em-ab': (61, 67),
                'em-bis': (72, 78)
            },
            2: {
                'RF': (18, 21),  # ok
                'PG': (21, 24),  # ok
                'code_bed': (24, 54),  # ok
                'asb': (55, 59),  # ok
                't-a_kz': (62, 63),
                't-a': (63, 69),
                't-b_kz': (73, 74),
                't-b': (74, 80)
            },
            3: {
                'code_bed': (24, 54)
            }
        }

        register = 0
        register_dict = {}
        dict_acc = {}
        for key, value in acc_dict.items():
            amount_of_items = len(value)
            swap_line = ''
            full_lines = []
            for i, line in enumerate(value):
                swap_line += str(line)
                if i == (amount_of_items - 1) or value[i + 1][1] == '_':
                    full_lines.append(str(swap_line))
                    swap_line = ''
            dict_acc[key] = full_lines

        for code, lines in dict_acc.items():
            register_dict[code] = {}
            reg_counter = 0
            for full_line in lines:
                reg_counter += 1
                register_dict[code][reg_counter] = {}
                amount_of_lines = int(len(full_line) / 80)  # finds the amount of data in the register (each line has 80 char)
                marker = False
                prior_substring = ''
                next_substring = ''
                analised_lines = []
                for line in range(1, amount_of_lines + 1):
                    end_char = line * 80  # used to specify first char if the line to identify
                    start_char = end_char - 80  # same idea as former but for the last char
                    substring = full_line[start_char:end_char + 1]  # establish the sub range to parse
                    if line > 1:
                        prior_line = line - 1
                        prior_end_char = prior_line * 80
                        prior_start_char = prior_end_char - 80
                        prior_substring = full_line[prior_start_char:prior_end_char + 1]

                    if line < amount_of_lines:
                        next_line = line + 1
                        next_end_char = next_line * 80
                        next_start_char = next_end_char - 80
                        next_substring = full_line[next_start_char:next_end_char + 1]

                    if '_' in substring[1]:
                        for q, r in zip(slices[1].keys(), slices[1].values()):
                            data = substring[r[0]:r[1]].strip()
                            if q == 'code_bed':
                                data.replace (' ', '')
                            if data == '':
                                data = None
                            if q not in register_dict[code][reg_counter]:
                                register_dict[code][reg_counter].update({q: data})
                            else:
                                register_dict[code][reg_counter][q] = data

                        analised_lines.append(line)

                    elif not prior_substring.strip() == '' and '_' in prior_substring[1]:  # defines if you are in between the register header and

                        for q_1, r_1 in zip(slices[2].keys(), slices[2].values()):
                            data = substring[r_1[0]:r_1[1]].strip()
                            if q_1 == 'code_bed':
                                data.replace (' ', '')
                            if data == '':
                                data = None
                            if q_1 not in register_dict[code][reg_counter]:
                                register_dict[code][reg_counter].update({q_1: data})
                            else:
                                if data:
                                    register_dict[code][reg_counter][q_1] += data
                        analised_lines.append(line)
                    else:
                        for q_2, r_2 in zip(slices[3].keys(), slices[3].values()):
                            data = substring[r_2[0]:r_2[1]].strip()
                            if q_2 == 'code_bed':
                                data.replace(' ', '')
                            if data == '':  ## if the line does not have information, None cant be added
                                data = None
                            if q_2 not in register_dict[code][reg_counter]:
                                register_dict[code][reg_counter].update({q_2: data})
                            else:
                                if data:
                                    register_dict[code][reg_counter][q_2] += data
                            analised_lines.append(line)
        with open('PDS_ACC_final.json', 'w', encoding='utf-8') as f:
            json.dump(register_dict, f, indent=4, sort_keys=True, ensure_ascii=False)

DataProvider.acc()
