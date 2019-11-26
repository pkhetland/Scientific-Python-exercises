# -*- coding: utf-8 -*-

__author__ = "petter hetland"
__email__ = "pehe@nmbu.no"


def char_counts(textfilename):
    """ Opens a given file and uses UTF-8 to count the amount
    of occurences of each element in the given file.
    """
    with open(textfilename, "r") as f:
        string = f.read()
        result = [string.count(chr(i)) for i in range(256)]
        f.close()
        return result


if __name__ == '__main__':
    filename = 'file_to_be_read.txt'
    frequencies = char_counts(filename)
    for code in range(256):
        if frequencies[code] > 0:
            character = ''
            if code >= 32:
                character = chr(code)

            print(
                '{:3}{:>4}{:6}'.format(
                    code, character, frequencies[code]
                )
            )
