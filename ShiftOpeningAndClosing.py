import Aggregator

# Инициализация глобальных переменных для очереди
name_of_users = {}
users_id = {}


def open_shift(message: Aggregator.tb_types.Message):
    user_id = message.from_user.id
    user = Aggregator.users_database[user_id]
    user_type = user.get_type()

    Aggregator.time.sleep(0.3)
    if user_type == "HUB":
        Aggregator.bot.send_message(message.chat.id,
                                    text="<strong>Нагадування</strong>Не забувайте звіряти номери терміналій, та Фопа.",
                                    parse_mode='HTML')

        Aggregator.time.sleep(0.3)
        Aggregator.bot.send_message(message.chat.id,
                                    text="<strong>Відкриття зміни, шаг 1 з 3</strong> "
                                         "Введіть ім'я людини яка відкриває зміну "
                                         "(не забувайте про пробіл між іменем, приклад: "
                                         "Джон_Сміт( _ = пробіл))",
                                    parse_mode='HTML')

        Aggregator.bot.register_next_step_handler(message, handle_hub_name_step, user)
    else:
        Aggregator.bot.send_message(message.chat.id,
                                    text="Введіть номер каси (цифра):")
        Aggregator.bot.register_next_step_handler(message, handle_cash_number, user)


def handle_hub_name_step(message: Aggregator.tb_types.Message, user):
    name_of_user = message.text.strip()

    if not name_of_user:
        Aggregator.time.sleep(0.3)
        Aggregator.bot.send_message(message.chat.id, "Введіть корректне ім'я.")
        Aggregator.bot.register_next_step_handler(message, handle_hub_name_step, user)
        return

    # Сохраняем имя пользователя в объекте Hub
    user.set_current_user(name_of_user)

    Aggregator.time.sleep(0.3)
    Aggregator.bot.send_message(message.chat.id,
                                text="<strong>Відкриття зміни, шаг 2 з 3</strong> Вкажіть вашу касу (цифрой 1, чи 2):",
                                parse_mode='HTML')

    Aggregator.bot.register_next_step_handler(message, handle_hub_cash_number, user)


def handle_hub_cash_number(message: Aggregator.tb_types.Message, user):
    cash_number = message.text.strip()

    if not cash_number.isdigit():
        Aggregator.time.sleep(0.3)
        Aggregator.bot.send_message(message.chat.id, "Введіть корректний номер каси.")
        Aggregator.bot.register_next_step_handler(message, handle_hub_cash_number, user)
        return

    # Добавляем или обновляем номер кассы для текущего пользователя в классе Hub
    user.set_cash_place(int(cash_number))

    Aggregator.time.sleep(0.3)
    Aggregator.bot.send_message(message.chat.id,
                                text="Касса успішно вибрана!")

    # Теперь можно продолжить работу с фотографиями
    Aggregator.bot.send_message(message.chat.id, "Сколько изображений вы хотите загрузить?")
    Aggregator.bot.register_next_step_handler(message, ask_for_images_count, user)


def handle_cash_number(message: Aggregator.tb_types.Message, user):
    cash_number = message.text.strip()

    if not cash_number.isdigit():
        Aggregator.time.sleep(0.3)
        Aggregator.bot.send_message(message.chat.id, "Введіть корректний номер каси.")
        Aggregator.bot.register_next_step_handler(message, handle_cash_number, user)
        return

    # Обновляем номер кассы для обычного пользователя
    user.set_cash_place(int(cash_number))

    Aggregator.time.sleep(0.3)
    Aggregator.bot.send_message(message.chat.id,
                                text="Касса успішно вибрана!")

    # Теперь можно продолжить работу с фотографиями
    Aggregator.bot.send_message(message.chat.id, "Сколько изображений вы хотите загрузить?")
    Aggregator.bot.register_next_step_handler(message, ask_for_images_count, user)


def ask_for_images_count(message: Aggregator.tb_types.Message, user):
    try:
        images_count = int(message.text.strip())
        if images_count <= 0:
            raise ValueError("Количество изображений должно быть положительным числом.")
        Aggregator.bot.send_message(message.chat.id, f"Хорошо, теперь отправьте {images_count} изображений по одному.")
        Aggregator.bot.register_next_step_handler(message, handle_each_image, user, images_count, 1)
    except ValueError as e:
        Aggregator.bot.send_message(message.chat.id, f"Ошибка: {str(e)}. Попробуйте еще раз.")
        Aggregator.bot.register_next_step_handler(message, ask_for_images_count, user)


