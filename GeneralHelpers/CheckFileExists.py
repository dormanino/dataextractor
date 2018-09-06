import os
import time


class Check:

    @staticmethod
    def open_file(path_to_file, attempts=0, timeout=5, sleep_int=5):
        if attempts < timeout and os.path.exists(path_to_file) and os.path.isfile(path_to_file):
            try:
                return True
            except:
                # perform an action
                time.sleep(sleep_int)
                Check.open_file(path_to_file, attempts+1)
