import py3270


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
