from MainframeMainConnections import MainframeMainConections as Connection
from os import getcwd
import time


class EdsNfcAST:

    @staticmethod
    def screen():

        start_time = time.time ()
        with open(getcwd() + '\\data.csv', 'r') as file:
            data_partnumbers = [line.rstrip() for line in file.readlines()]

        outF = open ("myOutFile.txt", "a")

        m = Connection.LogInMBBrasTN3270EDS()

        mainframe_connection = m.mainframe_connection()
        main_list = []
        for partnumber in data_partnumbers:
            print(partnumber)
            mainframe_connection.send_string('AST', 1, 31)
            mainframe_connection.move_to (2, 7)
            mainframe_connection.send_eraseEOF ()
            mainframe_connection.send_string(partnumber, 2, 7)
            mainframe_connection.move_to (2, 50)
            mainframe_connection.send_eraseEOF()
            mainframe_connection.move_to(24, 80)
            mainframe_connection.send_enter()
            mainframe_connection.wait_for_field()
            if mainframe_connection.string_get(5, 17, 40).strip() == '':  # ifd item does not present contents
                outF.write(partnumber + ',' + 'inexistente' + "\n")
                continue

            first_as = mainframe_connection.string_get(6, 18, 3)  # as
            plants_str = mainframe_connection.string_get(8, 17, 40) + ' ' + mainframe_connection.string_get(9, 17, 40)

            # fase análise
            # if the latest as is the first and Brasil is in it, construct the data and move to next
            if first_as == '001':
                if EdsNfcAST.checkbrplant(plants_str):
                    date = mainframe_connection.string_get(6, 46, 8)
                    # main_list.append([partnumber, date])
                    outF.write(partnumber + ',' + date + "\n")
            else:
                eof = True
                as_swap = '001'
                date = mainframe_connection.string_get (6, 46, 8)
                while eof:
                    mainframe_connection.move_to (2, 50)
                    mainframe_connection.send_eraseEOF ()
                    mainframe_connection.send_string(as_swap, 2, 50)
                    mainframe_connection.move_to(24, 80)
                    mainframe_connection.send_enter()
                    mainframe_connection.wait_for_field()
                    current_as = mainframe_connection.string_get (6, 18, 3)
                    plants_str = mainframe_connection.string_get (8, 17, 40) + ' ' + mainframe_connection.string_get (9, 17, 40)
                    if EdsNfcAST.checkbrplant (plants_str):
                        first_date_in_br = mainframe_connection.string_get(6, 46, 8)
                        # main_list.append ([partnumber, date, first_date_in_br])
                        outF.write (partnumber + ',' + date + ',' + first_date_in_br + "\n")
                        eof = False
                    else:
                        if int(current_as) < int(first_as):
                            as_swap = EdsNfcAST.asstringadder (current_as)
                        else:
                            # main_list.append ([partnumber, 'not released in br'])
                            outF.write (partnumber + ',' + 'not released in br' + "\n")
                            eof = False
            print ("--- %s seconds ---" % (time.time () - start_time))
        outF.close ()
        return main_list

    @staticmethod
    def asstringadder(as_string=''):
        if not as_string.strip() == '':
            string_int_swp = int(as_string) + 1
            if string_int_swp < 10:
                return '00' + str(string_int_swp)
            elif string_int_swp == 10 or string_int_swp <= 99:
                return '0' + str(string_int_swp)
            elif string_int_swp >= 100:
                return str(string_int_swp)
        else:
            return ''

    @staticmethod
    def checkbrplant(u_string=''):
        if not u_string == '':
            u_string = u_string.split()
            if 'U' in u_string:
                return True
            else:
                return False
        else:
            return False


d = EdsNfcAST()
data = d.screen()
