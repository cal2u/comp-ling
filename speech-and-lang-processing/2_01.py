#!/usr/bin/python
import re


def test_regex(regex):
    test_cases = [
        "Well, hello there.",
        "123 - 1324-555(123)(A123) (ABC)",
        "Yikes! That's interesting to me .",
        "Crab cakes are yummy?",
        "Chicka chicka boom boom",
        "Rabal Furnishings has sold to Abandonded Decorators.",
        "1.) The end.",
        "The raven in the grotto.",
        "The grotto in the raven."
    ]
    
    return [re.findall(regex, test) for test in test_cases if re.search(regex, test)]

print "1. Alphabetic strings: \n", test_regex(r'[a-zA-Z]+'), "\n"

print "2. Lowercase alphabetic strings ending in 'b': \n", test_regex(r'[a-z]*b')


