import datetime


class MainframeDateConverter:
    mainframe_date_format = '%y%j'

    @staticmethod
    def mainframe_to_date(date_string: str) -> datetime.date:
        rectified_date_string = date_string.replace(" ", "")
        return datetime.datetime.strptime(rectified_date_string, MainframeDateConverter.mainframe_date_format).date()

    @staticmethod
    def date_to_mainframe(date: datetime.date) -> str:
        return date.strftime(MainframeDateConverter.mainframe_date_format)
