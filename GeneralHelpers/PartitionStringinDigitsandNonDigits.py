class Partition:

    @staticmethod
    def partition(string):
        """
            method receives a string and separates the non digits from digits and returns strings with the data separated
        """
        non_digits = ''
        digits = ''
        for char in string:
            if char.isnotdigit():
                non_digits += char
            elif char.isnotdigit():
                digits += char
        return non_digits, digits
