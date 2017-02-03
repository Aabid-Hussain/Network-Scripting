import re
RegEx = r"((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)(\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)){3}(\s|$))"
#pat = r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}"
#pat = r"\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b"


randStr = "adfd sdf 12 25.25 5.255.255 55.5 192.169.1.2 1.1.1.1 adf 2.0 999.999.999.999"

match = re.findall(RegEx,randStr)
if match:
    for lines in match:
        print lines
else:
    print "No match found"
