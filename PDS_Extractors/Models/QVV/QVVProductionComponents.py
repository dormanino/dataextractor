from typing import Dict, List

from PDS_Extractors.Models.Component.Component import Component
from PDS_Extractors.Models.QVV.QVVProduction import QVVProduction


class QVVProductionComponents:
    def __init__(self, qvv_production: QVVProduction, valid_components: Dict[str, List[Component]]):
        self.qvv_production: QVVProduction = qvv_production
        self.components: Dict[str, List[Component]] = valid_components
