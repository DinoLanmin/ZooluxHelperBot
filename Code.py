import Aggregator


class Code:

    def __init__(self, code: int, type_code: str):
        self.__code = code
        self.__type_code = type_code

    def __str__(self):
        return str(self.__code)

    def __repr__(self):
        return self.__code

    def __eq__(self, other):
        if isinstance(other, Code):
            return self.__code == other.__code
        elif isinstance(other, (str, int)):
            return str(self.__code) == str(other)
        return False

    def get_code(self):
        return self.__code

    def get_code_type(self):
        '''
        :return: User or Hub
        '''
        return self.__type_code


def download_codes():
    Aggregator.logging('The codes is loading.')
    database = Aggregator.sheet_secret_code.get_all_records()

    if len(database) == 0:
        Aggregator.logging('Database is empty!')
        return

    for data in database:
        code_data = Code(data.get('CODE'), data.get('TYPE'))
        Aggregator.code_database.append(code_data)

        Aggregator.logging('Database loaded!')
