import Aggregator

BOT_INITIALIZATION_STATUS = False


def initialising():
    Aggregator.download_database()

    Aggregator.download_codes()

    Aggregator.bot_status = True


def password_security(message: Aggregator.tb_types.Message):
    def check_password(message: Aggregator.tb_types.Message):

        for code in Aggregator.code_database:
            print(f'Сравниваем {message.text} с {code}')

            if message.text == code:

                Aggregator.bot.send_message(message.chat.id,
                                            text='<strong>Регістрація</strong> Ваш захисний пароль, успішно, підтверджено!',
                                            parse_mode='HTML')

                Aggregator.registration_enter(code, message)

            elif message.text != code:

                Aggregator.bot.send_message(message.chat.id,
                                            text='<strong>Регістрація</strong> Ваш захисний код не співпадає, вибачте, '
                                                 'вам відмовлено у регістрації, будь ласка зверніться до '
                                                 'вашого системного адміністратора',
                                            parse_mode='HTML')

                return

    with Aggregator.locker:
        Aggregator.bot.send_message(message.chat.id,
                                    text='<strong>Регістрація</strong>\nНадішліть код для реєстрації:',
                                    parse_mode='HTML')
        Aggregator.bot.register_next_step_handler(message, check_password)


def brancher(message: Aggregator.tb_types.Message):
    match message.text:
        case 'Відкрити зміну':
            Aggregator.open_shift(message)
        case _:
            Aggregator.bot.send_message(message.chat.id,
                                        text='<strong>Помилка</strong>\nВаша команда не розпізнана.',
                                        parse_mode='HTML')

            Aggregator.bot.register_next_step_handler(message, brancher)


@Aggregator.bot.message_handler(['start'])
def start(message: Aggregator.tb_types.Message):
    if Aggregator.bot_status is False:
        initialising()

    Aggregator.bot.send_message(message.chat.id,
                                text='<strong>Вітання</strong>\nВітаємо вас у боті ZooluxHelperBot',
                                parse_mode='HTML')

    if message.from_user.id not in Aggregator.users_database:
        Aggregator.numeral += 1

        Aggregator.time.sleep(0.5)

        Aggregator.threading.Thread(target=password_security, name=f'Waiting for password {Aggregator.numeral}',
                                    args=(message,)).start()

    elif message.from_user.id in Aggregator.users_database:
        print(Aggregator.users_database[message.from_user.id].get_accesses_level())
        Aggregator.time.sleep(0.5)
        match Aggregator.users_database[message.from_user.id].get_accesses_level():
            case 'HUB':
                Aggregator.dashboard_for_hub(message, 'Хаб авторизовано')
            case 'USER':
                Aggregator.dashboard_for_users(message, 'Юзера авторизовано')
            case 'ADMIN':
                Aggregator.dashboard_for_admin(message, 'Адміна авторизовано')
            case 'TEX':
                Aggregator.dashboard_for_tex(message, 'Техніка авторизовано')

    Aggregator.bot.register_next_step_handler(message, brancher)


Aggregator.bot.polling(none_stop=True)
