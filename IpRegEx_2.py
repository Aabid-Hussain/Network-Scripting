#This is program to find out IPv4 address pattern

import re

randStr = "adfd sdf 12 25.25 5.255.255 55.5 192.169.1.2 1.1.1.1 adf 2.0"

RegEx = r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b"
#Using this expression, we can find a word which has 1 or more number but not more than 3 grouped together in dotted
# decimal format.
#\d{1,3}\. meaning any number from 0 to 9 grouped together to as single digit, double digits or triple digits

matches = re.findall(RegEx,randStr)

for lines in matches:
    print lines
