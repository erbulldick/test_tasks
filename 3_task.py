import re

pattern = r'^-?\d+$'
input_str = '1 -2 -3 4 5 -6f ss3 0 0 0 -0 0.0 0.05'

def checking_natural_numbers():
    result = []
    for i in input_str.split():
        if re.match(pattern, i):
            result.append(int(i))
    return sorted(set(result))


if __name__ == '__main__':
    print(checking_natural_numbers())