import zxing
import re

reader = zxing.BarCodeReader()
barcode = reader.decode('cedulas_test/contrast.png')

str_ = str(barcode.raw.encode("ascii","ignore")).replace('x02C', '\n').split()[0]
str_ = str_.replace("b'", '')
str_ = str_.replace("\\x002\\", '')
str_ = str_.replace("\\x00", ' ')
str_ = re.sub(r'\s+',' ', str_)

pref = 'PubDSK'
result = []
keep = False
for section in str_.split():
    if keep:
        result.append(section)
    if section.startswith(pref):
        keep = True

if result[0].isnumeric():
    result.pop(0)

data = {'lastname_1': None, 'lastname_2': None, 'name': None, 'id': None, 'RH': None, 'sex': None, 'birth': None}

# 0: ID + Lastname
split_ = re.split('(\d+)', result[0])
data['lastname_1'] = split_[-1]
data['id'] = split_[-2][-10:]

# 1: Second lastname
data['lastname_2'] = result[1]

if len(result) == 4:
    data['name'] = result[2]
elif len(result) == 5:
    data['name'] = result[2] + ' ' + result[3]

data['sex'] = result[-1][1]

data['birth'] = result[-1][2:10]

data['RH'] = result[-1][-2:]

print(data)