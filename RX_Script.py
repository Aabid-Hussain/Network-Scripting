# Regular expressions allow you to locate and change
# strings in very powerful ways.
# They work in almost exactly the same way in every
# programming language as well.

# Regular Expressions (Regex) are used to
# 1. Search for a specific string in a large amount of data
# 2. Verify that a string has the proper format (Email, Phone #)
# 3. Find a string and replace it with another string
# 4. Format data into the proper form for importing for example

# import the Regex module
import re

# ---------- Was a Match Found ----------

# Search for ape in the string
if re.search("ape", "The ape was at the apex"):
    print("There is an ape")

# ---------- Get All Matches ----------

# findall() returns a list of matches
# . is used to match any 1 character or space
allApes = re.findall("ape.", "The ape was at the apex")

for i in allApes:
    print(i)

# finditer returns an iterator of matching objects
# You can use span to get the location

theStr = "The ape was at the apex"

for i in re.finditer("ape.", theStr):
    # Span returns a tuple
    locTuple = i.span()

    print(locTuple)

    # Slice the match out using the tuple values
    print(theStr[locTuple[0]:locTuple[1]])

# ---------- Match 1 of Several Letters ----------

# Square brackets will match any one of the characters between
# the brackets not including upper and lowercase varieties
# unless they are listed

animalStr = "Cat rat mat fat pat"

allAnimals = re.findall("[crmfp]at", animalStr)
for i in allAnimals:
    print(i)

print()

# We can also allow for characters in a range
# Remember to include upper and lowercase letters
someAnimals = re.findall("[c-mC-M]at", animalStr)
for i in someAnimals:
    print(i)

print()

# Use ^ to denote any character but whatever characters are
# between the brackets
someAnimals = re.findall("[^Cr]at", animalStr)
for i in someAnimals:
    print(i)

print()

# ---------- Replace All Matches ----------

# Replace matching items in a string

owlFood = "rat cat mat pat"

# You can compile a regex into pattern objects which
# provide additional methods
regex = re.compile("[cr]at")

# sub() replaces items that match the regex in the string
# with the 1st attribute string passed to sub
owlFood = regex.sub("owl", owlFood)

print(owlFood)

# ---------- Solving Backslash Problems ----------

# Regex use the backslash to designate special characters
# and Python does the same inside strings which causes
# issues.

# Let's try to get "\\stuff" out of a string

randStr = "Here is \\stuff"

# This won't find it
print("Find \\stuff : ", re.search("\\stuff", randStr))

# This does, but we have to put in 4 slashes which is
# messy
print("Find \\stuff : ", re.search("\\\\stuff", randStr))

# You can get around this by using raw strings which
# don't treat backslashes as special
print("Find \\stuff : ", re.search(r"\\stuff", randStr))

# ---------- Matching Any Character ----------
# We saw that . matches any character, but what if we
# want to match a period. Backslash the period
# You do the same with [, ] and others

randStr = "F.B.I. I.R.S. CIA"

print("Matches :", len(re.findall(".\..\..", randStr)))

# ---------- Matching Whitespace ----------
# We can match many whitespace characters

randStr = """This is a long
string that goes
on for many lines"""

print(randStr)

# Remove newlines
regex = re.compile("\n")

randStr = regex.sub(" ", randStr)

print(randStr)

# You can also match
# \b : Backspace
# \f : Form Feed
# \r : Carriage Return
# \t : Tab
# \v : Vertical Tab

# You may need to remove \r\n on Windows

# ---------- Matching Any Single Number ----------
# \d can be used instead of [0-9]
# \D is the same as [^0-9]

randStr = "12345"

print("Matches :", len(re.findall("\d", randStr)))

# ---------- Matching Multiple Numbers ----------
# You can match multiple digits by following the \d with {numOfValues}

# Match 5 numbers only
if re.search("\d{5}", "12345"):
    print("It is a zip code")

# You can also match within a range
# Match values that are between 5 and 7 digits
numStr = "123 12345 123456 1234567"

