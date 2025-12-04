from jinja2 import Environment, PackageLoader, select_autoescape
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs, ParseResult
from models import App, Author, Currency, User, UserCurrency
from utils.currencies_api import get_currencies
from requests import exceptions


# Заглушки с тестовой информацией
class UsersMock:
    def __init__(self):
        self.__users = [User(1, 'Ariane', '$2b$12$h4RjolT5K1DAS94NQ.Ou/OOnaG7CPm6BucKwo8tTGg/0ual/iNaFe'),
                        User(2, 'Simon', '$2b$12$avNHezgHP7inIhUm/dY99eLcFPZFwTQ4hWOO0u9ZW1i5ejn.Z9mG2'),
                        User(3, 'Kris', '$2b$12$s1QW4BvpBhVhtiwP/mvxEeKH4EWpuG31tT2cxKZKEyufX1cHu9x22')]

    @property
    def users(self):
        return self.__users

class UsersCurrencyMock:
    def __init__(self):
        self.__data = [UserCurrency(1, 1, 1),
                       UserCurrency(2, 1, 34),
                       UserCurrency(3, 2, 2),
                       UserCurrency(4, 2, 5),
                       UserCurrency(5, 3, 22)]

    @property
    def data(self):
        return self.__data

class UsersCurrencyInfoMock:
    def __init__(self):
        currencies_info = get_currencies().values()
        self.__data = [Currency(num_code=valute['NumCode'],
                               char_code=valute['CharCode'],
                               name=valute['Name'],
                               value=valute['Value'],
                               nominal=valute['Nominal'],
                               valute_id=(index + 1)) for index, valute in enumerate(currencies_info) if (index + 1) in (1, 34, 2, 5, 22)]

    @property
    def data(self):
        return self.__data


# Основное приложение
main_author = Author('Golubkov Nikita', 'P3120', 'https://github.com/Nikilireous')
main_app = App(name='CurrenciesListApp', version='0.0.1', author=main_author)
class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    # Инициализация класса
    def __init__(self, *args):
        super().__init__(*args)
        self.__url_path: ParseResult | None = None

    @property
    def url_path(self):
        return self.__url_path

    @url_path.setter
    def url_path(self, path: ParseResult):
        if type(path) is ParseResult:
            self.__url_path = path
        else:
            raise ValueError('Ошибка при задании имени запроса')

    # Основная функция
    def do_GET(self):
        # Парсинг пути URL
        parsed_path = urlparse(self.path)
        path = parsed_path.path

        routes = {
            '/': self.home_page,
            '/author': self.author_page,
            '/users': self.users_page,
            '/user': self.user_page,
            '/currencies': self.currencies_page
        }

        if path in routes:
            self.url_path = parsed_path
            routes[path]()
        else:
            self.page_404()

    # Функции рендера базовых страниц
    def home_page(self):
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.end_headers()

        template = env.get_template("index.html")
        result = template.render(myapp=main_app.name)

        self.wfile.write(bytes(result, "utf-8"))

    def author_page(self):
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.end_headers()

        template = env.get_template("author.html")
        result = template.render(myapp=main_app.name,
                                 name=main_author.name,
                                 group=main_author.group,
                                 url=main_author.info)

        self.wfile.write(bytes(result, "utf-8"))

    def currencies_page(self):
        try:
            currencies_info = get_currencies().values()
            all_currencies = [Currency(num_code=valute['NumCode'],
                                       char_code=valute['CharCode'],
                                       name=valute['Name'],
                                       value=valute['Value'],
                                       nominal=valute['Nominal'],
                                       valute_id=index + 1) for index, valute in enumerate(currencies_info)]

            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()

            template = env.get_template("currencies.html")
            result = template.render(myapp=main_app.name,
                                     currencies=all_currencies)

            self.wfile.write(bytes(result, "utf-8"))
        except exceptions.RequestException:
            self.page_500()

    def users_page(self):
        try:
            data = UsersMock().users

            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()

            template = env.get_template("users.html")
            result = template.render(myapp=main_app.name,
                                     users=data)

            self.wfile.write(bytes(result, "utf-8"))
        except Exception:
            self.page_500()

    def user_page(self):
        try:
            cur_user_id = int((parse_qs(self.url_path.query)['id'])[0])
            cur_user = [user for user in UsersMock().users if user.user_id == cur_user_id][0]
            cur_info = [info.currency_id for info in UsersCurrencyMock().data if info.user_id == cur_user.user_id]
            cur_currencies = [currency for currency in UsersCurrencyInfoMock().data if currency.valute_id in cur_info]

            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()

            template = env.get_template("user_currencies.html")
            result = template.render(myapp=main_app.name,
                                     user=cur_user,
                                     currencies=cur_currencies)

            self.wfile.write(bytes(result, "utf-8"))
        except IndexError:
            self.page_404()
        except Exception:
            self.page_500()

    # Функции рендера страниц ошибок
    def page_404(self):
        self.send_response(404, 'Page not found')
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.end_headers()

        template = env.get_template("error404.html")
        result = template.render(myapp=main_app.name)

        self.wfile.write(bytes(result, "utf-8"))

    def page_500(self):
        self.send_response(500, 'Internal server error')
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.end_headers()

        template = env.get_template("error500.html")
        result = template.render(myapp=main_app.name)

        self.wfile.write(bytes(result, "utf-8"))


# Создание окружения
env = Environment(
    loader=PackageLoader("myapp"),
    autoescape=select_autoescape()
)

# Запуск сервера
httpd = HTTPServer(('localhost', 8080), SimpleHTTPRequestHandler)
print('server is running')
httpd.serve_forever()