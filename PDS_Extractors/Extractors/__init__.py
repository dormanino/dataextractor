from PDS_Extractors.Data.DataPoint import DataPoint
from PDS_Extractors.Models.Part.ComponentsCollection import ComponentsCollection
from BPM_STAR_Extractors import MainframeMainConnections
import json
import datetime
import time
from collections import OrderedDict


class PdsNfc:
    connection = MainframeMainConnections.LogInMBBrasTN3270PDS()

    def __init__(self, plant=None):
        self.plant = plant
        if self.plant == 'sbc':
            self.app_name = 'IDMSCV6P'
            self.app_plant = '154'
        elif self.plant == 'jdf':
            self.app_name = 'IDMSCV8P'
            self.app_plant = '1542'
        self.mainframe_connection = self.connection.pds_connection(self.app_name, self.app_plant)

    def oper_pds_56(self, logout=False):
        parts_data_3ca = object
        if self.plant == "sbc":
            parts_data_3ca = ComponentsCollection.from_dict(json.load(open(DataPoint.data_3ca_sbc, encoding='utf-8')))
        elif self.plant == "jdf":
            parts_data_3ca = ComponentsCollection.from_dict(json.load(open(DataPoint.data_3ca_jdf, encoding='utf-8')))

        parts_set = set()
        drawings_and_tables_set = set()
        data_list = [parts_set, drawings_and_tables_set]
        register_count = 0
        ifchangeinternalflag = False
        pd_56_data_list = []
        for component in parts_data_3ca.component_parts_list:
            for part in component.parts_list:
                parts_set.add(part.part_number.replace(" ", ""))

        for index, data in enumerate(data_list):
            for part in data:
                self.mainframe_connection.send_string('56', 1, 30)
                self.mainframe_connection.move_to(24, 80)
                self.mainframe_connection.send_enter()
                self.mainframe_connection.wait_for_field()

                self.mainframe_connection.move_to(2, 46)
                self.mainframe_connection.send_eraseEOF()
                self.mainframe_connection.send_string(part, 2, 46)

                self.mainframe_connection.move_to(24, 80)
                self.mainframe_connection.send_enter()
                self.mainframe_connection.wait_for_field()

                ifchangeflag = True
                while ifchangeflag:
                    pd56_data = OrderedDict()
                    pd56_data["sachnummer"] = self.mainframe_connection.string_get_EBCDIC(5, 1, 80).strip().replace(",", ";")
                    pd56_data["benennung"] = self.mainframe_connection.string_get_EBCDIC(7, 1, 51).strip().replace(",", ";")
                    pd56_data["skz"] = self.mainframe_connection.string_get_EBCDIC(7, 53, 4).strip().replace(",", ";")
                    pd56_data["st"] = self.mainframe_connection.string_get_EBCDIC(7, 58, 2).strip().replace(",", ";")
                    pd56_data["ww"] = self.mainframe_connection.string_get_EBCDIC(7, 61, 2).strip().replace(",", ";")
                    pd56_data["d"] = self.mainframe_connection.string_get_EBCDIC(7, 64, 1).strip().replace(",", ";")
                    pd56_data["f"] = self.mainframe_connection.string_get_EBCDIC(7, 66, 1).strip().replace(",", ";")
                    pd56_data["b"] = self.mainframe_connection.string_get_EBCDIC(7, 68, 1).strip().replace(",", ";")
                    pd56_data["ehm"] = self.mainframe_connection.string_get_EBCDIC(7, 70, 2).strip().replace(",", ";")
                    pd56_data["ae-st"] = self.mainframe_connection.string_get_EBCDIC(7, 74, 3).strip().replace(",", ";")
                    pd56_data["brm"] = self.mainframe_connection.string_get_EBCDIC(8, 7, 45).strip().replace(",", ";")
                    pd56_data["dbwa"] = self.mainframe_connection.string_get_EBCDIC(8, 62, 6).strip().replace(",", ";")
                    pd56_data["get"] = self.mainframe_connection.string_get_EBCDIC(8, 73, 1).strip().replace(",", ";")
                    pd56_data["mr"] = self.mainframe_connection.string_get_EBCDIC(8, 79, 2).strip().replace(",", ";")
                    pd56_data["kf"] = self.mainframe_connection.string_get_EBCDIC(9, 6, 1).strip().replace(",", ";")
                    pd56_data["vert"] = self.mainframe_connection.string_get_EBCDIC(9, 14, 45).strip().replace(",", ";")
                    pd56_data["w-vert"] = self.mainframe_connection.string_get_EBCDIC(9, 68, 13).strip().replace(",", ";")
                    pd56_data["bm"] = self.mainframe_connection.string_get_EBCDIC(10, 7, 51).strip().replace(",", ";")
                    pd56_data["kont"] = self.mainframe_connection.string_get_EBCDIC(10, 74, 4).strip().replace(",", ";")
                    pd56_data["znr"] = self.mainframe_connection.string_get_EBCDIC(11, 7, 3).strip().replace(",", ";")
                    pd56_data["zgs"] = self.mainframe_connection.string_get_EBCDIC(11, 16, 3).strip().replace(",", ";")
                    pd56_data["b1"] = self.mainframe_connection.string_get_EBCDIC(11, 24, 57).strip().replace(",", ";")
                    pd56_data["cad"] = self.mainframe_connection.string_get_EBCDIC(12, 16, 2).strip().replace(",", ";")
                    pd56_data["b2"] = self.mainframe_connection.string_get_EBCDIC(12, 24, 57).strip().replace(",", ";")
                    if "PF13=B1,B2/NEUE ATTRIBUTE" in self.mainframe_connection.string_get_EBCDIC(24, 1, 80):
                        pass  # TODO: include routine to new further data into b1 and b2 field
                    # if zdat field is not a date, is considered another pd56 for part number/drawings table
                    # dont repeat if isnt the first set
                    if index == 0:
                        if self.mainframe_connection.string_get_EBCDIC(13, 2, 1) == "_":
                            pd56_data["zdat_ref_table"] = self.mainframe_connection.string_get_EBCDIC(13, 10, 13).strip().replace(",", ";")
                            if self.mainframe_connection.string_get_EBCDIC(13, 10, 13).strip().replace(",", ";") not in parts_set:
                                drawings_and_tables_set.add(self.mainframe_connection.string_get_EBCDIC(13, 10, 13).strip().replace(",", ";"))
                            # check if the reference is inside the data to copy. Include in the list if it´s not
                        else:
                            pd56_data["zdat"] = self.mainframe_connection.string_get_EBCDIC(13, 10, 13).strip().replace(",", ";")
                    pd56_data["mt"] = self.mainframe_connection.string_get_EBCDIC(13, 29, 1).strip().replace(",", ";")
                    pd56_data["dbn"] = self.mainframe_connection.string_get_EBCDIC(13, 36, 5).strip().replace(",", ";")
                    pd56_data["dbo"] = self.mainframe_connection.string_get_EBCDIC(13, 47, 5).strip().replace(",", ";")
                    pd56_data["dba"] = self.mainframe_connection.string_get_EBCDIC(13, 60, 5).strip().replace(",", ";")
                    pd56_data["ds"] = self.mainframe_connection.string_get_EBCDIC(13, 72, 1).strip().replace(",", ";")
                    pd56_data["dz"] = self.mainframe_connection.string_get_EBCDIC(13, 78, 1).strip().replace(",", ";")
                    pd56_data["wqua"] = self.mainframe_connection.string_get_EBCDIC(14, 8, 38).strip().replace(",", ";")
                    pd56_data["dbwe"] = self.mainframe_connection.string_get_EBCDIC(14, 60, 6).strip().replace(",", ";")
                    pd56_data["dbh"] = self.mainframe_connection.string_get_EBCDIC(14, 72, 6).strip().replace(",", ";")
                    pd56_data["bza"] = self.mainframe_connection.string_get_EBCDIC(15, 8, 7).strip().replace(",", ";")
                    pd56_data["da"] = self.mainframe_connection.string_get_EBCDIC(15, 21, 2).strip().replace(",", ";")
                    pd56_data["di"] = self.mainframe_connection.string_get_EBCDIC(15, 33, 3).strip().replace(",", ";")
                    pd56_data["mv-vw"] = self.mainframe_connection.string_get_EBCDIC(15, 47, 3).strip().replace(",", ";")
                    pd56_data["pv"] = self.mainframe_connection.string_get_EBCDIC(15, 60, 3).strip().replace(",", ";")
                    pd56_data["dv"] = self.mainframe_connection.string_get_EBCDIC(15, 72, 3).strip().replace(",", ";")
                    pd56_data["lm"] = self.mainframe_connection.string_get_EBCDIC(16, 80, 1).strip().replace(",", ";")
                    pd56_data["abs"] = self.mainframe_connection.string_get_EBCDIC(16, 8, 4).strip().replace(",", ";")
                    pd56_data["eba"] = self.mainframe_connection.string_get_EBCDIC(16, 21, 5).strip().replace(",", ";")
                    pd56_data["lba"] = self.mainframe_connection.string_get_EBCDIC(16, 33, 5).strip().replace(",", ";")
                    pd56_data["moa/bg"] = self.mainframe_connection.string_get_EBCDIC(16, 47, 7).strip().replace(",", ";")
                    pd56_data["ml/ae"] = self.mainframe_connection.string_get_EBCDIC(16, 72, 8).strip().replace(",", ";")
                    if "PF15=F23/GEWICHTE" in self.mainframe_connection.string_get_EBCDIC(24, 1, 80):
                        pass  # TODO: implement routine to copy multi_screen data
                    pd56_data["em-ab"] = self.mainframe_connection.string_get_EBCDIC(18, 10, 6).strip().replace(",", ";")
                    pd56_data["t-a"] = self.mainframe_connection.string_get_EBCDIC(18, 24, 7).strip().replace(",", ";")
                    pd56_data["fz-ab"] = self.mainframe_connection.string_get_EBCDIC(18, 32, 7).strip().replace(",", ";")
                    pd56_data["em-bis"] = self.mainframe_connection.string_get_EBCDIC(18, 50, 6).strip().replace(",", ";")
                    if self.mainframe_connection.string_get_EBCDIC(18, 50, 6).strip().replace(",", ";") == "":
                        ifchangeflag = False
                    else:
                        ifchangeflag = True
                    pd56_data["t-b"] = self.mainframe_connection.string_get_EBCDIC(18, 64, 7).strip().replace(",", ";")
                    pd56_data["fz-bis"] = self.mainframe_connection.string_get_EBCDIC(18, 72, 7).strip().replace(",", ";")
                    if (
                            self.mainframe_connection.string_get_EBCDIC(21, 1, 80).strip() != "" and
                            self.mainframe_connection.string_get_EBCDIC(22, 1, 80).strip() != "" and
                            self.mainframe_connection.string_get_EBCDIC(23, 1, 80).strip() != ""
                    ):
                        pd56_data_raw_mat_data = OrderedDict()
                        pd56_data_raw_mat_data["pos"] = self.mainframe_connection.string_get_EBCDIC(21, 2, 3).strip().replace(",", ";")
                        pd56_data_raw_mat_data["sachnummer"] = self.mainframe_connection.string_get_EBCDIC(21, 10, 18).strip().replace(",", ";")
                        pd56_data_raw_mat_data["es1"] = self.mainframe_connection.string_get_EBCDIC(21, 29, 4).strip().replace(",", ";")
                        pd56_data_raw_mat_data["es2"] = self.mainframe_connection.string_get_EBCDIC(21, 34, 4).strip().replace(",", ";")
                        pd56_data_raw_mat_data["ehm"] = self.mainframe_connection.string_get_EBCDIC(21, 39, 2).strip().replace(",", ";")
                        # menge is a decimal number...had to change ; by .
                        pd56_data_raw_mat_data["menge"] = self.mainframe_connection.string_get_EBCDIC(21, 43, 9).strip().replace(",", ".")
                        pd56_data_raw_mat_data["da"] = self.mainframe_connection.string_get_EBCDIC(21, 53, 2).strip().replace(",", ";")
                        pd56_data_raw_mat_data["pos"] = self.mainframe_connection.string_get_EBCDIC(21, 61, 6).strip().replace(",", ";")
                        pd56_data_raw_mat_data["em-ab"] = self.mainframe_connection.string_get_EBCDIC(21, 73, 6).strip().replace(",", ";")
                        pd56_data_raw_mat_data["em-bis"] = self.mainframe_connection.string_get_EBCDIC(21, 73, 6).strip().replace(",", ";")
                        # menge is a decimal number...had to change ; by .
                        pd56_data_raw_mat_data["erm"] = self.mainframe_connection.string_get_EBCDIC(22, 10, 17).strip().replace(",", ".")
                        pd56_data_raw_mat_data["srm"] = self.mainframe_connection.string_get_EBCDIC(22, 29, 7).strip().replace(",", ";")
                        pd56_data_raw_mat_data["bza"] = self.mainframe_connection.string_get_EBCDIC(22, 39, 7).strip().replace(",", ";")
                        pd56_data_raw_mat_data["t-a"] = self.mainframe_connection.string_get_EBCDIC(22, 60, 7).strip().replace(",", ";")
                        pd56_data_raw_mat_data["t-b"] = self.mainframe_connection.string_get_EBCDIC(22, 72, 7).strip().replace(",", ";")
                        pd56_data_raw_mat_data["zsm"] = self.mainframe_connection.string_get_EBCDIC(23, 10, 17).strip().replace(",", ";")
                        pd56_data_raw_mat_data["szs"] = self.mainframe_connection.string_get_EBCDIC(23, 29, 6).strip().replace(",", ";")
                        pd56_data_raw_mat_data["abf"] = self.mainframe_connection.string_get_EBCDIC(23, 39, 7).strip().replace(",", ";")
                        pd56_data_raw_mat_data["fz-ab"] = self.mainframe_connection.string_get_EBCDIC(23, 60, 7).strip().replace(",", ";")
                        pd56_data_raw_mat_data["fz-bis"] = self.mainframe_connection.string_get_EBCDIC(23, 72, 7).strip().replace(",", ";")
                        pd56_data["raw_part_data"] = pd56_data_raw_mat_data
                    else:
                        pd56_data["raw_part_data"] = None

                    # if external check points change, add register counter
                    if ifchangeflag:
                        pd56_data["tech_change_counter"] = register_count
                        register_count += 1
                        ifchangeinternalflag = True
                        self.mainframe_connection.move_to(24, 80)
                        self.mainframe_connection.send_enter()
                        self.mainframe_connection.wait_for_field()
                    else:
                        if ifchangeinternalflag:
                            pd56_data["tech_change_counter"] = register_count
                            register_count = 0
                            ifchangeinternalflag = False
                        else:
                            pd56_data["register_count"] = None

                    pd_56_data_list.append(pd56_data)

        if logout:
            self.connection.pds_logout()

        return pd_56_data_list

    def oper_pds_02(self, logout=False):
        mainframe_data_list = []
        oper_eof = True
        line_number = 1
        page_number = 1
        data_eof_declaration = 'DATEIENDE'
        self.mainframe_connection.send_string('02', 1, 30)
        self.mainframe_connection.move_to(24, 80)
        self.mainframe_connection.send_enter()
        self.mainframe_connection.wait_for_field()
        while oper_eof:
            for line in range(8, 23):  # range 8-22..23 is not considered in operation
                line_list = OrderedDict()
                line_data = self.mainframe_connection.string_get_EBCDIC(line, 1, 80)
                if not line_data.replace(' ', '') == '':
                    line_list['page'] = page_number
                    line_list['line'] = line_number
                    line_list['text'] = self.mainframe_connection.string_get_EBCDIC(line, 1, 80)
                    mainframe_data_list.append(line_list)
                    line_number += 1
                if data_eof_declaration in self.mainframe_connection.string_get_EBCDIC(24, 1, 80):
                    oper_eof = False
            page_number += 1
            self.mainframe_connection.move_to(24, 80)
            self.mainframe_connection.send_enter()
            self.mainframe_connection.wait_for_field()
        if logout:
            self.connection.pds_logout()
        return mainframe_data_list

    def oper_pds_03(self, logout=False):
        mainframe_data = []
        oper_eof = True
        line_number = 1
        page_number = 1
        data_eof_declaration = 'DATEIENDE'
        self.mainframe_connection.send_string('03', 1, 30)
        self.mainframe_connection.move_to(24, 80)
        self.mainframe_connection.send_enter()
        self.mainframe_connection.wait_for_field()
        while oper_eof:
            for line in range(8, 23):  # range 8-22..23 is not considered in operation
                line_list = OrderedDict()
                line_data = self.mainframe_connection.string_get_EBCDIC(line, 1, 80)
                if not line_data.replace(' ', '') == '':
                    line_list['page'] = page_number
                    line_list['line'] = line_number
                    line_list['text'] = self.mainframe_connection.string_get_EBCDIC(line, 1, 80)
                    mainframe_data.append(line_list)
                    line_number += 1
                if data_eof_declaration in self.mainframe_connection.string_get_EBCDIC(24, 1, 80):
                    oper_eof = False
            page_number += 1
            self.mainframe_connection.move_to(24, 80)
            self.mainframe_connection.send_enter()
            self.mainframe_connection.wait_for_field()
        if logout:
            self.connection.pds_logout()
        return mainframe_data

    def oper_pds_agr_for_kgs(self, data_type, logout=False):
        pds_bm_data = object
        if plant is 'sbc':
            if data_type == 'vehicle':
                pds_bm_data = json.load(open(DataPoint.data_02_sbc, 'r'))
            elif data_type == 'aggregate':
                pds_bm_data = json.load(open(DataPoint.data_03_sbc, 'r'))
        elif plant is 'jdf':
            if data_type == 'vehicle':
                pds_bm_data = json.load(open(DataPoint.data_02_jdf, 'r'))
            elif data_type == 'aggregate':
                pds_bm_data = json.load(open(DataPoint.data_03_jdf, 'r'))

        bm_set = set()

        for item in pds_bm_data:
            bm_string = item['text'][4:13]
            for char in [' ', '.', '-', ',']:
                bm_string = bm_string.replace(char, '')
            bm_set.add(bm_string)

        bm_srt_list = list(bm_set)
        bm_srt_list.sort()
        del bm_set

        kg_list = []
        for bm in bm_srt_list:
            operation = True
            self.mainframe_connection.send_string('AGR', 1, 30)
            self.mainframe_connection.send_string(bm, 2, 46)
            self.mainframe_connection.move_to(2, 60)
            self.mainframe_connection.send_eraseEOF()
            self.mainframe_connection.move_to(2, 65)
            self.mainframe_connection.send_eraseEOF()
            self.mainframe_connection.move_to(24, 80)
            self.mainframe_connection.send_enter()
            self.mainframe_connection.wait_for_field()
            check_list = []
            while operation is True:
                kg_dict = OrderedDict()
                kg_data = self.mainframe_connection.string_get_EBCDIC(7, 4, 4)
                if kg_data not in check_list or check_list is not check_list:
                    check_list.append(kg_data)
                    kg_dict['bm_original'] = self.mainframe_connection.string_get_EBCDIC(5, 4, 18)
                    swap_string = self.mainframe_connection.string_get_EBCDIC(5, 4, 18)
                    for char in [' ', '.', '-', ',']:
                        if char in swap_string:
                            swap_string = swap_string.replace(char, '')
                    kg_dict['bm'] = swap_string
                    kg_dict['kg'] = kg_data
                    kg_dict['kg_name'] = self.mainframe_connection.string_get_EBCDIC(7, 9, 51)
                    kg_list.append(kg_dict)
                    self.mainframe_connection.move_to(24, 80)
                    self.mainframe_connection.send_pf20()
                    self.mainframe_connection.wait_for_field()
                else:
                    operation = False
        if logout:
            self.connection.pds_logout()
        return kg_list

    def oper_pds_agrmz(self, data_type, logout=False):
        pds_bm_data = object
        if plant is 'sbc':
            if data_type == 'vehicle':
                pds_bm_data = json.load(open(DataPoint.data_kgs_agr_vehicles_sbc))
            elif data_type == 'aggregate':
                pds_bm_data = json.load(open(DataPoint.data_kgs_agr_aggregates_sbc))
        elif plant is 'jdf':
            if data_type == 'vehicle':
                pds_bm_data = json.load(open(DataPoint.data_kgs_agr_vehicles_jdf))
            elif data_type == 'aggregate':
                pds_bm_data = json.load(open(DataPoint.data_kgs_agr_aggregates_jdf))
        kg_list = []
        for reg in pds_bm_data:
            kg_list.append([reg['bm'], reg['kg']])
        kg_list = sorted(kg_list, key=lambda x: (x[0], x[1]))

        timeout = time.time() + 60 * 2
        line = 0
        page = 0
        data_eof_declaration = 'DATEI - ENDE'
        data_eof_declaration_chng = 'DATEI-ENDE'
        data_deletion_declaration = 'STAEMME ALS GELOESCHT GEKENNZEICHNET'

        agrmz_data = []

        for kg in kg_list:
            if not kg[1]:  # falsy if empty if string
                agr_dict = OrderedDict()
                line += 1
                agr_dict['data_type'] = None
                agr_dict['page'] = page
                agr_dict['line'] = line
                agr_dict['bm'] = kg[0]
                agr_dict['data'] = None
                agr_dict['kg'] = None
                agrmz_data.append(agr_dict)
                page += 1
                continue
            else:
                operation = True
                if time.time() > timeout:
                    time.sleep(10)
                    timeout = time.time() + 60 * 2
                self.mainframe_connection.send_string('AGRMZ', 1, 30)
                self.mainframe_connection.send_string(kg[0], 2, 46)
                self.mainframe_connection.move_to(2, 60)
                self.mainframe_connection.send_eraseEOF()
                self.mainframe_connection.move_to(2, 65)
                self.mainframe_connection.send_eraseEOF()
                if kg[1][0] == 'C':  # TODO weak referencing-if the kg is a code (start with caa normally)
                    start_line = 11
                else:
                    start_line = 12
                self.mainframe_connection.send_string(kg[1], 2, 60)
                self.mainframe_connection.move_to(24, 80)
                self.mainframe_connection.send_enter()
                self.mainframe_connection.wait_for_field()
                while operation is True:
                    for screenline in range(start_line, 23):
                        line_data = self.mainframe_connection.string_get_EBCDIC(screenline, 1, 80)
                        if not self.mainframe_connection.string_get_EBCDIC(screenline, 1, 80).strip() == '':
                            agr_dict = OrderedDict()
                            line += 1
                            if kg[1][0] == 'C':
                                agr_dict['data_type'] = 'Code'
                            elif kg[1][0] == 'G':
                                agr_dict['data_type'] = 'Aggregate'
                            elif kg[1][0] == 'S':
                                agr_dict['data_type'] = 'SAA'
                            elif kg[1][0] == 'L':
                                agr_dict['data_type'] = 'LEG'
                            else:
                                agr_dict['data_type'] = 'General'
                            agr_dict['page'] = page
                            agr_dict['line'] = line
                            agr_dict['bm'] = str(kg[0])
                            agr_dict['kg'] = str(kg[1])
                            agr_dict['data'] = str(line_data)
                            agrmz_data.append(agr_dict)
                    if data_eof_declaration in self.mainframe_connection.string_get_EBCDIC(24, 1, 80):
                        operation = False
                    elif data_eof_declaration_chng in self.mainframe_connection.string_get_EBCDIC(24, 1, 80):
                        operation = False
                    elif data_deletion_declaration in self.mainframe_connection.string_get_EBCDIC(24, 1, 80):
                        operation = False
                    else:
                        self.mainframe_connection.move_to(24, 80)
                        self.mainframe_connection.send_enter()
                        self.mainframe_connection.wait_for_field()

                    page += 1
        if logout:
            self.connection.pds_logout()
        return agrmz_data

    def oper_pds_3ca(self, logout=False):
        saa_list = []
        file_csv = object
        if plant is 'sbc':
            file_csv = open(DataPoint.data_saa_sbc, encoding='utf-8')
        elif plant is 'jdf':
            file_csv = open(DataPoint.data_saa_jdf, encoding='utf-8')

        saa_swap_list = file_csv.readlines()
        for saa_line_index, saa_line in enumerate(saa_swap_list):
            if not saa_line_index == 0:
                saa_rpl_line = saa_line.replace('\n', '')
                saa_split = saa_rpl_line.split(',')
                saa_list.append(saa_split)

        part_list = []
        operation = True
        timeout = time.time() + 60 * 2
        data_eof_declaration = 'DATEI - ENDE'
        data_eof_declaration_chng = 'DATEI-ENDE'
        data_deletion_declaration = 'STAEMME ALS GELOESCHT GEKENNZEICHNET'
        data_not_availabe_declaration = 'SNR NICHT VORHANDEN'
        string_trail = ''
        ntsaa = {}
        register_chk = False
        for saa in saa_list:
            if saa:  # falsy if empty if string
                operation = True
                saa_start = saa[1][0:7]  # saa[0] with spaces and all chars
                saa_trailing = saa[1][7:9]
                self.mainframe_connection.send_string('3CA', 1, 30)
                self.mainframe_connection.send_string(saa_start, 2, 46)
                self.mainframe_connection.send_enter()
                self.mainframe_connection.wait_for_field()
                self.mainframe_connection.move_to(2, 60)
                self.mainframe_connection.send_eraseEOF()
                self.mainframe_connection.move_to(2, 65)
                self.mainframe_connection.send_eraseEOF()
                self.mainframe_connection.move_to(4, 25)
                self.mainframe_connection.send_eraseEOF()
                self.mainframe_connection.send_string(saa_trailing, 4, 25)
                self.mainframe_connection.move_to(4, 32)
                self.mainframe_connection.send_eraseEOF()
                self.mainframe_connection.send_string(saa_trailing, 4, 32)
                self.mainframe_connection.move_to(24, 80)
                self.mainframe_connection.send_enter()
                self.mainframe_connection.wait_for_field()
                while operation:
                    if time.time() > timeout:
                        time.sleep(10)
                        timeout = time.time() + 60 * 2
                    for line in range(9, 24):  # range 8-22..23 is not considered in operation
                        line_data = self.mainframe_connection.string_get_EBCDIC(line, 1, 80)
                        if not line_data.replace(' ', '') == '':
                            register_chk = True
                            if line_data[1] == '_':
                                string_start = line_data
                                if string_trail:
                                    string_complete = string_start + string_trail
                                    ntsaa[saa[0]] = string_complete
                                    part_list.append(ntsaa)
                                    string_trail = ''
                                    ntsaa = {}
                            else:
                                string_trail += line_data
                        elif line == 9:
                            if not register_chk:
                                ntsaa[saa[0]] = None
                                part_list.append(ntsaa)
                                string_trail = ''
                                ntsaa = {}
                                continue

                    if data_eof_declaration in self.mainframe_connection.string_get_EBCDIC(24, 1, 80):
                        operation = False
                        register_chk = False
                    elif data_eof_declaration_chng in self.mainframe_connection.string_get_EBCDIC(24, 1, 80):
                        operation = False
                        register_chk = False
                    elif data_deletion_declaration in self.mainframe_connection.string_get_EBCDIC(24, 1, 80):
                        operation = False
                        register_chk = False
                    elif data_not_availabe_declaration in self.mainframe_connection.string_get_EBCDIC(24, 1, 80):
                        operation = False
                        register_chk = False
                    else:
                        self.mainframe_connection.move_to(24, 80)
                        self.mainframe_connection.send_enter()
                        self.mainframe_connection.wait_for_field()
        if logout:
            self.connection.pds_logout()
        return part_list


