from MainframeMainConnections import MainframeMainConections as Connection
import json
import datetime
from collections import OrderedDict


class PdsNfcAGR:

    def __init__(self):
        m = Connection.LogInMBBrasTN3270PDS()
        self.mainframe = m.mainframe_connection()

    def screen(self):
        kg_list = []
        operation = True
        self.mainframe.send_string('AGR', 1, 30)
        # TODO include automatic referencing into send_string and remove manual input
        self.mainframe.send_string('C963425', 2, 46)
        self.mainframe.move_to(24, 80)
        self.mainframe.send_enter()
        self.mainframe.wait_for_field()
        check_list = []
        while operation is True:
            kg_dict = OrderedDict()
            kg_data = self.ebcdic_screen_operation(7, 4, 4)
            if kg_data not in check_list or check_list is not check_list:
                check_list.append(kg_data)
                kg_dict['bm_original'] = self.ebcdic_screen_operation(5, 4, 18, remove_spaces=True)
                swap_string = self.ebcdic_screen_operation(5, 4, 18, remove_spaces=True)
                for char in [' ', '.', '-']:
                    if char in swap_string:
                        swap_string = swap_string.replace(char, '')
                kg_dict['bm'] = swap_string
                kg_dict['kg'] = kg_data
                kg_dict['kg_name'] = self.ebcdic_screen_operation(7, 9, 51, remove_spaces=True)
                kg_list.append(kg_dict)
                self.mainframe.move_to(24, 80)
                self.mainframe.send_pf20()
                self.mainframe.wait_for_field()
            else:
                operation = False
        return kg_list

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


d = PdsNfcAGR()
data = d.screen()

date = datetime.date.today()
date_string = date.strftime('%y%m%d')

with open(date_string + 'PDS_KGS_AGR.json', 'w') as f:
    json.dump(data, f, indent=4, sort_keys=True, ensure_ascii=False)
