def gen_bin_tree(root: int = 4, height: int = 4,
                 left_branch = lambda x: x * 4, right_branch = lambda x: x + 1) -> dict | Exception:
    """
    Создать бинарное дерево

    :param root: -- указатель корня
    :param height: -- высота генерируемого дерева (целое число от единицы)
    :param left_branch: -- уравнение левой ветки
    :param right_branch: -- уравнение правой ветки
    :return: Созданное бинарное дерево в виде словаря
    """
    if not isinstance(root, int):
        raise TypeError("Значение параметра root должно являться целым числом")
    if not isinstance(height, int):
        raise TypeError("Значение параметра height должно являться целым числом")

    if height < 1:
        raise ValueError("Значение параметра height должно быть больше 0")

    # Создание каждого листка дерева
    stack = [[{root: []}]]
    for cur_height in range(height - 1):
        new_level = []

        for cur_root in stack[cur_height]:
            new_level.append({left_branch(tuple(cur_root.keys())[0]): []})
            new_level.append({right_branch(tuple(cur_root.keys())[0]): []})

        stack.append(new_level)

    # Сборка дерева, начиная с нижнего уровня
    for i in range(height - 1, 0, -1):
        for j in range(2 ** (i - 1)):
            current_key = tuple(stack[i - 1][j].keys())[0]
            stack[i - 1][j][current_key] = stack[i][j * 2: (j + 1) * 2]
        del stack[i]

    return stack[0][0]