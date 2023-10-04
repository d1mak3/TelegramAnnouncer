from src.core.types.user import User


class DatabaseService:
    def __init__(self, telegram_client, database_provider):
        self.database = database_provider
        self.telegram_client = telegram_client

    def set_sheet(self, title):
        self.database.set_sheet(title)

    def save(self, data: [[]]):
        self.database.save(data)

    def get(self):
        data = self.database.get()
        return list(self.parse_data(data))

    @staticmethod
    def parse_data(data: [[]]):
        for d in data:
            yield User(d[0], d[1])
