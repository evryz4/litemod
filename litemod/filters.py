from aiogram import Bot
from aiogram.filters import BaseFilter
from aiogram.types import Message

bot = Bot
def init(_bot: Bot):
    global bot
    bot = _bot


class AdminFilter(BaseFilter):
    def __init__(self, is_admin: bool = True):
        self.is_admin = is_admin

    async def __call__(self, msg: Message) -> bool:
        member = await bot.get_chat_member(chat_id=msg.chat.id,\
                                                user_id=msg.from_user.id)

        return self.is_admin == (member.status in ['administrator', 'creator'])
