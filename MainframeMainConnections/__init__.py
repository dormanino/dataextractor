import py3270
import time


class MBBrasMainframeTN3270Connection:

    def __init__(self):
        self.emulator = py3270.Emulator(visible=True)
        self.emulator.connect('cpua')
        self.emulator.wait_for_field()
        if self.emulator.is_connected():
            while not self.emulator.string_found(11, 50, 'Usuario :'):
                self.emulator.wait_for_field()

            if self.emulator.string_found(11, 50, 'Usuario :'):
                self.emulator.wait_for_field()
                print('Session loaded fine')
                pass
            else:
                print('Session not created! Log Off')
                self.emulator.terminate()
        else:
            self.emulator.terminate()


class LogInMBBrasTN3270(MBBrasMainframeTN3270Connection):

    def __init__(self):
        MBBrasMainframeTN3270Connection.__init__(self)
        user = input('Please insert your F mainframe user ID: ')
        password = input('Please, input your user ' + user + ' password: ')
        if self.emulator.is_connected():
            self.emulator.move_to(11, 60)
            self.emulator.send_eraseEOF()
            self.emulator.send_string(user, 11, 60)
            self.emulator.move_to(12, 60)
            self.emulator.send_eraseEOF()
            self.emulator.send_string(password, 12, 60)
            self.emulator.send_enter()
            self.emulator.wait_for_field()
        if self.emulator.string_get(2, 2, 12) == "Command ===>":
            self.emulator.wait_for_field()
            print('mainframe on Command ===>')


class LogInMBBrasTN3270EDS(LogInMBBrasTN3270):

    def mainframe_connection(self):
        self.emulator.send_string('L EDS-CICS', 2, 15)
        self.emulator.move_to(24, 80)
        self.emulator.send_enter()
        self.emulator.wait_for_field()

        if self.emulator.string_get(1, 1, 80).replace(' ', '') == '':
            self.emulator.terminate()
        else:
            if self.emulator.string_get(24, 2, 31) == 'ENTER YOUR USER ID AND PASSWORD':
                self.emulator.send_string('F171305', 18, 23)
                self.emulator.send_string('brasil00', 18, 54)
                self.emulator.move_to(24, 80)
                self.emulator.send_enter()
                self.emulator.wait_for_field()
                if self.emulator.string_get(1, 2, 3) == 'BYE':
                    self.emulator.wait_for_field()
                    if self.emulator.string_get(24, 2, 43) == 'SIGN-ON IS COMPLETE, ENTER TRANSACTION-CODE':
                        self.emulator.send_string('eds', 1, 2)
                        self.emulator.move_to(24, 80)
                        self.emulator.send_enter()
                        self.emulator.wait_for_field()
                # if PDS available and ready
                if self.emulator.string_get(1, 2, 5) == 'E D S':
                    print('EDS on you fuck')
                    return self.emulator


class LogInMBBrasTN3270PDS(LogInMBBrasTN3270):

    def pds_connection(self, app_name, app_plant):
        self.emulator.send_string(app_name, 2, 15)
        self.emulator.move_to(24, 80)
        self.emulator.send_enter()
        self.emulator.wait_for_field()

        if self.emulator.string_get(1, 1, 80).replace(' ', '') == '':
            self.emulator.terminate()
        else:
            self.emulator.send_string('PDS', 3, 2)
            self.emulator.move_to(24, 80)
            self.emulator.send_enter()
            self.emulator.wait_for_field()

            if self.emulator.string_get(1, 25, 4) == 'NFC:' and self.emulator.string_get(19, 32, 9) == 'PASSWORT:':
                self.emulator.send_string(app_plant, 1, 61)
                self.emulator.send_string('PDS', 19, 43)
                self.emulator.move_to(24, 80)
                self.emulator.send_enter()
                self.emulator.wait_for_field()

                # if PDS available and ready
                if self.emulator.string_get(1, 25, 4) == 'NFC:':

                    print('PDS on you fuck')
                    return self.emulator

    def pds_logout(self):
        self.emulator.send_string('ENDE', 1, 30)
        self.emulator.move_to(24, 80)
        self.emulator.send_enter()
        self.emulator.wait_for_field()
        pds_ende_string = self.emulator.string_get_EBCDIC(12, 1, 80)
        if 'PDS-ENDE' in pds_ende_string.replace(' ', ''):
            self.emulator.send_string('bye', 1, 2)
            self.emulator.move_to(24, 80)
            self.emulator.send_enter()
            self.emulator.wait_for_field()
            if self.emulator.string_get(2, 2, 12) == "Command ===>":
                self.emulator.wait_for_field()
                print('mainframe on Command ===>')
                return self.emulator
        else:
            pass
            # TODO: provide fallback solution


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
# TODO: change all mainframe connections acording to __init__method
