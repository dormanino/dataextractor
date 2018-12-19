import datetime


class MainframeDateConverter:
    # class MainframeDateConverter has initial attribute (mainframe_date_format)
    # formatted according datetime.strptime(string[, format]) syntax where
    # the format directives are:
    # %y - year without a century (range 00 to 99)
    # %j - day of the year (001 to 366)

    mainframe_date_format = '%y%j'

    @staticmethod
    def mainframe_to_date(date_string: str) -> datetime.date:
        # date from PDS extractor usually comes with a space between year and day
        # that requires to be removed for strptime to work
        rectified_date_string = date_string.replace(" ", "")
        # returns a date according to datetime.date
        return datetime.datetime.strptime(rectified_date_string, MainframeDateConverter.mainframe_date_format).date()

    @staticmethod
    def date_to_mainframe(date: datetime.date) -> str:
        # returns a date according to PDS julian calendar format
        return date.strftime(MainframeDateConverter.mainframe_date_format)
