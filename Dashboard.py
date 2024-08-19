import Aggregator


def dashboard_for_hub(message: Aggregator.tb_types.Message, text: str):
    markup = Aggregator.tb_types.ReplyKeyboardMarkup(resize_keyboard=True)
    open_shift = Aggregator.tb_types.KeyboardButton(text='Відкрити зміну')
    close_shift = Aggregator.tb_types.KeyboardButton(text='Закрити зміну')
    send_message = Aggregator.tb_types.KeyboardButton(text='Відправити повідомлення')

    markup.add(open_shift, close_shift, send_message)

    Aggregator.bot.send_message(message.from_user.id, text, reply_markup=markup, parse_mode='HTML')


def dashboard_for_users(message: Aggregator.tb_types.Message, text: str):
    markup = Aggregator.tb_types.ReplyKeyboardMarkup(resize_keyboard=True)
    open_shift = Aggregator.tb_types.KeyboardButton(text='Відкрити зміну')
    close_shift = Aggregator.tb_types.KeyboardButton(text='Закрити зміну')
    send_message = Aggregator.tb_types.KeyboardButton(text='Відправити повідомлення')

    match Aggregator.users_database[message.from_user.id].shift_status:
        case False:
            markup.add(open_shift, send_message)
        case True:
            markup.add(close_shift, send_message)

    Aggregator.bot.send_message(message.from_user.id, text, reply_markup=markup, parse_mode='HTML')


def dashboard_for_admin(message: Aggregator.tb_types.Message, text: str):
    markup = Aggregator.tb_types.ReplyKeyboardMarkup(resize_keyboard=True)
    open_shift = Aggregator.tb_types.KeyboardButton(text='Відкрити зміну')
    close_shift = Aggregator.tb_types.KeyboardButton(text='Закрити зміну')
    send_message = Aggregator.tb_types.KeyboardButton(text='Відправити повідомлення')
    change_paths = Aggregator.tb_types.KeyboardButton(text='Змінити шлях')

    match Aggregator.users_database[message.from_user.id].shift_status:
        case False:
            markup.add(open_shift, send_message, change_paths)
        case True:
            markup.add(close_shift, send_message, change_paths)

    Aggregator.bot.send_message(message.from_user.id, text, reply_markup=markup, parse_mode='HTML')


def dashboard_for_tex(message: Aggregator.tb_types.Message, text: str):
    markup = Aggregator.tb_types.ReplyKeyboardMarkup(resize_keyboard=True)
    open_shift = Aggregator.tb_types.KeyboardButton(text='Відкрити зміну')
    close_shift = Aggregator.tb_types.KeyboardButton(text='Закрити зміну')
    send_message = Aggregator.tb_types.KeyboardButton(text='Відправити повідомлення')
    change_paths = Aggregator.tb_types.KeyboardButton(text='Змінити шлях')

    match Aggregator.users_database[message.from_user.id].shift_status:
        case False:
            markup.add(open_shift, send_message, change_paths)
        case True:
            markup.add(close_shift, send_message, change_paths)

    Aggregator.bot.send_message(message.from_user.id, text, reply_markup=markup, parse_mode='HTML')
