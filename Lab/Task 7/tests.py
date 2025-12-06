import io
import logging

import requests
from unittest import TestCase, main
from get_currency import get_currencies
from logger import logger
from quadratics import solve_quadratic

class TestGetCurrencies(TestCase):
    # Получение всех возможных котировок
    def test_get_all_currencies(self):
        self.assertIsInstance(get_currencies(), dict)

    # Получение определённой котировки по коду
    def test_get_some_currencies(self):
        self.assertIsInstance(get_currencies(['USD']), dict)
        self.assertEqual(get_currencies(['AUD'])['AUD']['NumCode'], '036')

    # Неверная подача данных функции
    def test_currencies_invalid_input(self):
        self.assertRaises(TypeError, get_currencies, 123)

    # Ошибка подключения к сайту
    def test_currencies_api_error(self):
        self.assertRaises(requests.exceptions.RequestException, get_currencies, ['USD', 'AUD'], 'https:/')

class TestLogger(TestCase):
    def setUp(self):
        self.nonstandard_stream = io.StringIO()

    # Логирование функции подключения к API
    def test_get_currencies_stringio(self):
        @logger(handle=self.nonstandard_stream)
        def function(codes):
            return get_currencies(codes)

        with self.assertRaises(TypeError):
            function(3456789)

        logs = self.nonstandard_stream.getvalue()
        self.assertIn("INFO", logs)
        self.assertIn('CRITICAL', logs)

        self.nonstandard_stream.truncate(0)

    # Логирование функции решения квадратного уравнения
    def test_solve_quadratics_stringio(self):
        @logger(handle=self.nonstandard_stream)
        def function(a, b, c):
            return solve_quadratic(a, b, c)

        with self.assertRaises(ValueError):
            function(0, 1, 2)

        logs = self.nonstandard_stream.getvalue()
        self.assertIn("INFO", logs)
        self.assertIn('ERROR', logs)

        self.nonstandard_stream.truncate(0)

    def tearDown(self):
        del self.nonstandard_stream


if __name__ == '__main__':
    main()
