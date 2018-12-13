import csv


class CSVWriter:

    @staticmethod
    def write(filename, headers, data_rows, path):
        full_path = path + "\\" + filename + ".csv"
        output_file = open(full_path, "w", newline="\n", encoding="utf-8")
        output_writer = csv.writer(output_file)
        # output_writer.writerow(["sep=,"])  # hack to enforce coma separator
        output_writer.writerow(headers)
        for data_row in data_rows:
            output_writer.writerow(data_row)
        output_file.close()
        print("Done!")
