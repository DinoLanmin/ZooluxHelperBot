import Aggregator

users_database = {}
numeral = 0
code_database = []

bot_status = False


class Member:

    def __init__(self, user_id: int, first_name: str, last_name: str, username: str, type_of_user: str,
                 accesses_level: str, real_name: str = None, ):
        self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.type_of_user = type_of_user
        self.__accesses_level = accesses_level
        self._real_name = real_name

        self.shift_status = False
        self._cash_place = None

    def set_cash_place(self, new_cash_place: int):
        self._cash_place = new_cash_place

    def get_cash_place(self):
        return self._cash_place

    def get_accesses_level(self):
        return self.__accesses_level

    def get_type(self):
        return self.type_of_user


class Hub:

    def __init__(self, user_id: int, first_name: str, last_name: str, username: str, type_of_system: str,
                 accesses_level: str):
        self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self._type_of_system = type_of_system
        self.__accesses_level = accesses_level

        self._name_of_current_user = None
        self.activ_users = []
        self.shift_status = []

    def get_type(self):
        return self._type_of_system

    def get_accesses_level(self):
        return self.__accesses_level

    def set_current_user(self, name: str):
        self._name_of_current_user = name

    def get_current_user(self):
        return self._name_of_current_user


def download_database():
    Aggregator.logging('The database is loading.')
    database = Aggregator.sheet_users.get_all_records()

    '''
    users = user = {'user_id': 000..., 'first_name': first_name, 'last_name':last_name,  'username':username, 
    'access_level': 'Level', 'real_name': real_name}

    hubs = hub = {'user_id: 000...., 'first_name': first_name, 'last_name': last_name, 'username': username,
    'accesses_level': 'Level'}
    '''

    if len(database) == 0:
        Aggregator.logging('Database is empty!')
        return

    for data in database:
        match data.get('type'):
            case 'USER':
                member = Member(data.get('user_id'), data.get('first_name'), data.get('last_name'),
                                data.get('username'), data.get('type'), data.get('accesses_level'),
                                data.get('real_name'))

                users_database.update({data.get('user_id'): member})

            case 'HUB':
                hub_data = Hub(data.get('user_id'), data.get('first_name'), data.get('last_name'),
                               data.get('username'), data.get('type'), data.get('accesses_level'))

                users_database.update({data.get('user_id'): hub_data})

    Aggregator.logging('Database loaded!')


def registration_enter(secret_code: Aggregator.Code, message: Aggregator.tb_types.Message):
    def registration_first(type_user: str, message: Aggregator.tb_types.Message):
        def registration_second(message: Aggregator.tb_types.Message):
            member = Member(message.from_user.id, message.from_user.first_name, message.from_user.last_name,
                            message.from_user.username, type_of_user='USER', accesses_level=access_level,
                            real_name=message.text)

            Aggregator.sheet_users.append_row(
                [message.from_user.id, message.from_user.first_name, message.from_user.last_name,
                 message.from_user.username, type_of_user, message.text, access_level, Aggregator.get_current_time()])

            users_database.update({message.chat.id: member})
            Aggregator.bot.send_message(message.chat.id,
                                        text='<strong>Регістрація</strong> Вітаємо, регістрація пройшла успішно.',
                                        parse_mode='HTML')

        access_level = 'USER'

        match type_user:
            case 'USER':

                Aggregator.bot.send_message(message.chat.id,
                                            "Будь ласка, напишіть ваше им'я та прізвище,"
                                            " через пробіл(приклад: Джон Сміт):")

                Aggregator.bot.register_next_step_handler(message, registration_second)

            case 'HUB':

                hub = Hub(message.from_user.id, message.from_user.first_name, message.from_user.last_name,
                          message.from_user.username, type_of_system='HUB', accesses_level=access_level)

                real_name = 'HUB'
                type_of_user = 'HUB'

                Aggregator.sheet_users.append_row(
                    [message.from_user.id, message.from_user.first_name, message.from_user.last_name,
                     message.from_user.username, type_of_user, real_name, access_level, Aggregator.get_current_time()])

                users_database.update({message.from_user.id: hub})
                Aggregator.bot.send_message(message.chat.id,
                                            text='<strong>Регістрація</strong> Вітаємо, Хаб успішно зареєстровано.',
                                            parse_mode='HTML')

    match secret_code.get_code_type():
        case 'USER':
            registration_first('USER', message)
        case 'HUB':
            registration_first('HUB', message)

    Aggregator.code_database.remove(secret_code)

    cell = Aggregator.sheet_secret_code.find(str(secret_code.get_code()))
    Aggregator.sheet_secret_code.delete_rows(cell.row)
    Aggregator.logging(f"Код {secret_code} був видалений.")


def write_data(name: str, number_of_case: int | float, x_z_report: int | float, cash: int | float,
               extended_report: int | float, terminal: int | float = None):

    new_row_data = [Aggregator.get_current_time(), name, number_of_case, x_z_report, cash, extended_report, terminal]
    Aggregator.sheet_save_data.append_row(new_row_data)
