from unittest import TestCase, main
from number_guesser import number_guesser


class GuesserTest(TestCase):

    # Правильный набор данных, переданы границы, число может быть найдено (медленный перебор)
    def test_slow_research_borders_exist(self):
        self.assertEqual(number_guesser(1, 0, 2), [1, 2])

    # Правильный набор данных, переданы границы, число может быть найдено (бинарный поиск)
    def test_binary_research_borders_exist(self):
        self.assertEqual(number_guesser(1, 0, 6), [1, 2])

    # Правильный набор данных, передан массив, число может быть найдено (медленный перебор)
    def test_slow_research_array_exist(self):
        self.assertEqual(number_guesser(1, [1, 2, 9]), [1, 1])

    # Правильный набор данных, передан массив, число может быть найдено (бинарный поиск)
    def test_binary_research_array_exist(self):
        self.assertEqual(number_guesser(1, [1, 2, 3, 6, 7, 9, 33, 4]), [1, 4])

    # Правильный набор данных, переданы границы, число не может быть найдено
    def test_research_borders_not_exist(self):
        self.assertIsInstance(number_guesser(55, 1, 10), str)

    # Правильный набор данных, передан массив, число не может быть найдено
    def test_research_array_not_exist(self):
        self.assertIsInstance(number_guesser(55, [8, 100, 77]), str)

    # Правильный набор данных, передан пустой массив
    def test_empty_array(self):
        self.assertIsInstance(number_guesser(7, []), str)

    # Аргументы поданы неправильно
    def test_wrong_guesser_type(self):
        self.assertRaises(TypeError, number_guesser, '1', 0, 1000)

    def test_wrong_left_border_type(self):
        self.assertRaises(TypeError, number_guesser, 4, '2', 100)

    def test_wrong_right_border_type(self):
        self.assertRaises(TypeError, number_guesser, 4, 2, '100')

    def test_left_higher_than_right(self):
        self.assertRaises(ValueError, number_guesser, 50, 100, 0)

    def test_wrong_array_type(self):
        self.assertRaises(TypeError, number_guesser, 3, ['3', '7', 6, 8])


if __name__ == '__main__':
    main()
