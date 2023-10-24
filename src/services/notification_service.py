from tqdm import tqdm


class NotificationService:
    def __init__(self, telegram_client):
        self.progress_bar = None
        self.telegram_client = telegram_client

    def set_bar(self, collection: []):
        self.progress_bar = tqdm(bar_format="|{bar}|{n}/{total}", colour="white", total=len(collection))

    def iterate(self):
        self.progress_bar.update()

    def finish(self):
        self.progress_bar.close()
