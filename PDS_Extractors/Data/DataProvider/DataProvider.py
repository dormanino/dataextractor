import json
from Models import AGRMZ


class DataProvider:

    def __init__(self):
        self.bm_info = self.load_bm_info()

    @staticmethod
    def load_bm_info():
        data = json.load(open(Data))
