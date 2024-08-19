import Aggregator

NAME_TABLE_TO_SAVE_USERS = ["Bot_users_zoolux"]
NAME_TABLE_TO_ACCEPT_CODES = ["BOT_SECRET_CODE"]
NAME_TABLE_TO_SAVE_LOG = ["Bot_log_zoolux"]
NAME_TABLE_TO_DATABASE = ['1MprrYzaGoyX4q0JvzoJ6ZrCcxDevV3Wo-Lk3XziQngs']
ID_OF_GOOGLE_DRIVER_FOLDER = ["1fXqHmrf0VR9YyX54anJorSZVr-Pwn4Jv"]


def change_paths(paths_name: str, new_paths):
    Aggregator.logging(f'Change paths of {paths_name}')

    match paths_name:
        case 'NAME_TABLE_TO_SAVE_USERS':
            NAME_TABLE_TO_SAVE_USERS.clear()
            NAME_TABLE_TO_SAVE_USERS.append(new_paths)
        case 'NAME_TABLE_TO_ACCEPT_CODES':
            NAME_TABLE_TO_ACCEPT_CODES.clear()
            NAME_TABLE_TO_ACCEPT_CODES.append(new_paths)
        case 'NAME_TABLE_TO_SAVE_LOG':
            NAME_TABLE_TO_SAVE_LOG.clear()
            NAME_TABLE_TO_SAVE_LOG.append(new_paths)
        case _:
            Aggregator.logging("The path doesn't exist")
            return
