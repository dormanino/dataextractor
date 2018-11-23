import time


class EmulatorPosition:
    def __init__(self, line, col):
        self.line = line
        self.col = col


class EmulatorHelper:
    @staticmethod
    def go_to(emulator, position):
        emulator.move_to(position.line, position.col)

    @staticmethod
    def go_to_end_position(emulator):
        end_position = EmulatorPosition(24, 80)
        EmulatorHelper.go_to(emulator, end_position)

    @staticmethod
    def hit_enter(emulator):
        EmulatorHelper.go_to_end_position(emulator)
        emulator.send_enter()
        emulator.wait_for_field()

    @staticmethod
    def go_to_next_screen(emulator):
        EmulatorHelper.hit_enter(emulator)
        time.sleep(1)

    @staticmethod
    def set_value(emulator, value, position):
        emulator.move_to(position.line, position.col)
        emulator.send_eraseEOF()
        emulator.send_string(value, position.line, position.col)

    @staticmethod
    def get_value(emulator, position, length):
        return emulator.string_get(position.line, position.col, length)
