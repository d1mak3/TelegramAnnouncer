from telethon import TelegramClient

from src.services.auth_service import AuthService
from src.services.chat_service import ChatService
from src.services.message_service import MessageService
from src.services.user_service import UserService


class TelethonClient(TelegramClient):
    def __init__(self, session, api_id, api_hash):
        super().__init__(session, api_id, api_hash)
        self.chat = ChatService(self)
        self.message = MessageService(self)
        self.user = UserService(self)
        self.auth = AuthService(self)