print("Matches :", len(re.findall("\d{5,7}", numStr)))

# ---------- Matching Any Single Letter or Number ----------
# \w is the same as [a-zA-Z0-9_]
# \W is the same as [^a-zA-Z0-9_]

phNum = "412-555-1212"

# Check if it is a phone number
if re.search("\w{3}-\w{3}-\w{4}", phNum):
    print("It is a phone number")

# Check for valid first name between 2 and 20 characters
if re.search("\w{2,20}", "Ultraman"):
    print("It is a valid name")

# ---------- Matching WhiteSpace ----------
# \s is the same as [\f\n\r\t\v]
# \S is the same as [^\f\n\r\t\v]

# Check for valid first and last name with a space
if re.search("\w{2,20}\s\w{2,20}", "Toshio Muramatsu"):
    print("It is a valid full name")

# ---------- Matching One or More ----------
# + matches 1 or more characters

# Match a followed by 1 or more characters
print("Matches :", len(re.findall("a+", "a as ape bug")))

# ---------- Problem ----------
# Create a Regex that matches email addresses from a list
# 1. 1 to 20 lowercase and uppercase letters, numbers, plus ._%+-
# 2. An @ symbol
# 3. 2 to 20 lowercase and uppercase letters, numbers, plus .-
# 4. A period
# 5. 2 to 3 lowercase and uppercase letters

emailList = "db@aol.com m@.com @apple.com db@.com"

print("Email Matches :", len(re.findall("[\w._%+-]{1,20}@[\w.-]{2,20}\.[A-Za-z]{2,3}", emailList)))

# Regular expressions allow you to locate and change
# strings in very powerful ways.
# They work in almost exactly the same way in every
# programming language as well.

# Regular Expressions (Regex) are used to
# 1. Search for a specific string in a large amount of data
# 2. Verify that a string has the proper format (Email, Phone #)
# 3. Find a string and replace it with another string
# 4. Format data into the proper form for importing for example

# import the Regex module
import re

# ---------- Was a Match Found ----------

# Search for ape in the string
if re.search("ape", "The ape was at the apex"):
    print("There is an ape")

# ---------- Get All Matches ----------

# findall() returns a list of matches
# . is used to match any 1 character or space
allApes = re.findall("ape.", "The ape was at the apex")

for i in allApes:
    print(i)

# finditer returns an iterator of matching objects
# You can use span to get the location

theStr = "The ape was at the apex"

for i in re.finditer("ape.", theStr):
    # Span returns a tuple
    locTuple = i.span()

    print(locTuple)

    # Slice the match out using the tuple values
    print(theStr[locTuple[0]:locTuple[1]])

# ---------- Match 1 of Several Letters ----------

# Square brackets will match any one of the characters between
# the brackets not including upper and lowercase varieties
# unless they are listed

animalStr = "Cat rat mat fat pat"

allAnimals = re.findall("[crmfp]at", animalStr)
for i in allAnimals:
    print(i)

print()

# We can also allow for characters in a range
# Remember to include upper and lowercase letters
someAnimals = re.findall("[c-mC-M]at", animalStr)
for i in someAnimals:
    print(i)

print()

# Use ^ to denote any character but whatever characters are
# between the brackets
someAnimals = re.findall("[^Cr]at", animalStr)
for i in someAnimals:
    print(i)

print()

# ---------- Replace All Matches ----------

# Replace matching items in a string

owlFood = "rat cat mat pat"

# You can compile a regex into pattern objects which
# provide additional methods
regex = re.compile("[cr]at")

# sub() replaces items that match the regex in the string
# with the 1st attribute string passed to sub
owlFood = regex.sub("owl", owlFood)

print(owlFood)

# ---------- Solving Backslash Problems ----------

# Regex use the backslash to designate special characters
# and Python does the same inside strings which causes
# issues.

# Let's try to get "\\stuff" out of a string

randStr = "Here is \\stuff"

# This won't find it
print("Find \\stuff : ", re.search("\\stuff", randStr))

