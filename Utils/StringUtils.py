class StringUtils:

    @staticmethod
    def split_digits(string):
        """Receives a string and separates non-digits from digits and returns on a tuple"""
        non_digits = ''
        digits = ''
        for char in string:
            if not char.isdigit():
                non_digits += char
            elif char.isdigit():
                digits += char
        return non_digits, digits

    @staticmethod
    def remove_whitespace(string):
        return string.strip().replace(" ", "")
