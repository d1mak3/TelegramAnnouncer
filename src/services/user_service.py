import asyncio


class UserService:
    def __init__(self, telegram_client):
        self.telegram_client = telegram_client

    async def get_users_from_chats(self, chats: []):
        users = []

        for chat in chats:
            users += await self.telegram_client.get_participants(chat)

        return users

    async def prepare_users(self, users):
        prepared_users = []
        handled_ids = []
        for user in users:
            converted_user = await self.telegram_client.get_input_entity(user.id)
            if user.id not in handled_ids:
                handled_ids.append(user.id)
                prepared_users.append(converted_user)

        return prepared_users

    @staticmethod
    def convert_users_to_database(users):
        for user in users:
            if user.username is None:
                yield [user.first_name, user.id]
            else:
                yield [user.username, user.id]
