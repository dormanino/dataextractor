import json
import datetime
from PDS_Extractors.Data.DataPoint import DataPoint
from PDS_Extractors.Helpers.LatestFileVersion import LatestFileVersion


class DataProvider:

    @staticmethod
    def agrmz(source):
        complete_line = ''
        data_source = []
        curent_reg = ''
        bm = ''
        data_type = ''
        kg = ''
        none_flag = False

        lines_list = ""
        if source is 'vehicle':
            lines_list = json.load(open(DataPoint.data_agrmz_raw_vehicles))
        elif source is 'aggregate':
            lines_list = json.load(open(DataPoint.data_agrmz_raw_aggregates))

        for line_counter, line_info_dict in enumerate(lines_list):
            line = line_info_dict['data']
            if line is not None:
                register_char = line[1]
                if register_char is '_' and line_counter is not 0:  # start of register
                    if line != curent_reg and not none_flag:
                        data_source.append((bm, data_type, kg, complete_line))
                        complete_line = ''
                    else:
                        bm = line_info_dict['bm']
                        data_type = line_info_dict['data_type']
                        kg = line_info_dict['kg']
                        none_flag = False
                        complete_line = ''
                    curent_reg = line
                complete_line += line
                bm = line_info_dict['bm']
                data_type = line_info_dict['data_type']
                kg = line_info_dict['kg']
            else:
                data_source.append((bm, data_type, kg, complete_line))
                bm = line_info_dict['bm']
                data_source.append((bm, None, None, None))
                none_flag = True
                continue

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

        main_dict = dict(source=source, data=[])
        for data in data_source:

            # Find/Create Baumuster node
            info_bm = data[0]
            bm_data = next(filter(lambda i: i['bm'] == info_bm, main_dict["data"]), None)
            if bm_data is None:
                bm_data = dict(bm='', data=[])
                bm_data['bm'] = info_bm
                main_dict['data'].append(bm_data)

            info_data_input = data[1]
            if info_data_input is not None:
                print(data)

                # Find/Create Data Input node
                data_input = next(filter(lambda i: i['type'] == info_data_input, bm_data["data"]), None)
                if data_input is None:
                    data_input = dict(type='', data=[])
                    data_input['type'] = info_data_input
                    bm_data['data'].append(data_input)

                # Find/Create Grouping Input node
                info_grouping_input = data[2]
                grouping_input = next(filter(lambda i: i['kg'] == info_grouping_input, data_input["data"]), None)
                if grouping_input is None:
                    grouping_input = dict(kg="", regs=[])
                    grouping_input['kg'] = info_grouping_input
                    data_input['data'].append(grouping_input)

                full_line = data[3]
                amount_of_lines = int(len(full_line) / 80)  # finds the amount of data in the register (each line has 80 char)
                register = dict()
                marker = False
                prior_substring = ''
                next_substring = ''
                analysed_lines = []

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

                    if '_' in substring[1]:  # if the line is the first register
                        for q, r in zip(slices[1].keys(), slices[1].values()):
                            data = substring[r[0]:r[1]].strip()
                            if data == '':
                                data = None
                            register.update({q: data})
                        analysed_lines.append(line)

                    elif not prior_substring.strip() == '' and '_' in prior_substring[1]:  # defines if you are in between the register header and
                        for q_1, r_1 in zip(slices[2].keys(), slices[2].values()):
                            data = substring[r_1[0]:r_1[1]].strip()
                            if data == '':
                                data = None
                            register.update({q_1: data})
                        analysed_lines.append(line)

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
                            register.update({q: data})
                        analysed_lines.append(line)
                        marker = False

                    elif 'BG/CODEBEDINGUNGEN :' in substring:
                        dicto_codebedingungen = slices[4]
                        dicto_data_0_codebedingungen = dicto_codebedingungen['bg']
                        dicto_data_1_codebedingungen = dicto_codebedingungen['code']
                        next_line_codebedingungen = line

                        if substring[dicto_data_0_codebedingungen[0]: dicto_data_0_codebedingungen[1]].strip() == '':
                            bg_codebedingungen = None
                        else:
                            bg_codebedingungen = substring[dicto_data_0_codebedingungen[0]: dicto_data_0_codebedingungen[1]]

                        restriction_codebedingungen = substring[dicto_data_1_codebedingungen[0]: dicto_data_1_codebedingungen[1]].strip()

                        if ';' not in restriction_codebedingungen:
                            eof_codebedingungen = False
                            next_line_codebedingungen += 1
                        else:
                            eof_codebedingungen = True

                        while not eof_codebedingungen:
                            next_end_char_codebedingungen = next_line_codebedingungen * 80
                            next_start_char_codebedingungen = next_end_char_codebedingungen - 80
                            next_substring_codebedingungen = full_line[next_start_char_codebedingungen:next_end_char_codebedingungen + 1]
                            next_substring_anal_codebedingungen = next_substring_codebedingungen[dicto_data_1_codebedingungen[0]: dicto_data_1_codebedingungen[1]].strip()
                            restriction_codebedingungen = restriction_codebedingungen + next_substring_anal_codebedingungen
                            analysed_lines.append(next_line_codebedingungen)
                            if ';' not in next_substring_anal_codebedingungen:
                                eof_codebedingungen = False
                                next_line_codebedingungen += 1
                            else:
                                eof_codebedingungen = True

                        restriction_codebedingungen = restriction_codebedingungen.replace(' ', '')

                        register.update({'bg_codebedingungen': bg_codebedingungen})
                        register.update({'CODEBEDINGUNGEN': restriction_codebedingungen})
                        analysed_lines.append(line)

                    elif 'BG/BAUBARKEITSBED' in substring:

                        dicto_baubarkeitsbed = slices[5]
                        dicto_data_0_baubarkeitsbed = dicto_baubarkeitsbed['bg']  # tuple
                        dicto_data_1_baubarkeitsbed = dicto_baubarkeitsbed['code']  # tuple
                        data_baubarkeitsbed = substring[dicto_data_1_baubarkeitsbed[0]:dicto_data_1_baubarkeitsbed[1]]  # codes data
                        next_line_baubarkeitsbed = line

                        if substring[dicto_data_0_baubarkeitsbed[0]: dicto_data_0_baubarkeitsbed[1]].strip() == '':
                            bg_baubarkeitsbed = None
                        else:
                            bg_baubarkeitsbed = substring[dicto_data_0_baubarkeitsbed[0]: dicto_data_0_baubarkeitsbed[1]]

                        restriction_baubarkeitsbed = substring[dicto_data_1_baubarkeitsbed[0]: dicto_data_1_baubarkeitsbed[1]].strip()

                        if ';' not in restriction_baubarkeitsbed:
                            eof_baubarkeitsbed = False
                            next_line_baubarkeitsbed += 1

                        else:
                            eof_baubarkeitsbed = True

                        while not eof_baubarkeitsbed:
                            next_end_char_baubarkeitsbed = next_line_baubarkeitsbed * 80
                            next_start_char_baubarkeitsbed = next_end_char_baubarkeitsbed - 80
                            next_substring_baubarkeitsbed = full_line[next_start_char_baubarkeitsbed:next_end_char_baubarkeitsbed + 1]
                            next_substring_anal_baubarkeitsbed = next_substring_baubarkeitsbed[dicto_data_1_baubarkeitsbed[0]: dicto_data_1_baubarkeitsbed[1]]
                            restriction_baubarkeitsbed = restriction_baubarkeitsbed + next_substring_anal_baubarkeitsbed
                            analysed_lines.append(next_line_baubarkeitsbed)

                            if ';' not in next_substring_anal_baubarkeitsbed:
                                eof_baubarkeitsbed = False
                                next_line_baubarkeitsbed += 1
                            else:
                                eof_baubarkeitsbed = True

                                restriction_baubarkeitsbed = restriction_baubarkeitsbed.replace(' ', '')

                        register.update({'bg_baubarkeitsbed': bg_baubarkeitsbed})
                        register.update({'BAUBARKEITSBED': restriction_baubarkeitsbed})
                        analysed_lines.append(line)

                    elif 'PB/ZUSTEUERBED' in substring:
                        dicto_zusteuerbed = slices[6]
                        dicto_data_zusteuerbed = dicto_zusteuerbed['ZUSTEUERBED']  # tuple
                        data_zusteuerbed = substring[dicto_data_zusteuerbed[0]:dicto_data_zusteuerbed[1]]  # codes data
                        next_line_zusteuerbed = line

                        restriction_zusteuerbed = substring[dicto_data_zusteuerbed[0]: dicto_data_zusteuerbed[1]].strip()

                        if ';' not in restriction_zusteuerbed:
                            eof_zusteuerbed = False
                            next_line_zusteuerbed += 1
                        else:
                            eof_zusteuerbed = True

                        while not eof_zusteuerbed:

                            next_end_char_zusteuerbed = next_line_zusteuerbed * 80
                            next_start_char_zusteuerbed = next_end_char_zusteuerbed - 80
                            next_substring_zusteuerbed = full_line[next_start_char_zusteuerbed:next_end_char_zusteuerbed + 1]
                            next_substring_anal_zusteuerbed = next_substring_zusteuerbed[dicto_data_zusteuerbed[0]: dicto_data_zusteuerbed[1]].strip()
                            restriction_zusteuerbed = restriction_zusteuerbed + next_substring_anal_zusteuerbed
                            analysed_lines.append(next_line_zusteuerbed)

                            if ';' not in next_substring_anal_zusteuerbed:
                                eof_zusteuerbed = False
                                next_line_zusteuerbed += 1
                            else:
                                eof_zusteuerbed = True

                        restriction_zusteuerbed = restriction_zusteuerbed.replace(' ', '')
                        register.update({'ZUSTEUERBED': restriction_zusteuerbed})
                        analysed_lines.append(line)

                    elif 'VERW.-ST.:' in substring:
                        dicto_verw = slices[7]
                        dicto_0_data_verw = dicto_verw['VERW.-ST']  # tuple
                        dicto_1_data_verw = dicto_verw['VERW_Info']  # tuple
                        data_0_verw = substring[dicto_0_data_verw[0]:dicto_0_data_verw[1]].strip()
                        data_1_verw = substring[dicto_1_data_verw[0]:dicto_1_data_verw[1]].strip()
                        next_line_VERW = line
                        if line == amount_of_lines:
                            if data_0_verw == '':
                                data_0_verw = None
                            if data_1_verw == '':
                                data_1_verw = None

                            register.update({'VERW.-ST': data_0_verw})
                            register.update({'VERW_Info': data_1_verw})
                        else:
                            x = 1
                            pass  # TODO: make logic for
                        analysed_lines.append(line)

                    elif line not in analysed_lines:
                        register.update({'extra_info': substring.strip()})

                grouping_input['regs'].append(register)

        date = datetime.date.today()
        date_string = date.strftime('%y%m%d')

        final_path = DataPoint.PATH_DataFiles + '\\' + date_string + '_PDS_AGRMZ_parsed_final_' + source + '.json'
        with open(final_path, 'w', encoding='utf-8') as f:
            json.dump(main_dict, f, indent=4, sort_keys=False, ensure_ascii=False)

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
                                data.replace(' ', '')
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
                                data.replace(' ', '')
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
                            if data == '':  # if the line does not have information, None cant be added
                                data = None
                            if q_2 not in register_dict[code][reg_counter]:
                                register_dict[code][reg_counter].update({q_2: data})
                            else:
                                if data:
                                    register_dict[code][reg_counter][q_2] += data
                            analised_lines.append(line)
        # TODO: change directory to base path
        with open('PDS_ACC_final.json', 'w', encoding='utf-8') as f:
            json.dump(register_dict, f, indent=4, sort_keys=True, ensure_ascii=False)


for source in ['vehicle', 'aggregate']:
    DataProvider.agrmz(source)
