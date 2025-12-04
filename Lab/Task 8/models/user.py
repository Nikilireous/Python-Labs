from bcrypt import hashpw, gensalt


# Модель информации пользователя
class User:
    def __init__(self, user_id: int, name: str, password: str):
        self.__user_id: int = user_id
        self.__name: str = name
        self.__password: str = str(hashpw(bytes(password, 'UTF8'), gensalt()), 'UTF8')

    @property
    def user_id(self):
        return self.__user_id

    @user_id.setter
    def user_id(self, user_id):
        if type(user_id) is int:
            self.__user_id = user_id
        else:
            raise ValueError('Ошибка при задании id пользователя')

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        if type(name) is str:
            self.__name = name
        else:
            raise ValueError('Ошибка при задании имени пользователя')

    @property
    def password(self):
        return self.__password

    @password.setter
    def password(self, password):
        if type(password) is str:
            self.__password = str(hashpw(bytes(password, 'UTF8'), gensalt()), 'UTF8')
        else:
            raise ValueError('Ошибка при задании пароля')
