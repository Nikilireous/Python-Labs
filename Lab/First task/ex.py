def find_target(list_of_numbers: list, target: int):
    if not isinstance(list_of_numbers, list):
        raise TypeError("First variable must be 'list' type")
    if not isinstance(target, int):
        raise TypeError("Second variable must be 'int' type")

    length = len(list_of_numbers)

    for i in range(0, length):
        a = list_of_numbers[i]

        if not isinstance(a, int):
            raise TypeError("First variable must contain only 'int' objects")

        try:
            j = list_of_numbers.index(target - a, i + 1)
            return [i, j]
        except ValueError:
            pass
    return None
