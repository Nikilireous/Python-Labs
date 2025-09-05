from unittest import TestCase, main
from ex import find_target


class SumFinderTest(TestCase):

    # Правильный набор данных, искомое число может быть составлено
    def test_ordinary_data_exist(self):
        self.assertEqual(find_target([2, 7, 11, 15], 9), [0, 1])

    # Правильный набор данных, искомое число может быть составлено из повторяющихся чисел
    def test_same_data_exist(self):
        self.assertEqual(find_target([3, 3, 3, 3], 6), [0, 1])

    # Правильный набор данных, искомое число не может быть составлено
    def test_ordinary_data_none(self):
        self.assertIsNone(find_target([2, 7, 11, 15], 10), None)

    # Длина списка меньше двух
    def test_small_data(self):
        self.assertIsNone(find_target([2, 7, 11, 15], 10), None)

    # Аргументы поданы неправильно
    def test_wrong_data_type(self):
        self.assertIsInstance(find_target(['1', '1', '1', '1'], 2), str)

    def test_wrong_target_type(self):
        self.assertIsInstance(find_target([1, 1, 1, 1], '2'), str)


if __name__ == '__main__':
    main()
    