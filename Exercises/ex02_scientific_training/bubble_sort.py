# -*- coding: utf-8 -*-

__author__ = "petter hetland"
__email__ = "pehe@nmbu.no"


def bubble_sort(list_or_tuple):
    """ Function takes in a list or tuple and uses bubble sort
    to iterate through the list and exchange a higher preceding number with
    the lower number that follows it.

    It does this N times, where N is the amount of items in the original data-
    entry.
    """
    sorted_list = list(list_or_tuple)
    for _ in sorted_list:
        for i in range(0, (len(sorted_list) - 1)):
            if sorted_list[i] > sorted_list[i + 1]:
                sorted_list[i], sorted_list[i + 1] = (
                    sorted_list[i + 1],
                    sorted_list[i],
                )
    return sorted_list


if __name__ == "__main__":
    for data in ((), (1,), (1, 3, 8, 12), (12, 8, 3, 1), (8, 3, 12, 1)):
        print("{!s:>15} --> {!s:>15}".format(data, bubble_sort(data)))
