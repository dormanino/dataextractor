from PDS_Extractors.Helpers.CSVWriter import CSVWriter


class ReportOutput:
    def __init__(self, headers, data_rows):
        self.headers = headers
        self.data_rows = data_rows

    def write(self, filename, path):
        CSVWriter.write(filename, self.headers, self.data_rows, path)