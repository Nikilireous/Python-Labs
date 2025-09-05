def find_target(list_of_numbers: list, target: int):
    length = len(list_of_numbers)

    for i in range(0, length):
        a = list_of_numbers[i]

        try:
            if a < target:
                j = list_of_numbers.index(target - a, i + 1)
                return [i, j]
        except ValueError:
            pass
        except TypeError:
            if isinstance(target, int):
                return 'Wrong data type'
            return 'Wrong target type'



nums = [1, 3, 4]
target = 4
print(find_target(nums, target))