plants = ['sbc', 'jdf']  # 'jdf',
data_type = ['vehicle', 'aggregate']
date = datetime.date.today()
date_string = date.strftime('%y%m%d')

for plant in plants:
    pds_mainframe_connection = PdsNfc(plant)
    data_02 = pds_mainframe_connection.oper_pds_02()

    with open(DataPoint.PATH_DataFiles + '\\' + date_string + '_' + plant + '_PDS_02.json', 'w+') as f:
        json.dump(data_02, f, indent=4, sort_keys=True, ensure_ascii=False)

    data_03 = pds_mainframe_connection.oper_pds_03()

    with open(DataPoint.PATH_DataFiles + '\\' + date_string + '_' + plant + '_PDS_03.json', 'w+') as f:
        json.dump(data_03, f, indent=4, sort_keys=True, ensure_ascii=False)
    pds_mainframe_connection.connection.pds_logout()

for plant in plants:
    pds_mainframe_connection = PdsNfc(plant)
    for data in data_type:
        data_kgs = pds_mainframe_connection.oper_pds_agr_for_kgs(data)

        with open(DataPoint.PATH_DataFiles + '\\' + date_string + '_' + plant + '_' + data + '_PDS_kgs.json', 'w+') as f:
            json.dump(data_kgs, f, indent=4, sort_keys=True, ensure_ascii=False)
    pds_mainframe_connection.connection.pds_logout()

