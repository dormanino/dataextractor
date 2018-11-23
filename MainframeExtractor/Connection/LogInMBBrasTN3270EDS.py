from MainframeExtractor.Connection.LogInMBBrasTN3270 import LogInMBBrasTN3270


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
