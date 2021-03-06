import datetime
from typing import Dict, List

from PDS_Extractors.Models.Analysis.AnalyzedComponent import AnalyzedComponent
from PDS_Extractors.Models.QVV.QVVProduction import QVVProduction


class AnalyzedQVVComponents:
    def __init__(self, qvv: QVVProduction, components: Dict[str, List[AnalyzedComponent]],
                 ref_date: datetime.date):
        self.qvv_production: QVVProduction = qvv
        self.components: Dict[str, List[AnalyzedComponent]] = components
        self.ref_date = ref_date
