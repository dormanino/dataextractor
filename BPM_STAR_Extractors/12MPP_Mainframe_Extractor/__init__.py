from MainframeMainConnections import LogInMBBrasTN3270BPMSTAR
from BPM_STAR_Extractors.DataPoint import DataPoint
from GeneralHelpers import PartitionStringinDigitsandNonDigits
import json
import datetime
import time


class ProPresum:
    def __init__(self):
        m = LogInMBBrasTN3270BPMSTAR()
        self.mainframe = m.mainframe_connection()

    def pro_presum_main(self, resume_type='ptfm', main_option='a', periodicity='m', presentation=' '):
        """
            schematics for screen matrix function
                1) rows starts on char 1 and ends on char 80 (80 columns)
                2) amount of rows on screen starts on 1 and ends on 24
                3) screen complete matrix represented as row x column (1,1 / 24, 80) integers
        """

        """
            method pro_presum_main emulates the screen data and fields to choose and therefore receives variables as options
            as follows:
                1sr screen of dialog:
                    main_option:
                        'a' represents the individual choice by type option (20, 28) position
                    periodicity:
                        'm' represents the choice of periodicity to analise as months. 'd' - daily and 'a' - annual also
                        available (21, 17) position
                2nd screen of dialog:
                    resume_type:
                        there are several possibilities but the PTFM has the volumes from Sao Bernardo and Juiz de Fora plants
                3rd screen of dialog:
                    presentation:
                        ' ' - blank -> used to remove the way the data is presented to show the most complete data (also with
                        export figures) (16, 49) position
        """
        #  TODO: implement query options from mainframe application screen i.e. 'Periodicidade'

        self.mainframe.send_string('pro-presum', 24, 32)
        time.sleep(1)  # sleeps because the connection may fail in between processes
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

        """
            get the full header on 6,1,80 (consider row, column, amount of chars) and strip string, split by spaces (chain of methods) and
            part the data from the returned list from split method/function 
        """
        dates_header_list = self.mainframe.string_get(6, 1, 80).strip().split(' ')
        dates_header_list[:] = [item for item in dates_header_list if item != '']
        dates_from_header = []
        for dates in dates_header_list:
            month, year = PartitionStringinDigitsandNonDigits.Partition.partition(dates)
            dates_from_header.append((month, year))
        months_from_header = [month for month, year in [data for data in dates_from_header]]
        years_from_header = set(year for month, year in [data for data in dates_from_header] if year != '')

        TOTALS_DECLARATION = 'TOTAL FINAL'
        oper_eof = True
        start = True
        data_eof_declaration = ''
        data_line_list = []
        totals_line_list = []
        dicto = {}
        main_operation_dict = {'variant_data': []}
        partials_main_operation_dict = {'variant_data': []}
        full_volume_data = {}
        months_volume_dict = {}

        while oper_eof:
            if start:
                # the first item determines the end of the full cycle of data
                data_eof_declaration = self.mainframe.string_get(4, 1, 80)

            for line in range(7, 18, 2):  # range 7-18 in steps of 2 lines copy the variant information's
                if self.mainframe.string_get(line, 1, 80).strip() != '':
                    data_line_list.append((self.mainframe.string_get(line, 1, 80), self.mainframe.string_get(line + 1, 1, 80)))

            if TOTALS_DECLARATION not in self.mainframe.string_get(19, 1, 80):
                counter = 0
                main_data_str = self.mainframe.string_get(4, 1, 80)
                variant = main_data_str[1:29]
                oper_eof_partial = True

                while oper_eof_partial:
                    for line in range(7, 18, 2):  # range 7-18 in steps of 2 lines copy the variant information's
                        if not self.mainframe.string_get(line, 1, 80).strip() == '' and\
                                not self.mainframe.string_get(line + 1, 1, 80).strip() == '':

                            partial_volume = self.mainframe.string_get(line + 1, 1, 80).strip().split(' ')
                            partial_volume[:] = [item for item in partial_volume if item != '']
                            partials_volume_dict = dict(zip(months_from_header, partial_volume))
                            partials_period_totals = {"TOTAL": partials_volume_dict["TOTAL"]}
                            partials_main_data_str = self.mainframe.string_get(line, 1, 80).strip()
                            partials_register_information = partials_main_data_str[1:26].strip().split('-')
                            partials_order_lacation_information = partials_main_data_str[26:80].strip.split('-')

                            if len(years_from_header) == 1:
                                partials_volume_dict.pop("TOTAL")
                                months_volume_dict = partials_volume_dict
                                volume_data = {'register_number': partials_register_information[0],
                                               'register_name': partials_register_information[1],
                                               'order_location_number_cerep': partials_order_lacation_information[0],
                                               'order_location_name': partials_order_lacation_information[1],
                                               'months': months_volume_dict, 'totals': partials_period_totals}
                                full_volume_data = {"year": years_from_header, "data": volume_data}
                            else:
                                partials_volume_dict.pop("TOTAL")
                                swap_volume_dict = partials_volume_dict
                                for year_from_header in years_from_header:
                                    for month, year in dates_from_header:
                                        if month in swap_volume_dict.keys() and year == year_from_header:
                                            months_volume_dict = {'key': month, 'value': partials_volume_dict[month]}
                                    volume_data = {'register_number': partials_register_information[0],
                                                   'register_name': partials_register_information[1],
                                                   'order_location_number_cerep': partials_order_lacation_information[0],
                                                   'order_location_name': partials_order_lacation_information[1],
                                                   'months': months_volume_dict, 'totals': partials_period_totals}
                                    full_volume_data = {"year": year_from_header, "data": volume_data}

                            main_data_str = self.mainframe.string_get(4, 1, 80)
                            variant = main_data_str[1:29]
                            variant_representation = main_data_str[29:58]

                            partials_main_operation_dict['variant_data'].append({'variant': variant.replace(' ', ''),
                                                                                 'variant_representation': variant_representation.strip(),
                                                                                 'volume_data': full_volume_data
                                                                                 })
                            counter += 1

                    if TOTALS_DECLARATION in self.mainframe.string_get(19, 1, 80):
                        oper_eof_partial = False
                        # in order for the flow of data be maintained, the next variant have to be queued. Then reintroduced into (22,9) for
                        # the screen to be reloaded on the analysed variant. This is why the next block of code is maintained
                        # in the flow with the inclusion of a erase statement to the before mentioned position
                        self.mainframe.move_to(22, 9)
                        self.mainframe.send_eraseEOF()

                    self.mainframe.move_to(24, 80)
                    self.mainframe.send_enter()
                    self.mainframe.wait_for_field()

                self.mainframe.send_string(variant, 22, 9)
                self.mainframe.move_to(24, 80)
                self.mainframe.send_enter()
                self.mainframe.wait_for_field()

            # the data has partial data in the screen
            if TOTALS_DECLARATION in self.mainframe.string_get(19, 1, 80):
                # first dict
                totals_line = (self.mainframe.string_get(20, 1, 80))
                totals_line_list.append(totals_line)
                dicto[self.mainframe.string_get(4, 1, 80)] = data_line_list, totals_line_list
                totals_line_list = []
                data_line_list = []

                # second dict (test)
                totals_volume = totals_line.strip().split(' ')
                totals_volume[:] = [item for item in totals_volume if item != '']
                volume_dict = dict(zip(months_from_header, totals_volume))
                period_totals = {"TOTAL": volume_dict["TOTAL"]}
                if len(years_from_header) == 1:
                    volume_dict.pop("TOTAL")
                    months_volume_dict = volume_dict
                    volume_data = {'months': months_volume_dict, 'totals': period_totals}
                    full_volume_data = {"year": years_from_header, "data": volume_data}
                else:
                    volume_dict.pop("TOTAL")
                    swap_volume_dict = volume_dict
                    for year_from_header in years_from_header:
                        for month, year in dates_from_header:
                            if month in swap_volume_dict.keys() and year == year_from_header:
                                months_volume_dict = {'key': month, 'value': volume_dict[month]}
                        volume_data = {'months': months_volume_dict, 'totals': volume_dict["TOTAL"]}
                        full_volume_data = {"year": year_from_header, "data": volume_data}

                main_data_str = self.mainframe.string_get(4, 1, 80)
                variant_representation = main_data_str[29:58]

                main_operation_dict['variant_data'].append({'variant': main_data_str[1:29].replace(' ', ''),
                                                            'variant_representation': variant_representation.strip(),
                                                            'volume_data': full_volume_data
                                                            })

            if data_eof_declaration in self.mainframe.string_get(4, 1, 80) and not start:
                oper_eof = False
                start = False

            self.mainframe.move_to(24, 80)
            self.mainframe.send_enter()
            self.mainframe.wait_for_field()
        return dicto


d = ProPresum().pro_presum_main()

date = datetime.date.today()
date_string = date.strftime('%y%m%d')

with open(DataPoint.PATH_DataFiles + "\\" + date_string + '_12mpp_raw.json', 'w') as f:
    json.dump(d, f, indent=4, sort_keys=True, ensure_ascii=False)
