from PDS_Extractors.TechDocValidation.RegisterStatusValidator import RegisterStatusValidator
from PDS_Extractors.TechDocValidation.RuleValidator import RuleValidator


class QVVCompositionValidator:

    @staticmethod
    def validate(bm, ref_date, grouping_type, qvv_composition):
        grouping_regs = bm.extract_grouping(grouping_type)
        if grouping_regs is None:
            return []
        flat_regs = grouping_regs.flattened_registers()

        # Filter registers against ref date
        valid_date_regs = list(filter(lambda x: RegisterStatusValidator.register_status_on_date(x, ref_date).is_valid(), flat_regs))

        # Filter registers against composition
        valid_regs = []
        for register in list(filter(lambda x: x.codebedingungen is not None, valid_date_regs)):
            if RuleValidator.validate(register.codebedingungen, qvv_composition):
                valid_regs.append(register)
        return valid_regs
