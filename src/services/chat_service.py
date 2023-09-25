class ChatService:
    def __init__(self, telegram_client):
        self.tg_client = telegram_client

    async def get_all_groups(self):
        groups = []

        async for dialog in self.tg_client.iter_dialogs():
            if dialog.is_group and dialog not in groups:
                groups.append(dialog)

        return groups

    async def get_all_channels(self):
        channels = []

        async for dialog in self.tg_client.iter_dialogs():
            if dialog.is_channel and dialog not in channels:
                channels.append(dialog)

        return channels
