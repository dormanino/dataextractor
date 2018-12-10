import py3270
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
