class Parse:
    @staticmethod
    def parse(string):
        sub_str = ''
        sub_str_lst = []
        for char_index, i in enumerate(string):
            if i != ' ':
                sub_str += i
            if char_index != (len(string)-1):
                if string[char_index + 1] == ' ':
                    if sub_str != '':
                        sub_str_lst.append(sub_str)
                        sub_str = ''
            else:
                if sub_str != '':
                    sub_str_lst.append(sub_str)

        return sub_str_lst
