# Контроллер для работы с БД
import sqlite3
from .currencies_controller import get_all_currencies, update_currency
from models import Currency, User


class AppCRUD:
    def __init__(self, database_path: str):
        self.__database: str = database_path

        self.__con = sqlite3.connect(database_path)
        self.__cursor = self.__con.cursor()
        self.__create_tables()


    @staticmethod
    def __currency_normalizer(currencies: list | tuple) -> list[Currency]:
        return [Currency(valute_id=currency[0],
                         num_code=currency[1],
                         char_code=currency[2],
                         name=currency[3],
                         value=currency[4],
                         nominal=currency[5]) for currency in currencies]

    @staticmethod
    def __user_normalizer(users: list | tuple) -> list[User]:
        return [User(user_id=user[0],
                     name=user[1],
                     password=user[2]) for user in users]


    def __create_tables(self):
        self.__cursor.execute('''SELECT name FROM sqlite_master WHERE type='table' AND name="Currencies"''')
        if not self.__cursor.fetchone():
            self.__cursor.execute(
                '''CREATE TABLE Currencies (
                        ValuteId TEXT PRIMARY KEY
                                         NOT NULL
                                         UNIQUE,
                        NumCode  TEXT    UNIQUE
                                         NOT NULL,
                        CharCode TEXT    UNIQUE
                                         NOT NULL,
                        Name     TEXT    UNIQUE
                                         NOT NULL,
                        Value    NUMERIC NOT NULL,
                        Nominal  INTEGER NOT NULL
                    );'''
            )

            currencies: list[Currency] = get_all_currencies()
            __sqlquery = '''INSERT INTO Currencies(ValuteId, NumCode, CharCode, Name, Value, Nominal)
                            VALUES(?, ?, ?, ?, ?, ?)'''

            self.__cursor.executemany(__sqlquery, [(currency.valute_id,
                                                    currency.num_code,
                                                    currency.char_code,
                                                    currency.name,
                                                    currency.value,
                                                    currency.nominal) for currency in currencies])
            self.__con.commit()

        self.__cursor.execute(
            '''CREATE TABLE IF NOT EXISTS Users (
                    UserId   INTEGER PRIMARY KEY
                                     UNIQUE
                                     NOT NULL,
                    Name     TEXT    UNIQUE
                                     NOT NULL,
                    Password TEXT    NOT NULL
                );'''
        )

        self.__con.execute(
            '''CREATE TABLE IF NOT EXISTS UsersCurrency (
                    CurrentId  INTEGER PRIMARY KEY
                                       UNIQUE
                                       NOT NULL,
                    UserId     INTEGER REFERENCES users (UserId) 
                                       NOT NULL,
                    CurrencyId TEST REFERENCES currencies (ValuteId) 
                                       NOT NULL
                );'''
        )

        self.__con.commit()

    def _read_currencies(self, currency_id: str | None = None, command_line=False):
        if currency_id:
            cur = self.__cursor.execute(f'SELECT * FROM Currencies WHERE ValuteId == "{currency_id}"')
        else:
            cur = self.__cursor.execute("SELECT * FROM Currencies")

        currencies = cur.fetchall()
        if not command_line:
            currencies = self.__currency_normalizer(currencies)
            return currencies

        if not currencies:
            print('Валюты не существует')
        for _row in currencies:
            print(_row)
        return None

    def _update_currencies(self, currency_id: str | None = None):
        if currency_id:
            cur = self.__cursor.execute(f'SELECT * FROM Currencies WHERE ValuteId == "{currency_id}"')
        else:
            cur = self.__cursor.execute("SELECT * FROM Currencies")
        currencies = self.__currency_normalizer(cur.fetchall())

        updated_currencies = [update_currency(currency) for currency in currencies]

        for currency in updated_currencies:
            self.__cursor.execute(f'''UPDATE Currencies SET Value = {currency.value}, Nominal = {currency.nominal}
                                        WHERE ValuteId == "{currency.valute_id}"''')
        self.__con.commit()

    def _read_users(self, user_id: int | None = None):
        if user_id:
            cur = self.__cursor.execute(f"SELECT * FROM Users WHERE UserId == {user_id}")
        else:
            cur = self.__cursor.execute("SELECT * FROM Users")
        users = self.__user_normalizer(cur.fetchall())
        return users

    def _create_user_currency(self, user_id: int, currency_id: str):
        cur = self.__cursor.execute(f'SELECT UserId FROM Users')
        if user_id in [user[0] for user in cur.fetchall()]:
            cur = self.__cursor.execute(f'SELECT CurrencyId FROM UsersCurrency WHERE UserId == {user_id}')
            already_have = [currency[0] for currency in cur.fetchall()]

            if currency_id not in already_have:
                __sqlquery = "INSERT INTO UsersCurrency(UserId, CurrencyId) VALUES(?, ?)"
                self.__cursor.execute(__sqlquery, [user_id, currency_id])
                self.__con.commit()

                return 'Валюта добавлена'

            raise ValueError('Пользователь уже отслеживает эту валюту')
        raise ValueError('Такого пользователя не существует')

    def _read_user_currency(self, user_id: int):
        cur = self.__cursor.execute(f'SELECT UserId FROM Users')
        if user_id in [user[0] for user in cur.fetchall()]:
            cur = self.__cursor.execute(f'SELECT CurrencyId FROM UsersCurrency WHERE UserId == {user_id}')
            info = tuple(currency[0] for currency in cur.fetchall()) + tuple(' ')

            cur = self.__cursor.execute(f'SELECT * FROM Currencies WHERE ValuteId in {info}')
            currencies = self.__currency_normalizer(cur.fetchall())
            return currencies

        raise ValueError('Такого пользователя не существует')

    def _delete_user_currency(self, user_id: int, currency_id: str):
        cur = self.__cursor.execute(f'SELECT UserId FROM Users')
        if user_id in [user[0] for user in cur.fetchall()]:
            cur = self.__cursor.execute(f'SELECT CurrencyId FROM UsersCurrency WHERE UserId == {user_id}')
            already_have = [(currency[0]) for currency in cur.fetchall()]

            if currency_id in already_have:
                request = f"DELETE FROM UsersCurrency WHERE UserId = {user_id} AND CurrencyId = '{currency_id}'"
                self.__cursor.execute(request)
                self.__con.commit()

                return 'Валюта удалена'

            raise ValueError('Пользователь не отслеживает данную валюту')
        raise ValueError('Такого пользователя не существует')


# class ViewController:
#
#     def __init__(self, currency_rates):
#         pass
#         self.currency_name = currency_rates.values[0]
#         self.currency_date = currency_rates.values[1]
#         self.currency_value = currency_rates.values[2]
#
#     def __call__(self):
#         return f"{self.currency_name} - {self.currency_date} - {self.currency_value}"