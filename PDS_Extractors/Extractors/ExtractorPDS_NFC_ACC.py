from MainframeMainConnections import MainframeMainConections as Connection
import json
import datetime
from PDS_Extractors.Data import DataProvider


class PdsNfcACC:

    def __init__(self):
        m = Connection.LogInMBBrasTN3270PDS()
        self.mainframe = m.mainframe_connection()
        self.codes_list = DataProvider.DataProvider.all_codes()

    def screen(self):
        final_acc_dict = {}
        final_lines = []
        data_eof_declaration = 'DATEI - ENDE'
        data_deleted_declaration = 'STAEMME ALS GELOESCHT GEKENNZEICHNET'
        data_not_available = 'SNR NICHT VORHANDEN'
        for i, code in enumerate(self.codes_list):
            oper_eof = True
            self.mainframe.send_string('ACC', 1, 30)
            self.mainframe.move_to(2, 46)
            self.mainframe.send_eraseEOF()
            self.mainframe.wait_for_field()
            self.mainframe.send_string(code, 2, 46)
            # self.mainframe.send_string('IXTA4', 2, 46)  ## test
            self.mainframe.move_to(24, 80)
            self.mainframe.send_enter()
            self.mainframe.wait_for_field()
            final_lines = []
            while oper_eof:
                for screen_line in range(11, 23):  # range 8-22..23 is not considered in operation
                    line_data = self.ebcdic_screen_operation(screen_line, 1, 80, remove_spaces=False)
                    if screen_line == 11 and line_data.strip() == '':
                        if data_deleted_declaration in self.ebcdic_screen_operation(24, 1, 80, remove_spaces=False):
                            final_acc_dict[code] = ['Deleted']
                            break
                        elif data_not_available in self.ebcdic_screen_operation(24, 1, 80, remove_spaces=False):
                            final_acc_dict[code] = ['Not Available']
                            break
                        else:
                            final_acc_dict[code] = ['Empty']
                            break
                    elif line_data.strip() != '':
                        final_lines.append(line_data)

                final_acc_dict[code] = final_lines

                if i < len(self.codes_list):
                    if data_eof_declaration in self.ebcdic_screen_operation(24, 1, 80, remove_spaces=False) or\
                            data_deleted_declaration in self.ebcdic_screen_operation(24, 1, 80, remove_spaces=False) or \
                            data_not_available in self.ebcdic_screen_operation(24, 1, 80, remove_spaces=False):
                        oper_eof = False

                    elif self.ebcdic_screen_operation(24, 1, 40, remove_spaces=False).strip() != '':
                        x = 1
                    else:
                        self.mainframe.move_to(24, 80)
                        self.mainframe.send_enter()
                        self.mainframe.wait_for_field()

        date = datetime.date.today()
        date_string = date.strftime('%y%m%d')
        path = 'C:\\Users\\vravagn\\PycharmProjects\\DataExtractor\\PDS_Extractors'

        with open (path + '\\' + date_string + '_PDS_ACC.json', 'w') as f:
            json.dump (final_acc_dict, f, indent=4, sort_keys=True, ensure_ascii=False)

        return print('concluded')

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


d = PdsNfcACC()
d.screen()
