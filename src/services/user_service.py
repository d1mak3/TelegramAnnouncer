import asyncio


class UserService:
    def __init__(self, telegram_client):
        self.telegram_client = telegram_client

    async def get_users_from_chats(self, chats: []):
        users = []

        for chat in chats:
            users += await self.get_converted_for_input_users(chat)

        return users

    async def get_converted_for_input_users(self, chat):
        converted_users = []
        async for user in self.telegram_client.iter_participants(chat):
            converted_user = await self.telegram_client.get_input_entity(user.id)
            if converted_user not in converted_users:
                converted_users.append(converted_user)

        return converted_users
