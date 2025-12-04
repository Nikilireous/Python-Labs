# Модель-связка между пользователем и его отслеживаемыми валютами
class UserCurrency:
    def __init__(self, current_id, user_id, currency_id):
        self.__current_id: int = current_id
        self.__user_id: int = user_id
        self.__currency_id : int = currency_id

    @property
    def current_id(self):
        return self.__current_id

    @current_id.setter
    def current_id(self, current_id):
        if type(current_id) is int:
            self.__current_id = current_id
        else:
            raise ValueError('Ошибка при задании id связки')

    @property
    def user_id(self):
        return self.__user_id

    @user_id.setter
    def user_id(self, user_id):
        if type(user_id) is str:
            self.__user_id = user_id
        else:
            raise ValueError('Ошибка при задании id пользователя')

    @property
    def currency_id(self):
        return self.__currency_id

    @currency_id.setter
    def currency_id(self, currency_id: int):
        if type(currency_id) is int:
            self.__currency_id = currency_id
        else:
            raise ValueError('Ошибка при задании id валюты')