"""Test's for test_3."""
# pylint: disable=C0116, W0622

from test_3 import sum_current_time


def test_sum_current_time_incorrect_time_format_empty():
    time_str = ""
    sum = sum_current_time(time_str)
    assert sum == "Error. The time input cannot be empty."


def test_sum_current_time_incorrect_time_format_too_short():
    time_str = "01:02"
    sum = sum_current_time(time_str)
    assert sum == "Invalid time format."


def test_sum_current_time_incorrect_time_format_too_short_2():
    time_str = "01"
    sum = sum_current_time(time_str)
    assert sum == "Invalid time format."


def test_sum_current_time_incorrect_time_format_too_long():
    time_str = "01:02:03:04"
    sum = sum_current_time(time_str)
    assert sum == "Invalid time format."


def test_sum_current_time_incorrect_time_format_too_long_2():
    time_str = "01:02:03:04:76453"
    sum = sum_current_time(time_str)
    assert sum == "Invalid time format."


def test_sum_current_time_incorrect_time_format_letters_in_time():
    time_str = "01:tf:03"
    sum = sum_current_time(time_str)
    assert sum == "Error! Incorrect time_str format, must only contain integers and :"


def test_sum_current_time_incorrect_time_format_letters_in_time_2():
    time_str = "01:tf:awdgtd"
    sum = sum_current_time(time_str)
    assert sum == "Error! Incorrect time_str format, must only contain integers and :"


def test_sum_current_time_incorrect_time_format_numbers_too_long():
    time_str = "01:02222:03"
    sum = sum_current_time(time_str)
    assert sum == "Error, number is too long. Incorrect format."


def test_sum_current_time_incorrect_time_format_numbers_too_long_2():
    time_str = "01:222:03"
    sum = sum_current_time(time_str)
    assert sum == "Error, number is too long. Incorrect format."


def test_sum_current_time_incorrect_time_format_negative_num():
    time_str = "-1:22:03"
    sum = sum_current_time(time_str)
    assert sum == "Error. Must be a positive number."


def test_sum_current_time_incorrect_time_format_negative_num_2():
    time_str = "11:22:-3"
    sum = sum_current_time(time_str)
    assert sum == "Error. Must be a positive number."
