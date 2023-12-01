# The below function doesn't work correctly. It should sum all the numbers at the
# current time. For example, 01:02:03 should return 6. Improve and fix the function,
# and write unit test(s) for it. Use any testing framework you're familiar with.


# [TODO]: fix the function
def sum_current_time(time_str: str) -> int:
    """Expects data in the format HH:MM:SS"""
    list_of_nums = time_str.split(":")

    if len(list_of_nums) != 3:
        return "Invalid number in list."

    list_of_int_nums = []

    for num in list_of_nums:

        try:
            list_of_int_nums.append(int(num))
        except ValueError:
            return "Error! Incorrect time_str format, must only contain integers and :"

    for num in list_of_nums:

        if len(num) != 1 or len(num) != 2:
            return "Error, number is too long. Incorrect format."

    print(list_of_int_nums)
    return sum(list_of_int_nums)


if __name__ == "__main__":

    print(sum_current_time("01:0222:03"))
