from MainframeMainConnections import MainframeMainConections as Connection
import json
import datetime
import LatestFileVersion
from collections import OrderedDict


class PdsNfcAGRMZ:

    def __init__(self):
        m = Connection.LogInMBBrasTN3270PDS()
        self.mainframe = m.mainframe_connection()

    def screen(self):
        line = 0
        page = 0
        data_eof_declaration = 'DATEI - ENDE'
        kgs_file = LatestFileVersion.latest_file_version('json', 'PDS_KGS_AGR')
        data_json = json.load(open(kgs_file))
        kg_list = []
        agrmz_data = []
        for reg in data_json:
            kg_list.append([reg['bm'], reg['kg']])
        for kg in kg_list:
            operation = True
            self.mainframe.send_string('AGRMZ', 1, 30)
            self.mainframe.send_string(kg[0], 2, 46)
            self.mainframe.move_to(2, 60)
            self.mainframe.send_eraseEOF()
            self.mainframe.move_to(2, 65)
            self.mainframe.send_eraseEOF()
            if kg[1][0] == 'C':
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
                    if not line_data.replace(' ', '') == '':
                        agr_dict = OrderedDict()
                        line += 1

                        if kg[1][0] == 'C':
                            agr_dict['data_type'] = 'Code'
                        elif kg[1][0] == 'G':
                            agr_dict['data_type'] = 'Aggregate'
                        else:
                            agr_dict['data_type'] = 'SAA'

                        agr_dict['page'] = page
                        agr_dict['line'] = line
                        agr_dict['bm'] = kg[0]
                        agr_dict['kg'] = kg[1]
                        agr_dict['data'] = line_data
                        agrmz_data.append(agr_dict)
                    if data_eof_declaration in self.mainframe.string_get(24, 1, 80):
                        operation = False
                page += 1
                self.mainframe.move_to(24, 80)
                self.mainframe.send_enter()
                self.mainframe.wait_for_field()
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


d = PdsNfcAGRMZ()
data = d.screen()

date = datetime.date.today()
date_string = date.strftime('%y%m%d')
print(data)

with open(date_string + 'PDS_KGS_AGRMZ.json', 'w') as f:
    json.dump(data, f, indent=4, sort_keys=True, ensure_ascii=False).encode('utf-8')
