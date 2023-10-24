from src.core.enums.message_input_type import MessageInputType
from tqdm import tqdm


class ConsoleMenu:
    def __init__(self):
        self.yes_no_choice = {"д": True, "н": False, "y": True, "n": False}
        self.progress_bar = None

    @staticmethod
    def select_chats(chats: []):
        print("Выберите группы для рассылки (в формате: 1, 3, 5):")
        chats_len = len(chats)

        for i in range(chats_len):
            print("{}. '{}'".format(i + 1, chats[i].name))

        options = input("Введите номера групп: ").replace(" ", "").split(",")

        for option in options:
            int_option = int(option) - 1
            if int_option >= chats_len or int_option < 0:
                raise AttributeError("Ошибка: Вы должны ввести число от {} до {}".format(0, chats_len - 1))
            yield chats[int_option]

    @staticmethod
    def select_message_input_type():
        print("Выберите способ задания сообщения:\n"
              "1. Через консоль\n"
              "2. Через файл")

        option = int(input("Введите номер: "))

        if option > 2 or option < 1:
            raise AttributeError("Ошибка: Вы должны ввести число от {} до {}".format(1, 2))

        if option == 1:
            return MessageInputType.RUNTIME
        else:
            return MessageInputType.FILE

    def should_message_be_configured(self):
        option = input("Нужно ли конфигурировать сообщение?(Д/н): ")
        return self.choose_yes_or_no(option)

    @staticmethod
    def get_message_configuration():
        receivers_per_iteration_option = int(input("Введите количество пользователей после которых необходимо делать "
                                                   "задержку: "))
        delay_option = int(input("Введите длительность задержки между отправкой (в секундах): "))
        return {"delay": delay_option, "receivers_per_iteration": receivers_per_iteration_option}

    @staticmethod
    def get_message():
        return input("Введите сообщение: ")

    @staticmethod
    def select_message_filenames(message_filenames):
        print("Выберите файлы с сообщениями: ")
        for i in range(len(message_filenames)):
            print("{}. {}".format(i + 1, message_filenames[i]))

        option = input("Номер файла или 'все': ")

        if option.lower() == "все":
            return message_filenames

        try:
            int_option = int(option) - 1
            return [message_filenames[int_option]]
        except ValueError or IndexError:
            raise AttributeError("Ошибка: Вы должны ввести число от {} до {} или 'все'"
                                 .format(0, len(message_filenames) - 1))

    @staticmethod
    def print_done():
        print("Сообщение отправлено")

    def should_telegram_be_configured(self):
        option = input("Нужно ли конфигурировать телеграм подключение?(Д/н): ")
        return self.choose_yes_or_no(option)

    @staticmethod
    def get_telegram_configuration():
        print("Введите данные с https://my.telegram.org")
        return {"phone": input("Введите номер телефона: "), "api_id": input("Введите api_id: "),
                "api_hash": input("Введите api_hash: ")}

    def should_users_be_saved(self):
        option = input("Нужно ли сохранить пользователей?(Д/н): ")
        return self.choose_yes_or_no(option)

    def should_database_be_configured(self):
        option = input("Нужно ли конфигурировать базу данных?(Д/н): ")
        return self.choose_yes_or_no(option)

    @staticmethod
    def get_database_configuration():
        return {"credentials_path": input("Введите путь до файла, полученного по гайду с "
                "https://dvsemenov.ru/google-tablicy-i-python-podrobnoe-rukovodstvo-s-primerami: "),
                "link": input("Введите ссылку на таблицу: "),
                "sheet_title": input("Введите имя листа: ")}

    def should_users_be_parsed(self):
        option = input("Нужно ли собирать данные из телеграма?(Д/н): ")
        return self.choose_yes_or_no(option)

    @staticmethod
    def print_notifications(word: str):
        print(word, end="")

    def choose_yes_or_no(self, option):
        try:
            return self.yes_no_choice[option.lower()]
        except KeyError:
            raise AttributeError("Ошибка: Вы должны ввести букву 'д' или 'н'")
