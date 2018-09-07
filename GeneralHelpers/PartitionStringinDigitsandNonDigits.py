class Partition:

    @staticmethod
    def partition(string):
        """
            method receives a string and separates the non digits from digits and returns strings with the data separated
        """
        non_digits = ''
        digits = ''
        for char in string:
            if not char.isdigit():
                non_digits += char
            elif char.isdigit():
                digits += char
        return non_digits, digits
