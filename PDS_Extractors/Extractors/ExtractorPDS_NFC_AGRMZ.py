from MainframeMainConnections import MainframeMainConections as Connection
import json
import datetime
from collections import OrderedDict
from PDS_Extractors.Data.DataPoint import DataPoint
import time


class PdsNfcAGRMZ:

    def __init__(self, data):
        m = Connection.LogInMBBrasTN3270PDS()
        self.mainframe = m.mainframe_connection()
        self.data_json = json.load(open(data))

    def screen(self):
        timeout = time.time() + 60 * 2
        line = 0
        page = 0
        data_eof_declaration = 'DATEI - ENDE'
        data_eof_declaration_chng = 'DATEI-ENDE'
        data_deletion_declaration = 'STAEMME ALS GELOESCHT GEKENNZEICHNET'
        kg_list = []
        agrmz_data = []
        for reg in self.data_json:
            kg_list.append([reg['bm'], reg['kg']])
        kg_list = sorted(kg_list, key=lambda x: (x[0], x[1]))

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
                self.mainframe.send_string('AGRMZ', 1, 30)
                self.mainframe.send_string(kg[0], 2, 46)
                self.mainframe.move_to(2, 60)
                self.mainframe.send_eraseEOF()
                self.mainframe.move_to(2, 65)
                self.mainframe.send_eraseEOF()
                if kg[1][0] == 'C':  # TODO weak referencing-if the kg is a code (start with caa normally
                    start_line = 11
                else:
                    start_line = 12
                self.mainframe.send_string(kg[1], 2, 60)
                self.mainframe.move_to(24, 80)
                self.mainframe.send_enter()
                self.mainframe.wait_for_field()
                while operation is True:
                    for screenline in range(start_line, 23):
                        line_data = self.ebcdic_screen_operation(screenline, 1, 80, remove_spaces=False)
                        if not self.ebcdic_screen_operation(screenline, 1, 80, remove_spaces=False).strip() == '':
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
                    if data_eof_declaration in self.mainframe.string_get(24, 1, 80):
                        operation = False
                    elif data_eof_declaration_chng in self.mainframe.string_get(24, 1, 80):
                        operation = False
                    elif data_deletion_declaration in self.mainframe.string_get(24, 1, 80):
                        operation = False
                    else:
                        self.mainframe.move_to(24, 80)
                        self.mainframe.send_enter()
                        self.mainframe.wait_for_field()

                    page += 1
        return agrmz_data

    def ebcdic_screen_operation(self, y_pos, x_pos, length, remove_spaces=True):
        x_pos -= 1
        y_pos -= 1
        mainframe = self.mainframe
        switch_data = mainframe.exec_command_EBCDIC('Ebcdic({0},{1},{2})'.format(y_pos, x_pos, length).encode())
        switch_data = switch_data.data[0]
        switch_data = switch_data.replace(' '.encode(), ''.encode()).decode()
        switch_data = bytearray.fromhex(switch_data).decode(encoding='cp037')
        switch_data = switch_data.encode()
        switch_data = switch_data.replace(b'\x00', b' ').decode()
        if remove_spaces:
            switch_data = switch_data.replace(' ', '').encode()
            switch_data = switch_data.replace(b'\x00', b'').decode()
        return switch_data


date = datetime.date.today()
date_string = date.strftime('%y%m%d')
# start_time = time.time()
# vehicle_pds_bm_agrmz = PdsNfcAGRMZ(DataPoint.data_kgs_agr_vehicles)
# data_vehicle = vehicle_pds_bm_agrmz.screen()
#
# with open('C:\\Users\\vravagn\\PycharmProjects\\dataextractor\\PDS_Extractors\\' + date_string + '_PDS_BM´s_AGRMZ_vehicles.json', 'w') as f:
#     json.dump(data_vehicle, f, indent=4, sort_keys=True, ensure_ascii=False)
#
# print("--- %s seconds ---" % (time.time() - start_time))

start_time = time.time()
# TODO join logics
aggregates_pds_bm_agrmz = PdsNfcAGRMZ(DataPoint.data_kgs_agr_aggregates)
data_aggregates = aggregates_pds_bm_agrmz.screen()

with open('C:\\Users\\vravagn\\PycharmProjects\\dataextractor\\PDS_Extractors\\' + date_string + '_PDS_BM´s_AGRMZ_aggregates.json', 'w') as f:
    json.dump(data_aggregates, f, indent=4, sort_keys=True, ensure_ascii=False)

print("--- %s seconds ---" % (time.time() - start_time))
