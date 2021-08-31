import zxing
import re


def found_pref(str_, pref):
    idx_ = 0
    for idx, section in enumerate(str_.split()):
        if section.startswith(pref):
            idx_ = idx + 1
            break
    return idx_


def find_second_lastname(list_str):
    lastname2 = None
    idx_ = 0
    for idx, item in enumerate(list_str):
        if item.isalpha():
            lastname2 = item
            idx_ = idx - 1
            break
    return idx_, lastname2


def find_names(list_str, idx):
    names = []
    next_ = 0
    for i in range(idx, len(list_str)):
        if list_str[i].isalpha():
            names.append(list_str[i])
        else:
            next_ = i
            break
    return next_, ' '.join(x for x in names)


def find_rh(str_):
    rh_idx = None
    for idx, item in enumerate(str_):
        if item.isalpha():
            rh_idx = idx
            break
    return str_[rh_idx:]


reader = zxing.BarCodeReader()
barcode = reader.decode('cedulas_test/barcode_tmp.jpg')

str_ = str(barcode.raw.encode("ascii","ignore"))
str_ = re.sub(r'\s+',' ', str_)
str_ = str_.replace("b'", '')
str_ = str_.replace("\\x002\\", '')
str_ = str_.replace("\\x00", ' ')
str_ = re.sub(r'\s+',' ', str_)

pref = 'PubDSK'
start = found_pref(str_, pref)
result = str_.split()[start:]

if result[0].isnumeric():
    result.pop(0)

data = {'lastname_1': None, 'lastname_2': None, 'names': None, 'id': None, 'RH': None, 'sex': None, 'birth': None}

# Second lastname
lastname1_idx, data['lastname_2'] = find_second_lastname(result)

# ID + Lastname
split_ = re.split(r'(\d+)', result[lastname1_idx])
data['lastname_1'] = split_[-1]
data['id'] = int(split_[-2][-10:])

# names
misc_data_idx, data['names'] = find_names(result, lastname1_idx + 2)

misc_data = result[misc_data_idx][1:].split('x0')[0]

data['sex'] = misc_data[0]

data['birth'] = misc_data[1:9]

data['RH'] = find_rh(misc_data[10:])

print(data)
