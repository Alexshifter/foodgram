import re


pattern = r'^[-a-zA-Z0-9_]+$'

s = input()

if re.match(pattern,s):
    print('da')
else:
    print('net')
