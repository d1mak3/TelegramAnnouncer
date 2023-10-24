from telethon import TelegramClient

from src.services.auth_service import AuthService
from src.services.chat_service import ChatService
from src.services.message_service import MessageService
from src.services.notification_service import NotificationService
from src.services.user_service import UserService
from src.services.database_service import DatabaseService


class TelethonClient(TelegramClient):
    def __init__(self, session, api_id, api_hash, database_provider):
        super().__init__(session, api_id, api_hash)
        self.chat = ChatService(self)
        self.message = MessageService(self)
        self.user = UserService(self)
        self.auth = AuthService(self)
        self.database = DatabaseService(self, database_provider)
        self.notification = NotificationService(self)

    def stop(self):
        super().disconnect()
