from datetime import datetime
import os


class LatestFileVersion:

    @staticmethod
    def latest_file_version(extension, prefix, current=''):
        if current == '':
            current = os.getcwd()
        swap_date_time = None
        final_file_name = ''
        for file in os.listdir(os.fsencode(current)):
            filename = os.fsdecode(file)
            if filename.endswith(extension):
                file_name = os.path.basename(os.path.splitext(file.decode())[0])
                # TODO: filename_find looks for string. if other filename contains the prefix as partial name, it will return error
                if not file_name.find(prefix) == -1:
                    file_date_delta = (datetime.today() - datetime.strptime(file_name[0:6], '%y%m%d')).days
                    if swap_date_time is None:
                        swap_date_time = file_date_delta
                        final_file_name = filename
                    else:
                        if swap_date_time > file_date_delta:
                            swap_date_time = file_date_delta
                            final_file_name = filename
                        else:
                            final_file_name = filename  # forced repetition since error occured ina alternate case

        if not final_file_name == '':
            return current + '\\' + final_file_name
        else:
            return 'file not found'
