import json
import datetime
from PDS_Extractors.Data.DataPoint import DataPoint
from PDS_Extractors.Helpers.LatestFileVersion import LatestFileVersion


class DataProvider:

    @staticmethod
    def agrmz(plant, data_type_source, source):
        bm_info = json.load(open(DataPoint.data_info_bm))
        complete_line = ''
        data_source = []
        curent_reg = ''
        bm = ''
        bu = ''
        family = ''
        data_type = ''
        kg = ''
        none_flag = False
        lines_list = source

        for line_counter, line_info_dict in enumerate(lines_list):
            line = line_info_dict['data']
            if line is not None:
                register_char = line[1]
                if register_char is '_' and line_counter is not 0:  # start of component
                    if line != curent_reg and not none_flag:
                        data_source.append((bm, bu, family, data_type, kg, complete_line))
                        complete_line = ''
                    else:
                        bm = line_info_dict['bm']
                        data_type = line_info_dict['data_type']
                        kg = line_info_dict['kg'].strip()
                        none_flag = False
                        complete_line = ''
                        if bm in bm_info:
                            bu = bm_info[bm][0]
                            family = bm_info[bm][1]
                        else:
                            bu = None
                            family = None

                    curent_reg = line
                complete_line += line
                bm = line_info_dict['bm']
                data_type = line_info_dict['data_type']
                kg = line_info_dict['kg'].strip()
                if bm in bm_info:
                    bu = bm_info[bm][0]
                    family = bm_info[bm][1]
                else:
                    bu = None
                    family = None
            else:
                data_source.append((bm, bu, family, data_type, kg, complete_line))
                bm = line_info_dict['bm']
                data_source.append((bm, None, None, None, None, None))
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
                'part_description': (3, 54),
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
                'bg': (24, 26),  # bg para Code
                'code': (28, 62)
            },
            5: {
                'bg': (24, 26),  # bg para SAA
                'code': (25, 80)
            },
            6: {
                'zusteuerbed': (25, 80)
            },
            7: {
                'verw.-st': (13, 16),
                'verw_info': (16, 80)
            }
        }

        main_dict = dict(plant=plant, source=data_type_source, data=[])
        for data in data_source:
            # print(data)

            # Find/Create Baumuster node

            bm_data = next(filter(lambda i: i["bm"] == data[0], main_dict["data"]), None)
            if bm_data is None:
                bm_data = dict(bm="", bu="", family="", data=[])
                bm_data["bm"] = data[0]
                bm_data["bu"] = data[1]
                bm_data["family"] = data[2]
                main_dict["data"].append(bm_data)

            # if the data_type field is None
            info_data_input = data[3]
            if info_data_input is not None:

                # Find/Create Data Input node
                data_input = next(filter(lambda i: i["type"] == info_data_input, bm_data["data"]), None)
                if data_input is None:
                    data_input = dict(type="", data=[])
                    data_input["type"] = info_data_input
                    bm_data["data"].append(data_input)

                # Find/Create Grouping Input node
                info_grouping_input = data[4]
                grouping_input = next(filter(lambda i: i["kg"] == info_grouping_input, data_input["data"]), None)
                if grouping_input is None:
                    grouping_input = dict(kg="", regs=[])
                    grouping_input["kg"] = info_grouping_input
                    data_input["data"].append(grouping_input)

                full_line = data[5]
                amount_of_lines = int(len(full_line) / 80)  # finds the amount of data in the component (each line has 80 char)
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

                    if '_' in substring[1]:  # if the line is the component marker
                        # print(substring)

                        for q, r in zip(slices[1].keys(), slices[1].values()):
                            data = substring[r[0]:r[1]].strip().replace(",", ";")
                            if data == '':
                                data = None
                            register.update({q: data})
                        analysed_lines.append(line)

                    elif not prior_substring.strip() == '' and '_' in prior_substring[1]:  # defines if you are in between the component header and
                        for q_1, r_1 in zip(slices[2].keys(), slices[2].values()):
                            data = substring[r_1[0]:r_1[1]].strip().replace(",", ";")
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
                            data = substring[r[0]:r[1]].strip().replace(",", ";")
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

                        if substring[dicto_data_0_codebedingungen[0]: dicto_data_0_codebedingungen[1]].strip().replace(",", ";") == '':
                            bg_codebedingungen = None
                        else:
                            bg_codebedingungen = substring[dicto_data_0_codebedingungen[0]: dicto_data_0_codebedingungen[1]]

                        restriction_codebedingungen = substring[dicto_data_1_codebedingungen[0]: dicto_data_1_codebedingungen[1]].strip().replace(",", ";")

                        if ';' not in restriction_codebedingungen:
                            eof_codebedingungen = False
                            next_line_codebedingungen += 1
                        else:
                            eof_codebedingungen = True

                        while not eof_codebedingungen:
                            next_end_char_codebedingungen = next_line_codebedingungen * 80
                            next_start_char_codebedingungen = next_end_char_codebedingungen - 80
                            next_substring_codebedingungen = full_line[next_start_char_codebedingungen:next_end_char_codebedingungen + 1]
                            next_substring_anal_codebedingungen = next_substring_codebedingungen[dicto_data_1_codebedingungen[0]: dicto_data_1_codebedingungen[1]].strip().replace(",", ";")
                            restriction_codebedingungen = restriction_codebedingungen + next_substring_anal_codebedingungen
                            analysed_lines.append(next_line_codebedingungen)
                            if ';' not in next_substring_anal_codebedingungen:
                                eof_codebedingungen = False
                                next_line_codebedingungen += 1
                            else:
                                eof_codebedingungen = True

                        restriction_codebedingungen = restriction_codebedingungen.replace(' ', '')

                        register.update({'bg_codebedingungen': bg_codebedingungen})
                        register.update({'codebedingungen': restriction_codebedingungen})
                        analysed_lines.append(line)

                    elif 'BG/BAUBARKEITSBED' in substring:

                        dicto_baubarkeitsbed = slices[5]
                        dicto_data_0_baubarkeitsbed = dicto_baubarkeitsbed['bg']  # tuple
                        dicto_data_1_baubarkeitsbed = dicto_baubarkeitsbed['code']  # tuple
                        data_baubarkeitsbed = substring[dicto_data_1_baubarkeitsbed[0]:dicto_data_1_baubarkeitsbed[1]]  # codes data
                        next_line_baubarkeitsbed = line

                        if substring[dicto_data_0_baubarkeitsbed[0]: dicto_data_0_baubarkeitsbed[1]].strip().replace(",", ";") == '':
                            bg_baubarkeitsbed = None
                        else:
                            bg_baubarkeitsbed = substring[dicto_data_0_baubarkeitsbed[0]: dicto_data_0_baubarkeitsbed[1]]

                        restriction_baubarkeitsbed = substring[dicto_data_1_baubarkeitsbed[0]: dicto_data_1_baubarkeitsbed[1]].strip().replace(",", ";")

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
                        register.update({'baubarkeitsbed': restriction_baubarkeitsbed})
                        analysed_lines.append(line)

                    elif 'PB/ZUSTEUERBED' in substring:
                        dicto_zusteuerbed = slices[6]
                        dicto_data_zusteuerbed = dicto_zusteuerbed['zusteuerbed']  # tuple
                        data_zusteuerbed = substring[dicto_data_zusteuerbed[0]:dicto_data_zusteuerbed[1]]  # codes data
                        next_line_zusteuerbed = line

                        restriction_zusteuerbed = substring[dicto_data_zusteuerbed[0]: dicto_data_zusteuerbed[1]].strip().replace(",", ";")

                        if ';' not in restriction_zusteuerbed:
                            eof_zusteuerbed = False
                            next_line_zusteuerbed += 1
                        else:
                            eof_zusteuerbed = True

                        while not eof_zusteuerbed:

                            next_end_char_zusteuerbed = next_line_zusteuerbed * 80
                            next_start_char_zusteuerbed = next_end_char_zusteuerbed - 80
                            next_substring_zusteuerbed = full_line[next_start_char_zusteuerbed:next_end_char_zusteuerbed + 1]
                            next_substring_anal_zusteuerbed = next_substring_zusteuerbed[dicto_data_zusteuerbed[0]: dicto_data_zusteuerbed[1]].strip().replace(",", ";")
                            restriction_zusteuerbed = restriction_zusteuerbed + next_substring_anal_zusteuerbed
                            analysed_lines.append(next_line_zusteuerbed)

                            if ';' not in next_substring_anal_zusteuerbed:
                                eof_zusteuerbed = False
                                next_line_zusteuerbed += 1
                            else:
                                eof_zusteuerbed = True

                        restriction_zusteuerbed = restriction_zusteuerbed.replace(' ', '')
                        register.update({'zusteuerbed': restriction_zusteuerbed})
                        analysed_lines.append(line)

                    elif 'VERW.-ST.:' in substring:
                        dicto_verw = slices[7]
                        dicto_0_data_verw = dicto_verw['verw.-st']  # tuple
                        dicto_1_data_verw = dicto_verw['verw_info']  # tuple
                        data_0_verw = substring[dicto_0_data_verw[0]:dicto_0_data_verw[1]].strip().replace(",", ";")
                        data_1_verw = substring[dicto_1_data_verw[0]:dicto_1_data_verw[1]].strip().replace(",", ";")
                        next_line_VERW = line
                        if line == amount_of_lines:
                            if data_0_verw == '':
                                data_0_verw = None
                            if data_1_verw == '':
                                data_1_verw = None

                            register.update({'verw.-st': data_0_verw})
                            register.update({'verw_info': data_1_verw})
                        else:
                            x = 1
                            pass  # TODO: make logic for
                        analysed_lines.append(line)

                    elif line not in analysed_lines:
                        register.update({'extra_info': substring.strip().replace(",", ";")})

                grouping_input['regs'].append(register)

        date = datetime.date.today()
        date_string = date.strftime('%y%m%d')

        final_path = DataPoint.PATH_DataFiles + '\\' + date_string + '_' + plant + '_' + data_type_source + '_PDS_AGRMZ_parsed_final' + '.json'
        with open(final_path, 'w', encoding='utf-8') as f:
            json.dump(main_dict, f, indent=4, sort_keys=True, ensure_ascii=False)

        return print('concluded')

    @staticmethod
    def all_codes():
        #TODO: remove weak file path
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
                amount_of_lines = int(len(full_line) / 80)  # finds the amount of data in the component (each line has 80 char)
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

                    elif not prior_substring.strip() == '' and '_' in prior_substring[1]:  # defines if you are in between the component header and

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

    @staticmethod
    def treeca(plant, source):

        slices = {
            1: {
                'part_number': (3, 21),
                'es1': (21, 25),
                'es2': (26, 30),
                'pos': (32, 35),
                'str': (36, 39),
                'aa': (40, 42),
                'l': (43, 45),
                'r': (46, 47),
                'li': (47, 49),
                'hws': (51, 55),
                'bza': (55, 61),
                'aesa': (64, 68),
                'quantity': (69, 78),
                'da': (78, 80)
            },
            2: {
                'part_description': (4, 39),
                'b': (39, 40),
                'w': (41, 42),
                'em-ab': (45, 51),
                'em-bis': (56, 62),
                't_a': (66, 72),
                't_b': (74, 80)
            },
            3: {
                'aesb': (4, 8),
                'kem-ab': (9, 23),
                'kem-bis': (24, 38),
                'ehm': (39, 42),
                'ag': (43, 45),
                'pf': (46, 48),
                'vh': (49, 51),
                'abs': (52, 56),
                'rfme': (57, 64),
                'fz-a': (65, 72),
                'fz-b': (73, 80)
            },
            4: {
                'ma': (38, 55)
            }
        }

        lines_list = json.load(open(source))
        # lines_list = dict_lines_list_file['data']
        main_dict = dict(plant=plant, data=[])
        register = {}
        # print(type(lines_list))

        for line_dict in lines_list:
            for key, line_dict_content in line_dict.items():
                # constructs the dictionaries
                saa_data = next(filter(lambda x: x['source'] == key, main_dict['data']), None)
                if saa_data is None:
                    saa_data = dict(source='', regs=[])
                    saa_data['source'] = key
                    main_dict['data'].append(saa_data)

                if line_dict_content is not None:
                    amount_of_chars_in_the_string = int(len(line_dict_content))
                    amount_of_lines = int(amount_of_chars_in_the_string / 80)

                    full_line = line_dict_content
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

                        if line == 1 and '_' in substring[1]:  # if the line is the component marker
                            for q, r in zip(slices[1].keys(), slices[1].values()):
                                data = substring[r[0]:r[1]].strip()
                                if data == '':
                                    data = None
                                register.update({q: data})
                        elif line == 2:
                            for q, r in zip(slices[2].keys(), slices[2].values()):
                                data = substring[r[0]:r[1]].strip()
                                if data == '':
                                    data = None
                                register.update({q: data})
                        elif line == 3:
                            for q, r in zip(slices[3].keys(), slices[3].values()):
                                data = substring[r[0]:r[1]].strip()
                                if data == '':
                                    data = None
                                register.update({q: data})
                        elif line == 4:
                            for q, r in zip(slices[4].keys(), slices[4].values()):
                                data = substring[r[0]:r[1]].strip()
                                if data == '':
                                    data = None
                                register.update({q: data})
                        else:
                            register.update({'extra_info': substring})

                    saa_data['regs'].append(register)
                    register = {}
                else:
                    saa_data['regs'].append(None)
                    register = {}

        date = datetime.date.today()
        date_string = date.strftime('%y%m%d')

        final_path = DataPoint.PATH_DataFiles + '\\' + date_string + '_' + plant + '_3ca_parsed_final' + '.json'
        with open(final_path, 'w', encoding='utf-8') as f:
            json.dump(main_dict, f, indent=4, sort_keys=False, ensure_ascii=False)

        return print('concluded')


# agrmz code
plants = ['sbc', 'jdf']
data_types = ['vehicle', 'aggregate']
for plant in plants:
    list_to_check = []
    for data_type in data_types:
        if plant == 'sbc' and data_type == 'vehicle':
            list_to_check = json.load(open(DataPoint.data_agrmz_raw_vehicles_sbc))
        elif plant == 'jdf' and data_type == 'vehicle':
            list_to_check = json.load(open(DataPoint.data_agrmz_raw_vehicles_jdf))
        elif plant == 'sbc' and data_type == 'aggregate':
            list_to_check = json.load(open(DataPoint.data_agrmz_raw_aggregates_sbc))
        elif plant == 'jdf' and data_type == 'aggregate':
            list_to_check = json.load(open(DataPoint.data_agrmz_raw_aggregates_jdf))
        DataProvider.agrmz(plant, data_type, list_to_check)
        print("concluded " + plant + "/" + data_type)


# DataProvider.treeca('sbc', DataPoint.data_3ca_raw_sbc)
# DataProvider.treeca('jdf', DataPoint.data_3ca_raw_jdf)
