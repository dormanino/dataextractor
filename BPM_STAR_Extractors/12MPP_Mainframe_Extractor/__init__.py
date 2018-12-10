from BPM_STAR_Extractors.DataPoint import DataPoint
from GeneralHelpers import PartitionStringinDigitsandNonDigits
import json
import datetime
import time
from MainframeExtractor.Connection.LogInMBBrasTN3270 import LogInMBBrasTN3270


class LogInMBBrasTN3270BPMSTAR(LogInMBBrasTN3270):
    # TODO: implement expired password logic
    def mainframe_connection(self):
        self.emulator.send_string('3', 2, 15)  # 3 is BMP-Star's Mainframe access number
        self.emulator.move_to(24, 80)
        self.emulator.send_enter()
        self.emulator.wait_for_field()
        time.sleep(3)

        if self.emulator.string_get(1, 1, 80).replace(' ', '') == '':  # check if the header is empty to ensure connection
            self.emulator.terminate()

        while self.emulator.string_get(23, 2, 12) == 'PF4 = DBSTAR':
            if self.emulator.string_get(12, 57, 6) != 'DBSTAR' or not self.emulator.string_get(2, 2, 10) != 'REATIVACAO':
                while self.emulator.string_get(24, 19, 57) == 'NO ACTIVE CONVERSATION IN PROCESS, CANNOT PROCESS COMMAND':
                    time.sleep(3)
                    self.emulator.send_pf4()
                    self.emulator.wait_for_field()
                while self.emulator.string_get(24, 19, 46) == 'DESTINATION CAN NOT BE FOUND OR CREATED, DEST=':
                    time.sleep(3)
                    self.emulator.send_pf4()
                    self.emulator.wait_for_field()
                while self.emulator.string_get(24, 20, 22) == 'EXIT COMMAND COMPLETED':
                    time.sleep(3)
                    self.emulator.send_pf4()
                    self.emulator.wait_for_field()

        if self.emulator.string_get(12, 57, 6) == 'DBSTAR':  # if DBSTAR available and ready
            pass
        elif self.emulator.string_get(2, 2, 10) == 'REATIVACAO':
            while not self.emulator.string_get(12, 57, 6) == 'DBSTAR':
                self.emulator.send_string('c', 20, 19)  # clear all active commands
                self.emulator.move_to(24, 80)
                self.emulator.send_enter()
                self.emulator.wait_for_field()
                # TODO: delete
                # self.emulator.send_string('s', 24, 32)
                # while self.emulator.string_get(7, 3, 1) == '_':
                #     self.emulator.send_string('c', 7, 3)
                #     self.emulator.move_to(24, 80)
                #     self.emulator.send_enter()
                #     self.emulator.wait_for_field()
                #     if self.emulator.string_get(7, 60, 20) == 'CS NAO PODE SER CAN.':
                #         self.emulator.send_string('s', 7, 3)
                #         self.emulator.send_enter()
                #         self.emulator.wait_for_field()
                #         self.emulator.send_PA1()
                #         self.emulator.wait_for_field()

            #     self.emulator.send_string('menu', 24, 32)  # if DBSTAR available but not ready on home screen
            #     self.emulator.move_to(24, 80)
            #     self.emulator.send_enter()
            #     self.emulator.wait_for_field()
            # else:
            # self.emulator.send_string('menu', 24, 32)  # if DBSTAR available but not ready on home screen
            # self.emulator.move_to(24, 80)
            # self.emulator.send_enter()
            # self.emulator.wait_for_field()
            print('DBSTAR on you fuck')
        return self.emulator


