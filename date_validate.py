"""This program is to validate the date pattern"""

import re

# February only to the 28th 
regex_01_to_28 = "((0[1-9]|1[0-9]|2[0-8])/02)"

# April, June, September, November have 30 days \
regex_01_to_30 = "((0[1-9]|[12][0-9]|30)/(04|06|09|11))"

# 'all the rest' have 31 days \
regex_01_to_31 = "((0[1-9]|[12][0-9]|3[01])/(01|03|05|07|08|10|12))"

#regex_00_to_96_by_4s := "([02468][048]|[13579][26])";
regex_04_to_96_by_4s = "([02468][48]|[13579][26]|[2468]0)"

# any century, any year (except 0000)\
#regex_0001_to_9999 ="([0-9]{3}[1-9]|[0-9]{2}[1-9][0-9]|[0-9][1-9][0-9]{2}|[1-9][0-9]{3})"

regex_0001_to_9999 ="(?=\d*[1-9])[0-9]{4}"


# February 29th \
regex_29 = "29/02/(([0-9]{2}" + regex_04_to_96_by_4s + ')|(' + regex_04_to_96_by_4s + "00))"


regex_valid_date = "((" + regex_01_to_28 + '|' + regex_01_to_30 + "|" + regex_01_to_31 + ")" + "/" + regex_0001_to_9999 + ")" + "|" + regex_29




## Take input from the user
dat = raw_input(" Enter date in dd/mm/yyyy format : ")

#compile function update the regular expression pattern. Basically add r' into pattern variable 
p = re.compile(regex_valid_date)

# search function does not need pattern here as it is being updated using compile function
match = p.search(dat)
if match :
    print "correct date: ", dat
else :
    print "Error: %s not valid date. Please enter correct date. " %dat

    
    
                

