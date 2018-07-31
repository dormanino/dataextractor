import datetime

from PDS_Extractors.Data.DataProvider.SAAProvider import DataProvider
from PDS_Extractors.TechDocValidation.SAAValidator import SAAValidator, SAAStatus


class Xablau:
    def __init__(self, saa, analysis):
        self.saa = saa
        self.analysis = analysis

    def printcomment(self):
        print("SAA #" + str(self.saa.id) + ": " + str(self.analysis.status.value) + " - " + self.analysis.comment)


ref_date = datetime.datetime.now()
data = DataProvider.load_saas()
invalid = []
for saa in data:
    analysis = SAAValidator.saa_status_on_date(saa, ref_date)
    if analysis.status is SAAStatus.Canceled:
        invalid.append(Xablau(saa, analysis))

print("INVALIDOS " + str(len(invalid)))
for xablau in invalid:
    xablau.printcomment()
