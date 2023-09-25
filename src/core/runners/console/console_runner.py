import os
import yaml

from src.clients.telethon_client import TelethonClient
from src.core.menu.console_menu import ConsoleMenu
from src.core.enums.message_input_type import MessageInputType


class ConsoleRunner:
    def __init__(self):
        self.menu = ConsoleMenu()
        self.messages_path = "../messages/"
        self.telegram_config_path = "../env/debug_tg_config.yml"
        self.message_config_path = "../env/debug_message_config.yml"

    async def run(self):
        # configure telegram
        telegram_config = self.get_config(self.telegram_config_path, self.menu.should_telegram_be_configured,
                                          self.menu.get_telegram_configuration)
        phone = telegram_config["phone"]
        api_id = telegram_config["api_id"]
        api_hash = telegram_config["api_hash"]
        telethon_client = TelethonClient(phone, api_id, api_hash)

        # configure message
        message_config = self.get_config(self.message_config_path, self.menu.should_message_be_configured,
                                         self.menu.get_message_configuration)
        receivers_per_iteration = message_config["receivers_per_iteration"]
        delay = message_config["delay"]

        # login + 2FA
        await telethon_client.auth.login(phone)

        # get all public chats
        chats = list(self.delete_repeating_chats(await telethon_client.chat.get_all_groups() +
                                                 await telethon_client.chat.get_all_channels()))

        # get chats to announce and get users from them
        selected_chats = self.menu.select_chats(chats)
        users = await telethon_client.user.get_users_from_chats(selected_chats)

        # get message
        message_input_type = self.menu.select_message_input_type()
        if message_input_type == MessageInputType.RUNTIME:
            message = self.menu.get_message()
        else:
            message_filenames = list(self.get_message_filenames())
            selected_filenames = self.menu.select_message_filenames(message_filenames)
            message = "\n\n".join(self.get_messages(selected_filenames))

        # begin announce
        await telethon_client.message.send_message(message, users, receivers_per_iteration, delay)

        # notify we are done
        self.menu.print_done()

    @staticmethod
    def delete_repeating_chats(chats):
        cleaned_chats_names = []

        for chat in chats:
            if chat.name not in cleaned_chats_names:
                cleaned_chats_names.append(chat.name)
                yield chat

    def get_message_filenames(self):
        for file in os.listdir(self.messages_path):
            path = os.path.join(self.messages_path, file)
            if os.path.isfile(path):
                yield path.removeprefix("../messages/")

    def get_messages(self, paths):
        for path in paths:
            with open(self.messages_path + path, "r") as file:
                yield file.read()

    @staticmethod
    def get_config(config_path, should_be_configured, get_configuration_func):
        if not os.path.exists(config_path) or should_be_configured():
            with open(config_path, "w") as config:
                config.write(yaml.dump(get_configuration_func()))

        try:
            with open(config_path, "r") as config:
                config_string = config.read()
                if config_string == "":
                    os.remove(config_path)
                    raise IOError("Ошибка: Файл конфигурации пуст. Перезапустите приложение")
                return yaml.safe_load(config_string)
        except yaml.YAMLError:
            os.remove(config_path)
            raise IOError("Ошибка: Файл конфигурации испорчен. Перезапустите приложение")