def handle_each_image(message: Aggregator.tb_types.Message, user, total_images, current_image):
    if not message.photo:
        Aggregator.bot.send_message(message.chat.id, "Пожалуйста, отправьте изображение.")
        Aggregator.bot.register_next_step_handler(message, handle_each_image, user, total_images, current_image)
        return

    # Обрабатываем загруженное изображение
    photo = message.photo[-1]  # Выбираем самое большое изображение
    file_info = Aggregator.bot.get_file(photo.file_id)
    file_name = f"{user.first_name}_{user.last_name}_{Aggregator.get_current_time()}_{file_info.file_id}.jpg"
    safe_file_name = file_name.replace(":", "-")

    with Aggregator.tempfile.TemporaryDirectory() as tmpdirname:
        file_path = Aggregator.os.path.join(tmpdirname, safe_file_name)

        # Скачиваем файл
        downloaded_file = Aggregator.bot.download_file(file_info.file_path)
        with open(file_path, 'wb') as new_file:
            new_file.write(downloaded_file)

        # Загрузка файла в Google Drive
        folder_id = Aggregator.ID_OF_GOOGLE_DRIVER_FOLDER[0]
        try:
            Aggregator.upload_photo(file_path, safe_file_name, folder_id)
        except Exception as e:
            Aggregator.bot.send_message(message.chat.id, f"Ошибка при загрузке файла: {str(e)}")
            return

    if current_image < total_images:
        Aggregator.bot.send_message(message.chat.id, f"Изображение {current_image} загружено. Отправьте следующее.")
        Aggregator.bot.register_next_step_handler(message, handle_each_image, user, total_images, current_image + 1)
    else:
        Aggregator.bot.send_message(message.chat.id, "Все изображения были успешно загружены!")
        # Переход к следующему шагу после загрузки всех изображений
        ask_for_cash_balance(message, user)


def ask_for_cash_balance(message: Aggregator.tb_types.Message, user):
    Aggregator.bot.send_message(message.chat.id, "Введите сумму кассы:")
    Aggregator.bot.register_next_step_handler(message, handle_cash_balance, user)


def handle_cash_balance(message: Aggregator.tb_types.Message, user):
    cash_balance = message.text.strip()

    if not cash_balance.isdigit():
        Aggregator.bot.send_message(message.chat.id, "Введите корректную сумму кассы.")
        Aggregator.bot.register_next_step_handler(message, handle_cash_balance, user)
        return

    # Сохраняем баланс кассы
    cash_balance = float(cash_balance)

    Aggregator.bot.send_message(message.chat.id, "Введите ваш X - отчет:")
    Aggregator.bot.register_next_step_handler(message, handle_x_report, user, cash_balance)


def handle_x_report(message: Aggregator.tb_types.Message, user, cash_balance):
    x_report = message.text.strip()

    if not x_report.isdigit():
        Aggregator.bot.send_message(message.chat.id, "Введите корректный X-отчет.")
        Aggregator.bot.register_next_step_handler(message, handle_x_report, user, cash_balance)
        return

    x_report = float(x_report)

    Aggregator.bot.send_message(message.chat.id, "Введите ваш развернутый отчет:")
    Aggregator.bot.register_next_step_handler(message, handle_extended_report, user, cash_balance, x_report)


def handle_extended_report(message: Aggregator.tb_types.Message, user, cash_balance, x_report):
    extended_report = message.text.strip()

    if not extended_report.isdigit():
        Aggregator.bot.send_message(message.chat.id, "Введите корректный развернутый отчет.")
        Aggregator.bot.register_next_step_handler(message, handle_extended_report, user, cash_balance, x_report)
        return

    extended_report = float(extended_report)

    # Записываем данные
    Aggregator.write_data(
        name=user.first_name,
        number_of_case=user.get_cash_place() if user.get_type() != "HUB" else user.cash_places[user.get_current_user()],
        x_z_report=x_report,
        cash=cash_balance,
        extended_report=extended_report
    )

    Aggregator.bot.send_message(message.chat.id, "Смена успешно открыта!")

    from Core import brancher
    Aggregator.bot.register_next_step_handler(message, brancher)

