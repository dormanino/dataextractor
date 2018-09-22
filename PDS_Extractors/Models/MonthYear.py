import datetime
import locale
from PDS_Extractors.Helpers.MonthsHelper import MonthsHelper


class MonthYear:
    def __init__(self, month: int, year: int, locale_code: str = "en_US"):
        self.month = month
        self.year = year
        self.locale_code = locale_code

    def to_date(self) -> datetime.date:
        return datetime.date(self.year, self.month, 1)

    def to_str(self, locale_code: str = "en_US") -> str:
        # locale.setlocale(locale.LC_ALL, locale_code)
        localized_str = self.to_date().strftime("%b/%Y")
        # locale.setlocale(locale.getdefaultlocale())
        return localized_str

    @staticmethod
    def from_str(month_year_str, locale_code: str = "en_US"):
        month_year_data = month_year_str.split("/")
        month = MonthsHelper.get_ordinal_from_short_name(month_year_data[0], locale_code)
        year = int(month_year_data[1])
        return MonthYear(month, year)
