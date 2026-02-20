from unittest import TestCase, main
from gen_bin_tree import gen_bin_tree


class GuesserTest(TestCase):

    # Значения функции по умолчанию
    def test_default_values(self):
        self.assertEqual(gen_bin_tree(),
                         {4: [{16: [{64: [{256: []}, {65: []}]}, {17: [{68: []}, {18: []}]}]}, {5: [{20: [{80: []}, {21: []}]}, {6: [{24: []}, {7: []}]}]}]})

    # Правильный набор данных, подан один аргумент
    def test_root_exist(self):
        self.assertEqual(gen_bin_tree(root=1),
                         {1: [{4: [{16: [{64: []}, {17: []}]}, {5: [{20: []}, {6: []}]}]}, {2: [{8: [{32: []}, {9: []}]}, {3: [{12: []}, {4: []}]}]}]})

    def test_height_exist(self):
        self.assertEqual(gen_bin_tree(height=1),
                         {4: []})

    # Правильный набор данных, поданы оба аргумента
    def test_gen_tree_exist(self):
        self.assertEqual(gen_bin_tree(root=0, height=3),
                         {0: [{0: [{0: []}, {1: []}]}, {1: [{4: []}, {2: []}]}]})

    # Высота дерева равна нулю
    def test_gen_zero_tree(self):
        self.assertRaises(ValueError, gen_bin_tree, 5, 0)

    # Аргументы поданы неправильно
    def test_wrong_root_type(self):
        self.assertRaises(TypeError, gen_bin_tree, '1', 5)

    def test_wrong_height_type(self):
        self.assertRaises(TypeError, gen_bin_tree, 1, 5.6789)


if __name__ == '__main__':
    main()
