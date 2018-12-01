from MainframeExtractor.Connection.LogInMBBrasTN3270 import LogInMBBrasTN3270


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
