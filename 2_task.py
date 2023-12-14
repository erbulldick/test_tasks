import re

file_path = '*/Test/files/1.xls, */Test/files/2.XLSX, */Test/files/9.vra, */Test/files/3.jpg, */Test/files/4.xml, */Test/files/5.png, */Test/files/6.xlsm, */Test/files/7.xlso, */Test/files/8.xls*, */Test/files/9.xlasx, */Test/files/9.vba'
regex = r'\b(xls|xlsx|xlsm|vba)\b'


def format_verification():
    result = []
    for i in file_path.split(','):
        if re.search(r'\.(xls|XLSX|xlsm|vba)$', i):
            result.append(i)

    return result


if __name__ == '__main__':
    print(format_verification())



