from MainframeMainConnections import MainframeMainConections as Connection
import json
import datetime
import time


class ProPresum:
    def __init__(self):
        m = Connection.LogInMBBrasTN3270BPMSTAR()
        self.mainframe = m.mainframe_connection()

    def pro_presum_main(self, resume_type='ptfm', main_option='a', periodicity='m', presentation=' '):
        #  TODO: implement query options from mainframe application screen i.e. 'Periodicidade'
        self.mainframe.send_string('pro-presum', 24, 32)
        time.sleep(1)
        self.mainframe.move_to(24, 80)
        self.mainframe.send_enter()
        self.mainframe.wait_for_field()
        time.sleep(1)
        self.mainframe.send_string(main_option, 20, 28)
        self.mainframe.send_string(periodicity, 21, 17)
        self.mainframe.move_to(24, 80)
        self.mainframe.send_enter()
        self.mainframe.wait_for_field()
        time.sleep(1)
        self.mainframe.send_string(resume_type, 22, 37)
        self.mainframe.move_to(24, 80)
        self.mainframe.send_enter()
        self.mainframe.wait_for_field()
        time.sleep(1)
        self.mainframe.send_string(presentation, 16, 49)
        self.mainframe.move_to(24, 80)
        self.mainframe.send_enter()
        self.mainframe.wait_for_field()
        time.sleep(1)

        #  TODO: implement query options from mainframe application screen i.e. 'Periodicidade' and other options

        oper_eof = True
        page_number = 1
        data_eof_declaration = ''
        start = True
        # TODO: implement query options from mainframe application screen i.e. 'Periodicidade'
        data_line_list = []
        totals_line_list = []
        dicto = {}
        line_data = ''
        while oper_eof:
            if start:  # the first item determines the end of the full cycle of data
                data_eof_declaration = self.mainframe.string_get(4, 1, 80)
            for line in range(7, 18, 2):  # range 7-18 in steps of 2 lines copy the variant informations
                line_data = self.mainframe.string_get(line, 1, 80)
                if line_data.strip() != '':
                    # TODO: implement header main copy (months, etc)
                    data_line = (self.mainframe.string_get(line, 1, 80), self.mainframe.string_get(line + 1, 1, 80))
                    data_line_list.append(data_line)
                    # line_list = OrderedDict()
                    # line_list['page'] = page_number
                    # line_list['data'] = self.mainframe.string_get(4, 1, 80)
                    # line_list['head'] = self.mainframe.string_get(line, 1, 80)
                    # line_list['body'] = self.mainframe.string_get(line + 1, 1, 80)

            if self.mainframe.string_get(19, 2, 11) == 'TOTAL FINAL':
                # TODO: implement header main copy (months, etc)
                totals_line = (self.mainframe.string_get(20, 1, 80))
                totals_line_list.append(totals_line)
                # totals_line_list = OrderedDict()
                # totals_line_list['data'] = self.mainframe.string_get(4, 1, 80)
                # totals_line_list['body'] = self.mainframe.string_get(20, 1, 80)
                dicto[self.mainframe.string_get(4, 1, 80)] = data_line_list, totals_line_list
                totals_line_list = []
                data_line_list = []

            if data_eof_declaration in self.mainframe.string_get(4, 1, 80) and not start:
                oper_eof = False
            else:
                start = False
            page_number += 1
            self.mainframe.move_to(24, 80)
            self.mainframe.send_enter()
            self.mainframe.wait_for_field()
        return dicto


d = ProPresum().pro_presum_main()

date = datetime.date.today()
date_string = date.strftime('%y%m%d')

path = 'C:\\Users\\vravagn\\PycharmProjects\\dataextractor\\BPM_STAR_Extractors\\DataPoint\\'

with open(path + date_string + '12mpp_raw.json', 'w') as f:
    json.dump(d, f, indent=4, sort_keys=True, ensure_ascii=False)
