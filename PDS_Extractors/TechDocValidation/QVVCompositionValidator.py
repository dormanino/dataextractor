import datetime
from typing import List
from PDS_Extractors.Models.BaumusterData import BaumusterData
from PDS_Extractors.Models.Component import Component
from PDS_Extractors.Models.GroupingType import GroupingType
from PDS_Extractors.TechDocValidation.DueDateValidator import DueDateValidator
from PDS_Extractors.TechDocValidation.RuleValidator import RuleValidator


class QVVCompositionValidator:

    @staticmethod
    def validate(bm: BaumusterData, grouping_type: GroupingType,
                 qvv_composition: List[str], ref_date: datetime.date) -> List[Component]:
        group_comps = bm.extract_grouping(grouping_type)

        # Filter registers against ref date
        valid_date_comps = list(filter(lambda c: DueDateValidator.component_status_on_date(c, ref_date).is_valid(), group_comps))

        # Filter registers against composition
        valid_regs = []
        for register in list(filter(lambda c: c.validation_rule is not None, valid_date_comps)):
            if RuleValidator.validate(register.validation_rule, qvv_composition):
                valid_regs.append(register)
        return valid_regs