for plant in plants:
    pds_mainframe_connection = PdsNfc(plant)
    for data in data_type:
        data_agr = pds_mainframe_connection.oper_pds_agrmz(data)

        with open(DataPoint.PATH_DataFiles + '\\' + date_string + '_' + plant + '_' + data + '_PDS_agrmz.json', 'w+') as f:
            json.dump(data_agr, f, indent=4, sort_keys=False, ensure_ascii=False)
    pds_mainframe_connection.connection.pds_logout()
PdsNfc().mainframe_connection.send_string('exit', 2, 15)

for plant in plants:
    pds_mainframe_connection = PdsNfc(plant)
    data_parts = pds_mainframe_connection.oper_pds_3ca()
    with open(DataPoint.PATH_DataFiles + '\\' + date_string + '_' + plant + '_PDS_3CA.json', 'w+') as f:
        json.dump(data_parts, f, indent=4, sort_keys=False, ensure_ascii=False)
    pds_mainframe_connection.connection.pds_logout()
PdsNfc().mainframe_connection.send_string('exit', 2, 15)
sys.exit()

# pd56
# for plant in plants:
#     pds_mainframe_connection = PdsNfc(plant)
#     data_56 = pds_mainframe_connection.oper_pds_56()
#     with open(DataPoint.PATH_DataFiles + '\\' + date_string + '_' + plant + '_PDS_56.json', 'w+') as f:
#         json.dump(data_56, f, indent=4, sort_keys=False, ensure_ascii=False)
