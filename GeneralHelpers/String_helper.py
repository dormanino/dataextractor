def string_divide(string, div):
    l = []
    strp = ''
    i = 0
    while i < len(string):
        strp = string[i:i + div].strip().replace(" ", "")
        if strp != '':
            if Xyz.is_float_try(strp):
                strp = int(strp)
            l.append(strp)
        i += div
    return l


def is_float_try(string):
    try:
        float(string)
        return True
    except ValueError:
        return False
