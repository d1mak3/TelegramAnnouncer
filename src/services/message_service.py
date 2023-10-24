import asyncio


class MessageService:
    def __init__(self, telegram_client):
        self.telegram_client = telegram_client

    @staticmethod
    def get_message_from_file(path=".\\messages\\test_message.txt"):
        message = open(path).read()
        return message

    async def send_message(self, message, receivers, receivers_per_iteration, delay, progress_notification=None):
        receivers_handled = 1
        receivers_count = len(list(receivers))
        for receiver in receivers:
            await self.telegram_client.send_message(receiver, message)

            if progress_notification is not None:
                progress_notification()

            if receivers_handled % receivers_per_iteration == 0 and 1 < receivers_count != receivers_handled:
                await asyncio.sleep(delay)

            receivers_handled += 1


