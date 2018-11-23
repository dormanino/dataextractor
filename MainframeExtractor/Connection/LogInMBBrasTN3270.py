from MainframeExtractor.Connection.MBBrasMainframeTN3270Connection import MBBrasMainframeTN3270Connection


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