class ProPresum:
    def __init__(self):
        m = LogInMBBrasTN3270BPMSTAR()
        self.mainframe = m.mainframe_connection()

    @staticmethod
    def create_volume_dict(months, year):
        volume_data = dict(year=year,
                           months=months)
        return volume_data

    @staticmethod
    def create_variant_data(order_location_number_cerep, order_location_name, register_number, register_name,
                            total_volume, data):
        variant_data = dict(order_location_number_cerep=order_location_number_cerep,
                            order_location_name=order_location_name,
                            register_number=register_number,
                            register_name=register_name,
                            total_volume=total_volume,
                            data=data)
        return variant_data

    def pro_presum_main(self, dt_ref, resume_type='ptfm', main_option='a', periodicity='m', deno="veiculo", presentation=' ', copy_all=False):
        """
            schematics for screen matrix function
                1) rows starts on char 1 and ends on char 80 (80 columns)
                2) amount of rows on screen starts on 1 and ends on 24
                3) screen complete matrix represented as row x column (1,1 / 24, 80) integers

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
        # if copy_all is flaged, need to include a 'q' to indicate start of the register in the mainframe in the same format from
        # the model below
        self.mainframe.send_string(dt_ref, 4, 49)

        if copy_all is True:
            self.mainframe.move_to(12, 49)
            self.mainframe.send_eraseEOF()
            self.mainframe.send_string('q', 9, 49)
        else:
            self.mainframe.send_string(deno, 12, 49)

        self.mainframe.send_string(presentation, 16, 49)
        self.mainframe.move_to(24, 80)
        self.mainframe.send_enter()
        self.mainframe.wait_for_field()
        time.sleep(1)

        """
            get the full header on line 6, row 1 to 80 (consider row, column, amount of chars) and strip string, split by spaces 
            (chain of methods) and part the data from the returned list from split method/function 
        """

        dates_header_list = self.mainframe.string_get(6, 1, 80).strip().split(' ')
        dates_header_list[:] = [item for item in dates_header_list if item != '']
        dates_from_header = []
        for dates in dates_header_list:
            month, year = PartitionStringinDigitsandNonDigits.Partition.partition(dates)
            dates_from_header.append((month, year))
        months_from_header = [month for month, year in [data for data in dates_from_header]]
        years_from_header = list(set(year for month, year in [data for data in dates_from_header] if year != ''))

        main_operation_dict = dict(extraction_date=datetime.date.today().strftime('%y%m%d'),
                                   ref_date=dt_ref,
                                   resume_type=resume_type,
                                   header=months_from_header,
                                   main_option=main_option,
                                   periodicity=periodicity,
                                   variant_data=[]
                                   )

        partials_main_operation_dict = dict(extraction_date=datetime.date.today().strftime('%y%m%d'),
                                            ref_date=dt_ref,
                                            resume_type=resume_type,
                                            header=months_from_header,
                                            main_option=main_option,
                                            periodicity=periodicity,
                                            variant_data=[]
                                            )

        totals_declaration = 'TOTAL FINAL'
        oper_eof = True
        start = True
        data_eof_declaration = ''
        data_line_list = []
        totals_line_list = []
        dicto = {}

        volume_data = []
        variant_data = []
        variant_complete_data = []
        months_volume_dict = {}

        while oper_eof:
            if start:
                # the first item determines the end of the full cycle of data
                data_eof_declaration = self.mainframe.string_get(4, 1, 80)

            for line in range(7, 18, 2):  # range 7-18 in steps of 2 lines copy the variant information's
                if self.mainframe.string_get(line, 1, 80).strip() != '':
                    data_line_list.append((self.mainframe.string_get(line, 1, 80), self.mainframe.string_get(line + 1, 1, 80)))

            # range 7-18 in steps/blocks of 2 lines copy the variant information's
            for line in range(7, 18, 2):
                if not self.mainframe.string_get(line, 1, 80).strip() == '' and\
                        not self.mainframe.string_get(line + 1, 1, 80).strip() == '':

                    # strip the line of information to strip variant info and values given by sales department
                    # returns swap variable
                    partials_main_data_str = self.mainframe.string_get(line, 1, 80).strip()

                    # slice string and split
                    # returns register information
                    register_information = partials_main_data_str[0:25].strip().split('-')

                    # slice string and split
                    # returns main orders internal sales/country/'for stock' information
                    sales_destination = partials_main_data_str[25:80].strip().split('-')

                    # get information from screen and strip trailing spaces and split by spaces
                    # returns a list of volume by month with int as str inside
                    partial_volume = self.mainframe.string_get(line + 1, 1, 80).strip().split(' ')

                    # with list of volume data by month, remove spaces / empty data from list for consistency
                    # returns 'consistent' list with volume by month
                    partial_volume[:] = [item for item in partial_volume if item != '']

                    # unpacking the months informed in the header (fixed and constant information) including
                    # 'column' with totals for the chosen period
                    # returns dictionary with months in the header with appropriate volume for that month
                    partials_volume_dict = dict(zip(months_from_header, partial_volume))

                    # collect the totals information in a separate dictionary
                    partials_period_totals = partials_volume_dict["TOTAL"]

                    # remove information of totals from the volume dictionary
                    partials_volume_dict.pop("TOTAL")

                    # if the amount of years in the header are one according to the reference date choose

                    for year_from_header in years_from_header:

                        for month, year in dates_from_header:
                            if month in partials_volume_dict.keys() and year == year_from_header:
                                # month_numeric = list(map(lambda x: MonthsHelper.MonthsHelper.numeric[x], month))
                                months_volume_dict[month] = partials_volume_dict[month]
                                #  months_volume_dict[month_numeric] = partials_volume_dict[month]

                        volume_data.append(ProPresum.create_volume_dict(year=year_from_header, months=months_volume_dict))

                        months_volume_dict = {}

                    variant_data.append(ProPresum.create_variant_data(sales_destination[0],
                                                                      sales_destination[1],
                                                                      register_information[0],
                                                                      register_information[1],
                                                                      partials_period_totals,
                                                                      volume_data))
                    volume_data = []

            if totals_declaration in self.mainframe.string_get(19, 1, 80):
                main_data_str = self.mainframe.string_get(4, 1, 80)
                variant = main_data_str[1:29].replace(' ', '')
                sales_name_for_variant = main_data_str[29:58].strip()

                partials_main_operation_dict['variant_data'].append(dict(variant=variant,
                                                                         variant_representation=sales_name_for_variant,
                                                                         volume_data=variant_data))
                variant_data = []

            # the data has partial data in the screen
            if totals_declaration in self.mainframe.string_get(19, 1, 80):
                # first dict
                totals_line = (self.mainframe.string_get(20, 1, 80))
                totals_line_list.append(totals_line)
                dicto[self.mainframe.string_get(4, 1, 80)] = data_line_list, totals_line_list
                totals_line_list = []
                data_line_list = []

                # # second dict (test)
                # totals_volume = totals_line.strip().split(' ')
                # totals_volume[:] = [item for item in totals_volume if item != '']
                # volume_dict = dict(zip(months_from_header, totals_volume))
                # period_totals = volume_dict["TOTAL"]
                # if len(years_from_header) == 1:
                #     volume_dict.pop("TOTAL")
                #     months_volume_dict = volume_dict
                #     volume_data = [{'months': months_volume_dict, 'totals': period_totals}]
                #     variant_data.append({"year": str(years_from_header[0]), "data": volume_data})
                # else:
                #     volume_dict.pop("TOTAL")
                #     swap_volume_dict = volume_dict
                #     variant_data = []
                #     for year_from_header in years_from_header:
                #         for month, year in dates_from_header:
                #             if month in swap_volume_dict.keys() and year == year_from_header:
                #                 months_volume_dict = {'key': month, 'value': volume_dict[month]}
                #         volume_data = [{'months': months_volume_dict, 'totals': period_totals}]
                #
                #         variant_data.append({"year": year_from_header, "data": volume_data})
                #
                # main_data_str = self.mainframe.string_get(4, 1, 80)
                # variant_representation = main_data_str[29:58]
                #
                # main_operation_dict['variant_data'].append({'variant': main_data_str[1:29].replace(' ', ''),
                #                                             'variant_representation': variant_representation.strip(),
                #                                             'volume_data': variant_data
                #                                             })

            if data_eof_declaration in self.mainframe.string_get(4, 1, 80) and start:
                start = False

            self.mainframe.move_to(24, 80)
            self.mainframe.send_enter()
            self.mainframe.wait_for_field()

            if data_eof_declaration in self.mainframe.string_get(4, 1, 80) and not start:
                oper_eof = False

        return dicto, partials_main_operation_dict  #  , main_operation_dict


data_for_12mpp_volume_data_extraction = '0119'
# data_for_12mpp_volume_data_extraction = '0119'
d = ProPresum().pro_presum_main(data_for_12mpp_volume_data_extraction, copy_all=True)

date = datetime.date.today()
date_string = date.strftime('%y%m%d')

with open(DataPoint.PATH_DataFiles + "\\" + date_string + "_" + data_for_12mpp_volume_data_extraction + "_12mpp_raw.json", "w") as f:
    json.dump(d[0], f, indent=4, sort_keys=True, ensure_ascii=False)

# with open(DataPoint.PATH_DataFiles + "\\" + date_string + '_main_operation_dict.json', 'w') as f:
#     json.dump(d[1], f, indent=4, sort_keys=True, ensure_ascii=False)

with open(DataPoint.PATH_DataFiles + "\\" + date_string + '_partials_operation.json', 'w') as f:
    json.dump(d[1], f, indent=4, sort_keys=True, ensure_ascii=False)
