import os
import yaml

from src.clients.telethon_client import TelethonClient
from src.core.menu.console_menu import ConsoleMenu
from src.core.enums.message_input_type import MessageInputType
from src.database_providers.google_sheets_provider import GoogleSheetsProvider


class ConsoleRunner:
    def __init__(self):
        self.menu = ConsoleMenu()
        self.messages_path = "./messages/"
        self.telegram_config_path = "./env/telegram_config.yml"
        self.message_config_path = "./env/message_config.yml"
        self.database_config_path = "./env/database_config.yml"

    async def run(self):
        # configure telegram
        telegram_config = self.get_config(self.telegram_config_path, self.menu.should_telegram_be_configured,
                                          self.menu.get_telegram_configuration)

        phone = telegram_config["phone"]
        api_id = telegram_config["api_id"]
        api_hash = telegram_config["api_hash"]

        # configure database
        database_config = self.get_config(self.database_config_path, self.menu.should_database_be_configured,
                                          self.menu.get_database_configuration)
        database_credentials_path = database_config["credentials_path"]
        database_link = database_config["link"]
        database_sheet_title = database_config["sheet_title"]

        # configure message
        message_config = self.get_config(self.message_config_path, self.menu.should_message_be_configured,
                                         self.menu.get_message_configuration)

        receivers_per_iteration = message_config["receivers_per_iteration"]
        delay = message_config["delay"]

        # create client
        telethon_client = TelethonClient(phone, api_id, api_hash, GoogleSheetsProvider(database_credentials_path,
                                                                                       database_link))
        telethon_client.database.set_sheet(database_sheet_title)

        # login + 2FA
        await telethon_client.auth.login(phone)

        # check if users are already set
        parsed = self.menu.should_users_be_parsed()
        if parsed:
            # get all public chats
            chats = list(self.delete_repeating_chats(await telethon_client.chat.get_all_groups() +
                                                     await telethon_client.chat.get_all_channels()))

            # get chats to announce and get users from them
            selected_chats = self.menu.select_chats(chats)
            users = await telethon_client.user.get_users_from_chats(selected_chats)
        else:
            users = telethon_client.database.get()

        # save users if needed
        if parsed and self.menu.should_users_be_saved():
            telethon_client.database.save(list(telethon_client.user.convert_users_to_database(users)))

        # get message
        message_input_type = self.menu.select_message_input_type()
        if message_input_type == MessageInputType.RUNTIME:
            message = self.menu.get_message()
        else:
            message_filenames = list(self.get_message_filenames())
            selected_filenames = self.menu.select_message_filenames(message_filenames)
            message = "\n\n".join(self.get_messages(selected_filenames))

        # begin announce
        prepared_users = await telethon_client.user.prepare_users(users)
        await telethon_client.message.send_message(message, prepared_users, receivers_per_iteration, delay)

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
