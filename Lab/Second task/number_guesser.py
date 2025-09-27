def number_guesser(to_guess: int, left_border: int | list[int] | tuple[int],
                   right_border: int | None = None) -> list[int] | str | Exception:
    """
    Угадает число в указанных границах

    :param to_guess -- число, загаданное пользователем.
    :param left_border -- число правой границы или массив чисел.
    :param right_border -- число левой границы (можно не указывать, если передан массив).
    :return: Угаданное число и количество шагов угадывания
    """
    if not isinstance(to_guess, int):
        raise TypeError("Параметр to_guess обязан быть целым числом")
    if not isinstance(left_border, int) and not isinstance(left_border, list) and not isinstance(left_border, tuple):
        raise TypeError("Параметр left_border должен быть целым числом или массивом чисел")

    all_numbers: list[int] = []
    if isinstance(left_border, int):
        if not isinstance(right_border, int):
            raise TypeError("Параметр right_border обязан быть целым числом")
        if left_border > right_border:
            raise ValueError("Параметр left_border должен быть не больше right_border")

        # Формирует список чисел
        all_numbers: list[int] = [i for i in range(left_border, right_border + 1)]

    if isinstance(left_border, list) or isinstance(left_border, tuple):
        # Формирует список чисел
        try:
            all_numbers: list[int] = sorted(left_border)
        except TypeError:
            raise TypeError("Массив должен состоять только из целых чисел")

    if len(all_numbers) <= 3:
        for i in range(len(all_numbers)):
            if all_numbers[i] == to_guess:
                return [to_guess, i + 1]  # Возвращает угаданное число и количество попыток

    else:
        counter: int = 1  # Счетчик угадываний функции

        # Бинарный поиск
        while all_numbers:
            length: int = len(all_numbers)  # Длина списка
            mid: int = length // 2  # Середина списка

            if all_numbers[mid] == to_guess:
                return [to_guess, counter]  # Возвращает угаданное число и количество попыток

            if to_guess > all_numbers[mid]:
                all_numbers = all_numbers[mid + 1:]
            else:
                all_numbers = all_numbers[:mid]
            counter += 1  # Увеличиваем счётчик угадываний

    return "Число не может быть угадано"
