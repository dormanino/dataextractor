import datetime
from typing import Dict, List

from PDS_Extractors.Models.Analysis.AnalyzedComponent import AnalyzedComponent
from PDS_Extractors.Models.Baumuster.BaumusterInfo import BaumusterInfo


class AnalyzedBaumusterComponents:
    def __init__(self, baumuster_info: BaumusterInfo, components: Dict[str, List[AnalyzedComponent]],
                 ref_date: datetime.date):
        self.baumuster_info: BaumusterInfo = baumuster_info
        self.components: Dict[str, List[AnalyzedComponent]] = components
        self.ref_date = ref_date
