def gen_bin_tree(root: int = 4, height: int = 4) -> dict | Exception:
    """
    Создать бинарное дерево

    :param root: -- указатель корня
    :param height: -- количество ярусов дерева (целое число от нуля)
    :return: Созданное бинарное дерево в виде словаря
    """
    if isinstance(root, int) and isinstance(height, int):
        if height >= 1:
            left_leaf = root * 4  # Формула для указателя левого узла
            right_leaf = root + 1  # Формула для указателя правого узла

            if isinstance(left_leaf, int) and isinstance(right_leaf, int):
                if height - 1:

                    # Создание ветвей бинарного дерева
                    return {root: [gen_bin_tree(left_leaf, height - 1), gen_bin_tree(right_leaf, height - 1)]}

                # Выход из рекурсии
                return {root: []}

            raise ValueError("Значения left_leaf и right_leaf должны быть целыми числам")
        raise ValueError("Значение параметра height должно быть больше 0")

    if not isinstance(root, int):
        raise TypeError("Значение параметра root должно являться целым числом")

    raise TypeError("Значение параметра height должно являться целым числом")
