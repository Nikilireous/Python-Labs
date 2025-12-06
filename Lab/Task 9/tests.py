from unittest import TestCase, main
from controllers import AppCRUD
from models import App, Author, User, Currency


app_controller = AppCRUD('data/data.db')
class TestSite(TestCase):
    # Получение всех возможных котировок
    def test_get_all_currencies(self):
        self.assertIsInstance(app_controller._read_currencies(), list)

    # Получение определённой котировки по коду
    def test_get_some_currency(self):
        self.assertEqual(app_controller._read_currencies('R01010')[0].char_code, 'AUD')

    # Счёт несуществующей валюты
    def test_no_currency(self):
        self.assertListEqual(app_controller._read_currencies('123'), [])

    # Тестирование геттеров и сеттеров моделей
    def test_App_getter(self):
        author = Author(name='Nikita', group='123', info='qwerty')
        app = App(name='someapp', version='1.1', author=author)
        self.assertEqual(app.name, 'someapp')
        self.assertEqual(app.author, author)

    def test_user_setter(self):
        user = User(user_id=55, name='V', password='$2b$12$CTb4DgIpIUwYi.DYdc2tyO.6pdGVa6xHb4j4PBw0R8T3Cysill8eG')
        self.assertEqual(user.name, 'V')
        user.name = 'Johnny'
        self.assertEqual(user.name, 'Johnny')

    # Неверная подача данных в сеттер
    def test_user_invalid_setter(self):
        user = User(user_id=512, name='Elster', password='$2b$12$pAsHXDFZM7OgBGeHit0fRuR1KMXZFzhJ7hGllS62mb6oAPXoNGupO')
        self.assertRaises(TypeError, user.name, 25512)

if __name__ == '__main__':
    main()