# This does, but we have to put in 4 slashes which is
# messy
print("Find \\stuff : ", re.search("\\\\stuff", randStr))

# You can get around this by using raw strings which
# don't treat backslashes as special
print("Find \\stuff : ", re.search(r"\\stuff", randStr))

# ---------- Matching Any Character ----------
# We saw that . matches any character, but what if we
# want to match a period. Backslash the period
# You do the same with [, ] and others

randStr = "F.B.I. I.R.S. CIA"

print("Matches :", len(re.findall(".\..\..", randStr)))

# ---------- Matching Whitespace ----------
# We can match many whitespace characters

randStr = """This is a long
string that goes
on for many lines"""

print(randStr)

# Remove newlines
regex = re.compile("\n")

randStr = regex.sub(" ", randStr)

print(randStr)

# You can also match
# \b : Backspace
# \f : Form Feed
# \r : Carriage Return
# \t : Tab
# \v : Vertical Tab

# You may need to remove \r\n on Windows

# ---------- Matching Any Single Number ----------
# \d can be used instead of [0-9]
# \D is the same as [^0-9]

randStr = "12345"

print("Matches :", len(re.findall("\d", randStr)))

# ---------- Matching Multiple Numbers ----------
# You can match multiple digits by following the \d with {numOfValues}

# Match 5 numbers only
if re.search("\d{5}", "12345"):
    print("It is a zip code")

# You can also match within a range
# Match values that are between 5 and 7 digits
numStr = "123 12345 123456 1234567"

print("Matches :", len(re.findall("\d{5,7}", numStr)))

# ---------- Matching Any Single Letter or Number ----------
# \w is the same as [a-zA-Z0-9_]
# \W is the same as [^a-zA-Z0-9_]

phNum = "412-555-1212"

# Check if it is a phone number
if re.search("\w{3}-\w{3}-\w{4}", phNum):
    print("It is a phone number")

# Check for valid first name between 2 and 20 characters
if re.search("\w{2,20}", "Ultraman"):
    print("It is a valid name")

# ---------- Matching WhiteSpace ----------
# \s is the same as [\f\n\r\t\v]
# \S is the same as [^\f\n\r\t\v]

# Check for valid first and last name with a space
if re.search("\w{2,20}\s\w{2,20}", "Toshio Muramatsu"):
    print("It is a valid full name")

# ---------- Matching One or More ----------
# + matches 1 or more characters

# Match a followed by 1 or more characters
print("Matches :", len(re.findall("a+", "a as ape bug")))

# ---------- Problem ----------
# Create a Regex that matches email addresses from a list
# 1. 1 to 20 lowercase and uppercase letters, numbers, plus ._%+-
# 2. An @ symbol
# 3. 2 to 20 lowercase and uppercase letters, numbers, plus .-
# 4. A period
# 5. 2 to 3 lowercase and uppercase letters

emailList = "db@aol.com m@.com @apple.com db@.com"

print("Email Matches :", len(re.findall("[\w._%+-]{1,20}@[\w.-]{2,20}.[A-Za-z]{2,3}",
                                        emailList)))



# Did you find a match
# if re.search("REGEX", yourString)

# Get list of matches
# print("Matches :", len(re.findall("REGEX", yourString)))

# Get a pattern object
# regex = re.compile("REGEX")

# Substitute the match
# yourString = regex.sub("substitution", yourString)

# [ ]   : Match what is in the brackets
# [^ ]  : Match anything not in the brackets
# .     : Match any 1 character or space
# +     : Match 1 or more of what proceeds
# \n    : Newline
# \d    : Any 1 number
# \D    : Anything but a number
# \w    : Same as [a-zA-Z0-9_]
# \W    : Same as [^a-zA-Z0-9_]
# \s    : Same as [\f\n\r\t\v]
# \S    : Same as [^\f\n\r\t\v]
# {5}   : Match 5 of what proceeds the curly brackets
# {5,7} : Match values that are between 5 and 7 in length

# ---------- Matching Zero or One ----------
import re


randStr = "cat cats"

