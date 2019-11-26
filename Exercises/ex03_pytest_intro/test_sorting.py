# -*- coding: utf-8 -*-

__author__ = "Petter Hetland"
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


def test_empty():
    """Test that the sorting function works for empty list
    """
    assert bubble_sort([]) == []


def test_single():
    """Test that the sorting function works for single-element list
    """
    assert bubble_sort([9]) == [9]


def test_sorted_is_not_original():
    """
    Test that the sorting function returns a new object.

    Consider

    data = [3, 2, 1]
    sorted_data = bubble_sort(data)

    Now sorted_data shall be a different object than data,
    not just another name for the same object.
    """
    data = [3, 2, 1]
    sorted_data = bubble_sort(data)
    assert sorted_data != data


def test_original_unchanged():
    """
    Test that sorting leaves the original data unchanged.

    Consider

    data = [3, 2, 1]
    sorted_data = bubble_sort(data)

    Now data shall still contain [3, 2, 1].
    """
    data = [3, 2, 1]
    sorted_data = bubble_sort(data)
    assert data == [3, 2, 1]


def test_sort_sorted():
    """Test that sorting works on sorted data."""
    data = [5, 7, 2, 5, 1]
    sorted_data = bubble_sort(data)
    double_sorted_data = bubble_sort(sorted_data)
    assert double_sorted_data == sorted_data


def test_sort_reversed():
    """Test that sorting works on reverse-sorted data."""
    reverse_data = [6, 5, 4, 3, 2, 1]
    sorted_data = bubble_sort(reverse_data)
    assert sorted_data == [1, 2, 3, 4, 5, 6]


def test_sort_all_equal():
    """Test that sorting handles data with identical elements."""
    data = list(5 for _ in range(5))
    sorted_data = bubble_sort(data)
    assert sorted_data == list(5 for _ in range(5))


def test_sorting():
    """
    Test sorting for various test cases.

    This test case should test sorting of a range of data sets and
    ensure that they are sorted correctly. These could be lists of
    numbers of different length or lists of strings.
    """
    data_1 = [5, 7, 4, 2, 8]
    data_2 = [8, 5]
    data_3 = ["F", "U", "B", "A", "R"]
    sorted_data_1 = bubble_sort(data_1)
    sorted_data_2 = bubble_sort(data_2)
    sorted_data_3 = bubble_sort(data_3)

    assert sorted_data_1 == sorted(data_1)
    assert sorted_data_2 == sorted(data_2)
    assert sorted_data_3 == sorted(data_3)
