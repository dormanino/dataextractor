from MainframeMainConnections import MainframeMainConections as Connection
import json
import datetime
from collections import OrderedDict


class PdsNfc03:

    def __init__(self):
        m = Connection.LogInMBBrasTN3270PDS()
        self.mainframe = m.mainframe_connection()

    def screen(self):
        mainframe_data = []
        oper_eof = True
        line_number = 1
        page_number = 1
        data_eof_declaration = 'DATEIENDE'
        self.mainframe.send_string('03', 1, 30)
        self.mainframe.move_to(24, 80)
        self.mainframe.send_enter()
        self.mainframe.wait_for_field()
        while oper_eof:
            for line in range(8, 23):  # range 8-22..23 is not considered in operation
                line_list = OrderedDict()
                line_data = self.ebcdic_screen_operation(line, 1, 80, remove_spaces=False)
                if not line_data.replace(' ', '') == '':
                    line_list['page'] = page_number
                    line_list['line'] = line_number
                    line_list['text'] = self.ebcdic_screen_operation(line, 1, 80, remove_spaces=False)
                    mainframe_data.append(line_list)
                    line_number += 1
                if data_eof_declaration in self.ebcdic_screen_operation(24, 1, 80, remove_spaces=False):
                    oper_eof = False
            page_number += 1
            self.mainframe.move_to(24, 80)
            self.mainframe.send_enter()
            self.mainframe.wait_for_field()
        return mainframe_data

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


d = PdsNfc03()
data = d.screen()

date = datetime.date.today()
date_string = date.strftime('%y%m%d')

with open('C:\\Users\\vravagn\\PycharmProjects\\dataextractor\\PDS_Extractors\\' + date_string + '_PDS_03.json', 'w') as f:
    json.dump(data, f, indent=4, sort_keys=True, ensure_ascii=False)