regex = re.compile("[cat]+s?")

matches = re.findall(regex, randStr)

# Match cat or cats
print("Matches :", len(matches))

for i in matches:
    print(i)

# ---------- Matching Zero or More ----------
# * matches zero or more of what proceeds it

randStr = "doctor doctors doctor's"

# Match doctor doctors or doctor's
regex = re.compile("[doctor]+['s]*")

matches = re.findall(regex, randStr)

print("Matches :", len(matches))

# You can do the same by setting an interval match
regex = re.compile("[doctor]+['s]{0,2}")

matches = re.findall(regex, randStr)

print("Matches :", len(matches))

for i in matches:
    print(i)

# ---------- PROBLEM ----------
# On Windows newlines are some times \n and other times \r\n
# Create a regex that will grab each of the lines in this
# string, print out the number of matches and each line

longStr = '''Just some words
and some more\r
and more
'''

print("Matches :", len(re.findall(r"[\w\s]+[\r]?\n", longStr)))

matches = re.findall("[\w\s]+[\r]?\n", longStr)

for i in matches:
    print(i)

# ---------- Greedy & Lazy Matching ----------

randStr = "<name>Life On Mars</name><name>Freaks and Geeks</name>"

# Let's try to grab everything between <name> tags
# Because * is greedy (It grabs the biggest match possible)
# we can't get what we want, which is each individual tag
# match
regex = re.compile(r"<name>.*</name>")

matches = re.findall(regex, randStr)

print("Matches :", len(matches))

for i in matches:
    print(i)

# We want to grab the smallest match we use *?, +?, or
# {n,}? instead

regex = re.compile(r"<name>.*?</name>")

matches = re.findall(regex, randStr)

print("Matches :", len(matches))

for i in matches:
    print(i)

# ---------- Word Boundaries ----------
# We use word boundaries to define where our matches start
# and end

# \b matches the start or end of a word

# If we want ape it will match ape and the beginning of apex
randStr = "ape at the apex"

regex = re.compile(r"ape")

# If we use the word boundary
regex = re.compile(r"\bape\b")

matches = re.findall(regex, randStr)

print("Matches :", len(matches))

for i in matches:
    print(i)

# ---------- String Boundaries ----------
# ^ : Matches the beginning of a string if outside of
#     a [ ]
# $ : Matches the end of a string

# Grab everything from the start of the string to @
randStr = "Match everything up to @"

regex = re.compile(r"^.*[^@]")

matches = re.findall(regex, randStr)

print("Matches :", len(matches))

for i in matches:
    print(i)

# Grab everything from @ to the end of the line
randStr = "@ Get this string"

regex = re.compile(r"[^@\s].*$")

matches = re.findall(regex, randStr)

print("Matches :", len(matches))

for i in matches:
    print(i)

# Grab the 1st word of each line using the the multiline
# code which allows for the targeting of each line after
# a line break with ^
randStr = '''Ape is big
Turtle is slow
Cheetah is fast'''

regex = re.compile(r"(?m)^.*?\s")

matches = re.findall(regex, randStr)

print("Matches :", len(matches))

for i in matches:
    print(i)

# ---------- Subexpressions ----------
# Subexpressions are parts of a larger expression
# If you want to match for a large block, but
# only want to return part of it. To do that
# surround what you want with ( )

# Get just the number minus the area code
randStr = "My number is 412-555-1212"

regex = re.compile(r"412-(.*)")

matches = re.findall(regex, randStr)

print("Matches :", len(matches))

for i in matches:
    print(i)

# ---------- Problem ----------

# Get just the numbers minus the area codes from
# this string
randStr = "412-555-1212 412-555-1213 412-555-1214"

regex = re.compile(r"412-(.{8})")

matches = re.findall(regex, randStr)

print("Matches :", len(matches))

for i in matches:
    print(i)

# ---------- Multiple Subexpressions ----------

# You can have multiple subexpressions as well
# Get both numbers that follow 412 separately
randStr = "My number is 412-555-1212"

regex = re.compile(r"412-(.*)-(.*)")

