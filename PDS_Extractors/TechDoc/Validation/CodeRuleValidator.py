from enum import Enum
from typing import List


class CodeRuleValidator:
    
    class Operation(Enum):
        PARENTHESIS = 1
        OR = 2
        AND = 3
        ITEM = 4

    @staticmethod
    def validate(rule: str, qvv_composition: List[str]) -> bool:
        open_parenthesis = '('
        close_parenthesis = ')'
        or_operator = '/'
        and_operator = '+'
        not_operator = "-"
        true_result = '%'
        false_result = '&'

        rule = rule.replace(';', '')

        if rule is None:
            return True
        if rule == '':
            return True
        if rule == true_result:
            return True
        elif rule == not_operator + true_result:
            return False
        elif rule == false_result:
            return False
        elif rule == not_operator + false_result:
            return True

        if open_parenthesis in rule:
            operation = CodeRuleValidator.Operation.PARENTHESIS
        elif or_operator in rule:
            operation = CodeRuleValidator.Operation.OR
        elif and_operator in rule:
            operation = CodeRuleValidator.Operation.AND
        else:
            operation = CodeRuleValidator.Operation.ITEM

        if operation == CodeRuleValidator.Operation.ITEM:
            if rule.startswith(not_operator):
                rule = rule[1:]
                return rule not in qvv_composition
            return rule in qvv_composition

        level = 0
        min_index = 0
        lhs = ''
        for index, char in enumerate(rule):

            if operation == CodeRuleValidator.Operation.PARENTHESIS:
                if char == open_parenthesis:
                    level += 1
                    if level == 1:
                        min_index = index + 1

                elif char == close_parenthesis:
                    if level == 1:
                        max_index = index

                        pre_condition = rule[min_index:max_index]
                        pre_condition_validation = CodeRuleValidator.validate(pre_condition, qvv_composition)
                        symbol = true_result if pre_condition_validation else false_result

                        replace_str = open_parenthesis + pre_condition + close_parenthesis
                        rule = rule.replace(replace_str, symbol)
                        return CodeRuleValidator.validate(rule, qvv_composition)
                    else:
                        level -= 1

            elif operation == CodeRuleValidator.Operation.OR:
                if char == or_operator:
                    is_left_valid = CodeRuleValidator.validate(lhs, qvv_composition)
                    rhs = rule[index + 1:]
                    is_right_valid = CodeRuleValidator.validate(rhs, qvv_composition)

                    return is_left_valid or is_right_valid
                else:
                    lhs += char

            elif operation == CodeRuleValidator.Operation.AND:
                if char == and_operator:
                    is_left_valid = CodeRuleValidator.validate(lhs, qvv_composition)
                    if is_left_valid is False:
                        return False
                    else:
                        rhs = rule[index + 1:]
                        return CodeRuleValidator.validate(rhs, qvv_composition)
                else:
                    lhs += char
