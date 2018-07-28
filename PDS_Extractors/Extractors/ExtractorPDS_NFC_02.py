from MainframeMainConnections import MainframeMainConections as Connection
import json
import datetime
from collections import OrderedDict


class PdsNfc02:
    @staticmethod
    def screen():
        mainframe_data = []
        oper_eof = True
        line_number = 1
        page_number = 1
        data_eof_declaration = 'DATEIENDE'
        m = Connection.LogInMBBrasTN3270PDS()
        mainframe_connection = m.mainframe_connection()
        mainframe_connection.send_string('02', 1, 30)
        mainframe_connection.move_to(24, 80)
        mainframe_connection.send_enter()
        mainframe_connection.wait_for_field()
        while oper_eof:
            for line in range(8, 23):  # range 8-22..23 is not considered in operation
                line_list = OrderedDict()
                line_data = mainframe_connection.string_get(line, 1, 80)
                if not line_data.replace(' ', '') == '':
                    line_list['page'] = page_number
                    line_list['line'] = line_number
                    line_list['text'] = mainframe_connection.string_get(line, 1, 80)
                    mainframe_data.append(line_list)
                    line_number += 1
                if data_eof_declaration in mainframe_connection.string_get(24, 1, 80):
                    oper_eof = False
            page_number += 1
            mainframe_connection.move_to(24, 80)
            mainframe_connection.send_enter()
            mainframe_connection.wait_for_field()
        return mainframe_data


d = PdsNfc02()
data = d.screen()

date = datetime.date.today()
date_string = date.strftime('%y%m%d')

with open('C:\\Users\\vravagn\\PycharmProjects\\dataextractor\\PDS_Extractors\\' + date_string + '_PDS_02.json', 'w') as f:
    json.dump(data, f, indent=4, sort_keys=True, ensure_ascii=False)