matches = re.findall(regex, randStr)

print("Matches :", len(matches))

print(matches[0][0])
print(matches[0][1])

# Did you find a match
# if re.search("REGEX", yourString)

# Get list of matches
# print("Matches :", len(re.findall("REGEX", yourString)))

# Get a pattern object
# regex = re.compile("REGEX")

# Substitute the match
# yourString = regex.sub("substitution", yourString)
# [ ]   : Match what is in the brackets
# [^ ]  : Match anything not in the brackets
# ( )   : Return surrounded submatch
# .     : Match any 1 character or space
# +     : Match 1 or more of what proceeds
# ?     : Match 0 or 1
# *     : Match 0 or More
# *?    : Lazy match the smallest match
# \b    : Word boundary
# ^     : Beginning of String
# $     : End of String
# \n    : Newline
# \d    : Any 1 number
# \D    : Anything but a number
# \w    : Same as [a-zA-Z0-9_]
# \W    : Same as [^a-zA-Z0-9_]
# \s    : Same as [\f\n\r\t\v]
# \S    : Same as [^\f\n\r\t\v]
# {5}   : Match 5 of what proceeds the curly brackets
# {5,7} : Match values that are between 5 and 7 in length
# ($m)  : Allow ^ on multiline string

# Use a back reference to substitute what is between the
# bold tags and eliminate the bold tags
# re.sub(r"<b>(.*?)</b>", r"\1", randStr)

# Use a look ahead to find all characters of 1 or more
# with a word boundary, but don't return the word
# boundary
# re.findall(r"\w+(?=\b)", randStr)

# Use a look behind to find words starting with a number,
# period and space, but only return the word that follows
# re.findall(r"(?<=\d.\s)\w+", randStr)

# Use a negative look behind to only return numbers without
# a $ in front of them
# re.findall(r"(?<!\$)\d+", randStr)

# ---------- Back References ----------
# A back reference allows you to to reuse the expression
# that proceeds it

# Grab a double word
randStr = "The cat cat fell out the window"

# Match a word boundary, 1 or more characters followed
# by a space if it is then followed by the same
# match that is surrounded by the parentheses
regex = re.compile(r"(\b\w+)\s+\1")

matches = re.findall(regex, randStr)

print("Matches :", len(matches))

for i in matches:
    print(i)

# ---------- Back Reference Substitutions ----------

# Replace the bold tags in the link with no tags
randStr = "<a href='#'><b>The Link</b></a>"

# Regex matches bold tags and grabs the text between
# them to be used by the back reference
regex = re.compile(r"<b>(.*?)</b>")

# Replace the tags with just the text between them
randStr = re.sub(regex, r"\1", randStr)

print(randStr)

# ---------- Another Back Reference Substitution ----------

# Receive this string
randStr = "412-555-1212"

# Match the phone number using multiple subexpressions
regex = re.compile(r"([\d]{3})-([\d]{3}-[\d]{4})")

# Output (412)555-1212
randStr = re.sub(regex, r"(\1)\2", randStr)

print(randStr)

# ---------- PROBLEM ----------
# Receive a string like this

randStr = "https://www.youtube.com http://www.google.com"

# Grab the URL and then provide the following output
# using a back reference substitution
# <a href='https://www.youtube.com'>www.youtube.com</a>
# <a href='https://www.google.com'>www.google.com</a>

regex = re.compile(r"(https?://([\w.]+))")

randStr = re.sub(regex, r"<a href='\1'>\2</a>\n", randStr)

print(randStr)

# ---------- Look Ahead ----------
# A look ahead defines a pattern to match but not return
# You define the expression to look for but not return
# like this (?=expression)

randStr = "One two three four"

# Grab all letters and numbers of 1 or more separated
# by a word boundary but don't include it
regex = re.compile(r"\w+(?=\b)")

matches = re.findall(regex, randStr)

for i in matches:
    print(i)

# ---------- Look Behind ----------
# The look behind looks for what is before the text
# to return, but doesn't return it
# It is defined like (?<=expression)

