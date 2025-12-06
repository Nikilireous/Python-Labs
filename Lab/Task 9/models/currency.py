class Currency:
    def __init__(self, valute_id: str, char_code: str, num_code: str, name: str, value: float, nominal: int):
        self.__valute_id: str = valute_id
        self.__num_code: str = num_code
        self.__char_code: str = char_code
        self.__name: str = name
        self.__value: float = value
        self.__nominal: int  = nominal

    @property
    def valute_id(self):
        return self.__valute_id

    @property
    def num_code(self):
        return self.__num_code

    @num_code.setter
    def num_code(self, num_code: str):
        if type(num_code) is str:
            self.__num_code = num_code
        else:
            raise ValueError('Ошибка при задании цифрового кода валюты')

    @property
    def char_code(self):
        return self.__char_code

    @char_code.setter
    def char_code(self, char_code: str):
        if type(char_code) is str and len(char_code) == 3:
            self.__char_code = char_code
        else:
            raise ValueError('Ошибка при задании символьного кода валюты. Код валюты должен состоять только из 3 символов')

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name: str):
        if type(name) is str:
            self.__name= name
        else:
            raise ValueError('Ошибка при задании названия валюты')

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value: float):
        if type(value) is float and value > 0:
            self.__value = value
        else:
            raise ValueError('Ошибка при задании курса валюты. Курс валюты должен быть положительным числом')

    @property
    def nominal(self):
        return self.__nominal

    @nominal.setter
    def nominal(self, nominal: int):
        if type(nominal) is int:
            self.__nominal = nominal
        else:
            raise ValueError('Ошибка при задании номинала валюты')