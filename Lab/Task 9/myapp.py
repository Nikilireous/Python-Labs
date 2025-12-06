from jinja2 import Environment, PackageLoader, select_autoescape
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs, ParseResult
from models import App, Author, Currency, User, UserCurrency
from controllers import AppCRUD
from requests import exceptions


# Заглушки с тестовой информацией
app_controller = AppCRUD('data/data.db')


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
        global app_controller

        # Парсинг пути URL
        parsed_path = urlparse(self.path)
        path = parsed_path.path

        routes = {
            '/': self.home_page,
            '/author': self.author_page,
            '/currencies': self.currencies_page,
            '/currencies/show':self.show_currencies,
            '/currencies/update': self.update_currencies,
            '/users': self.users_page,
            '/user': self.user_page,
            '/user/delete': self.delete_user_currency
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
            all_currencies = app_controller._read_currencies()

            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()

            template = env.get_template("currencies.html")
            result = template.render(myapp=main_app.name,
                                     currencies=all_currencies)

            self.wfile.write(bytes(result, "utf-8"))
        except exceptions.RequestException:
            self.page_500()

    def show_currencies(self):
        try:
            try:
                currency_id = (parse_qs(self.url_path.query)['id'])[0]
                app_controller._read_currencies(currency_id=currency_id, command_line=True)
            except KeyError:
                app_controller._read_currencies(command_line=True)
            self.request_page()
        except exceptions.RequestException:
            self.page_500()

    def update_currencies(self):
        try:
            try:
                currency_id = (parse_qs(self.url_path.query)['id'])[0]
                app_controller._update_currencies(currency_id)
            except KeyError:
                app_controller._update_currencies()

            self.request_page()
        except exceptions.RequestException:
            self.page_500()

    def users_page(self):
        try:
            users = app_controller._read_users()
            print(users)

            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()

            template = env.get_template("users.html")
            result = template.render(myapp=main_app.name,
                                     users=users)

            self.wfile.write(bytes(result, "utf-8"))
        except Exception:
            self.page_500()

    def user_page(self):
        try:
            cur_user_id = int((parse_qs(self.url_path.query)['id'])[0])
            cur_user = app_controller._read_users(cur_user_id)[0]
            cur_currencies = app_controller._read_user_currency(cur_user_id)

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

    def delete_user_currency(self):
        try:
            user_id = int((parse_qs(self.url_path.query)['user'])[0])
            currency_id = (parse_qs(self.url_path.query)['currency'])[0]

            app_controller._delete_user_currency(user_id, currency_id)

            self.request_page()

        except IndexError:
            self.page_404()
        except Exception:
            self.page_500()


    def request_page(self):
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.end_headers()

        template = env.get_template("request_success.html")
        result = template.render(myapp=main_app.name)

        self.wfile.write(bytes(result, "utf-8"))

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