randStr = "1. Bread 2. Apples 3. Lettuce"

# Find the number, period and space, but only return
# the 1 or more letters or numbers that follow
regex = re.compile(r"(?<=\d.\s)\w+")

matches = re.findall(regex, randStr)

for i in matches:
    print(i)

# ---------- Look Ahead & Behind ----------

randStr = "<h1>I'm Important</h1> <h1>So am I</h1>"

# Use the look behind, get 1 or more of anything,
# and use the look ahead
regex = re.compile(r"(?<=<h1>).+?(?=</h1>)")

matches = re.findall(regex, randStr)

for i in matches:
    print(i)

import re

# ---------- Negative Look Ahead & Behind ----------
# These are used to look for text that doesn't match
# the pattern

# (?!expression) : Negative Look Ahead
# (?<!expression) : Negative Look Behind

randStr = "8 Apples $3, 1 Bread $1, 1 Cereal $4"

# Grab the total number of grocery items by ignoring the $
regex = re.compile(r"(?<!\$)\d+")

matches = re.findall(regex, randStr)

print(len(matches))

# Convert from a string list to an int list
matches = [int(i) for i in matches]

from functools import reduce

# Sum the items in the list with reduce
print("Total Items {}".format(reduce((lambda x, y: x + y), matches)))



# ---------- OR CONDITIONAL ----------
# You can use | to define the matches you'll except

randStr = "1. Dog 2. Cat 3. Turtle"

regex = re.compile(r"\d\.\s(Dog|Cat)")

matches = re.findall(regex, randStr)

print(len(matches))

for i in matches:
    print(i)

# ---------- PROBLEM ----------
# Create a regex that will match for 5 digit zip
# codes or zip codes with 5 digits a dash and
# then 4 digits

randStr = "12345 12345-1234 1234 12346-333"

regex = re.compile(r"(\d{5}-\d{4}|\d{5}\s)")

matches = re.findall(regex, randStr)

print(len(matches))

for i in matches:
    print(i)

# ---------- GROUP ----------
# We can use group to retrieve parts of regex
# matches
'''
bd = input("Enter your birthday (mm-dd-yyyy) : ")

bdRegex = re.search(r"(\d{1,2})-(\d{1,2})-(\d{4})", bd)

print("You were born on", bdRegex.group())
print("Birth Month", bdRegex.group(1))
print("Birth Day", bdRegex.group(2))
print("Birth Year", bdRegex.group(3))
'''

# ---------- MATCH OBJECT FUNCTIONS ----------
# There are functions that provide more information
# on your matches

match = re.search(r"\d{2}", "The chicken weighed 13 lbs")

# Print the match
print("Match :", match.group())

# Print the start and ending index of the match
print("Span :", match.span())

# Print starting index of the match
print("Match :", match.start())

# Print the ending index of the match
print("Match :", match.end())

# ---------- NAMED GROUPS ----------
# You can also assign names to matches

randStr = "December 21 1974"

regex = r"^(?P<month>\w+)\s(?P<day>\d+)\s(?P<year>\d+)"

matches = re.search(regex, randStr)

print("Month :", matches.group('month'))
print("Day :", matches.group('day'))
print("Year :", matches.group('year'))

# ---------- PROBLEM ----------
# Find all of the following email addresses

randStr = "d+b@aol.com a_1@yahoo.co.uk A-100@m-b.INTERNATIONAL"

regex = re.compile(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+")

matches = re.findall(regex, randStr)

print(len(matches))

for i in matches:
    print(i)

# ---------- PROBLEM ----------
# Find all of the following phone numbers and then print them

randStr = "14125551212 4125551212 (412)5551212 412 555 1212 412-555-1212 1-412-555-1212"

regex = re.compile(r"((1?)(-| ?)(\()?(\d{3})(\)|-| |\)-|\) )?(\d{3})(-| )?(\d{4}|\d{4}))")

matches = re.findall(regex, randStr)

print(len(matches))

for i in matches:
    print(i[0].lstrip())