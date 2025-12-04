# Модель автора приложения
class Author:
    def __init__(self, name: str, group: str, info: str):
        self.__name: str = name
        self.__group: str = group
        self.__info: str = info

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name: str):
        if type(name) is str and len(name) >= 2:
            self.__name = name
        else:
            raise ValueError('Ошибка при задании имени автора')

    @property
    def group(self):
        return self.__group

    @group.setter
    def group(self, group: str):
        if type(group) is str and len(group) > 5:
            self.__group = group
        else:
            raise ValueError('Ошибка при задании группы автора')

    @property
    def info(self):
        return self.__info

    @info.setter
    def info(self, info: str):
        if type(info) is str:
            self.__info = info
        else:
            raise ValueError('Ошибка при задании информации автора')
