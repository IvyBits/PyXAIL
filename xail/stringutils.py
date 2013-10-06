import os
import re

__all__ = ['rewhite', 'strip_clean', 'normalize']

_encoding = 'mbcs' if os.name == 'nt' else 'utf-8'
rewhite = re.compile(r'\s+')


def strip_clean(text, allow=frozenset('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz +\'')):
    # List comprehension is the fastest
    return ''.join([c for c in text if c in allow])


def normalize(text):
    if type(text) is not unicode:
        text = unicode(text, _encoding, 'ignore')
    return text
