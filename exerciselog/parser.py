# -*- coding: utf-8 -*-
"""
"""

import sys
import decimal
from pyparsing import *

import locale
loc = locale.getlocale() # get current locale
print(loc)
# use German locale; name might vary with platform

# print ('%20s: %10s  %10s' % ('name', locale.currency(1234.56), locale.currency(-1234.56)))

locale.setlocale(locale.LC_ALL, 'de')


ws = ' \t'
ParserElement.setDefaultWhitespaceChars(ws)

# Define punctuation and legal characters.
backslash = '\\'
hashmark = '#'
colon = ':'

unicode_printables = ''.join(chr(c) for c in range(65536)
                             if not chr(c).isspace())

standard_chars = unicode_printables.replace(backslash, '').replace(hashmark, '')


float_number = Regex(r'\d+(\.\d*)?').setParseAction( lambda s, l, t: [ decimal.Decimal(t[0]) ] )

unit = oneOf(('kg', 'lbs')).setResultsName('unit')

weight = float_number.setResultsName('weight') + Optional(unit)

# ws = ' \t'
exercise = Word(unicode_printables).setResultsName('exercise')

integer = Word(nums).setParseAction( lambda s,l,t: int(t[0]) )

times = Suppress('x') + integer

# repetitions = Suppress('x') + integer

sets_reps = times.setResultsName('x1') + Optional(times).setResultsName('x2')

reps = (Suppress('x') + integer + OneOrMore(Suppress('|') + integer)).setResultsName('reps')

exercise_set = exercise + OneOrMore(weight + Or((sets_reps, reps))).setResultsName('weight_reps')

tests = [
    ('Squat 125x3x5', ['Squat', decimal.Decimal(125), 3, 5]),
    ('Drücken 60x3x5', ['Drücken', 60.0, 3, 5]),
    ('Drcken 62.5x1x5', ['Drcken', 62.5, 1, 5]),
    ('Drcken 62.5kg x 1 x 5', ['Drcken', 62.5, 'kg', 1, 5]),
    ('Bankdrcken 97.5x3', ['Bankdrcken', 97.5, 3]),
    ('Bankdrcken 220lbsx3 ', ['Bankdrcken', 220, 'lbs', 3]),
    ('Kreuzheben 400kgx3|2|1 ', ['Kreuzheben', 400, 'kg', 3]),
    ('Kreuzheben 300x5|4 250x4x4 200x3|2|1 ', ['Kreuzheben', 300, 'lbs', 3]),
    ('Drcken 62.5kg x 1 x 5', ['Drcken', 62.5, 'kg', 3, 5]),
]

# print('TEST')
# print('TEST')
# print('TEST')
# print('TEST')

for test, expected in tests:
    result = exercise_set.parseString(test)
    print('{}'.format(test))
    print("Parsing `{}` resulted in {} (expected: {}) -> {}".format(
          test, result, expected,
          'PASSED' if list(result) == expected else 'FAILED'))
    # print('YOHO')

    # pprint('TEST')
    # sys.stderr.write('YOHOOOO')

