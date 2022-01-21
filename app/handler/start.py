from app.config import msg
from app.handler.general import TelegramMessageHandler, MessageMeta


class StartHandler(TelegramMessageHandler):
    def __init__(self):
        super().__init__()

    async def handle_(self, message: MessageMeta, *args):
        await message.original.answer(msg.START)
