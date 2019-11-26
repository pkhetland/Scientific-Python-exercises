# -*- coding: utf-8 -*-

__author__ = "petter hetland"
__email__ = "pehe@nmbu.no"

import math


def letter_freq(txt):
    """ Function returns a dict with the form
    (UTF-8-code: Number of occurrences), for all letters in the given text.
    """
    letter_count = {}
    for letter in txt:
        letter_count[ord(letter)] = txt.count(letter)
    return letter_count


def entropy(message):
    """Function returns the entropy of a given message, based
    on the mathematical formula for entropy.

    Result
    -----------
    N = len(message),
    n_i = Number of occurrences of each UTF-8-code (letter)
    in the message.
    The entropy value is the negative sum of the entropy of each
    individual character in the message.
    The entropy value in a way represents the average number of questions
    we would need to guess the following letter in the message.
    """
    freq = letter_freq(message)
    entropy_value = 0
    for value in freq:
        frac_i = freq[value] / (len(message))
        entropy_value += -(frac_i * math.log(frac_i, 2))
    return entropy_value


if __name__ == "__main__":
    for msg in "", "aaaa", "aaba", "abcd", "This is a short text.":
        print("{:25}: {:8.3f} bits".format(msg, entropy(msg)))
