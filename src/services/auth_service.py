class AuthService:
    def __init__(self, telegram_client):
        self.telegram_client = telegram_client

    async def login(self, phone):
        await self.telegram_client.connect()
        if not await self.telegram_client.is_user_authorized():
            await self.telegram_client.send_code_request(phone)
            await self.telegram_client.sign_in(phone, input("Введите код: "))
