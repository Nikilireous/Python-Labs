from math import sqrt


def solve_quadratic(a, b, c):
    # Ошибка типов
    for name, value in zip(("a", "b", "c"), (a, b, c)):
        if not isinstance(value, (int, float)):
            raise TypeError(f"Coefficient '{name}' must be numeric")

    # Ошибка: a == 0
    if a == 0:
        raise ValueError("a cannot be zero")

    d = pow(b, 2) - (4 * a * c)

    if d < 0:
        return None

    if d == 0:
        x = -b / (2 * a)
        return (x,)

    root1 = (-b + sqrt(d)) / (2 * a)
    root2 = (-b - sqrt(d)) / (2 * a)
    return root1, root2
