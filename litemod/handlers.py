from datetime import datetime

from aiogram import Router, F, Bot
from aiogram.types import Message
from aiogram.filters import Command

router = Router()

bot = 0
def botinit(_bot: Bot):
    global bot
    bot = _bot

async def gettext(msg: Message, txt: str, msgtype: str = 'ok'):
    now = datetime.now()
    time = now.strftime("%H:%M:%S")

    return f'user: @{msg.from_user.username}\ntime: {time}\ntype: [{msgtype.upper()}]\ntext: "{txt}"'

@router.message(Command('start'))
async def start_handler(msg: Message):
    await msg.reply(await gettext(msg, 'Hi, It\'s opensource moderaton bot for telegram. Channel - @litemodnews'))
    
    if msg.chat.type not in ['group', 'supergroup']:
        await msg.reply(await gettext(msg, 'Add bot to the server!', 'warning'))
    else:
        await msg.reply(await gettext(msg, 'Write /help for see the command list', 'info'))


@router.message(Command('help'))
async def help_handler(msg: Message):
    await msg.reply(await gettext(msg, '/start - see the start text\n/help - see this menu\n/del reply/[quantity] delete replied message/last [quantity messages]'))


@router.message(Command('del'))
async def del_handler(msg: Message):
    if len(msg.text.split()) == 1:
        err = False
        try:
            await bot.delete_message(chat_id=msg.chat.id, \
                                     message_id=msg.reply_to_message.message_id)
        except:
            err = True

        if err:
            await msg.reply(await gettext(msg, 'Some err has occured. Try to be sure, that:\n1. Your message is reply to another message\n2. Bot has permissions for deleting messages', 'err'))
            try:
                await bot.delete_message(chat_id=msg.chat.id, \
                                             message_id=msg.message_id)
            except:
                pass
        else:
            try:
                await bot.delete_message(chat_id=msg.chat.id, \
                                         message_id=msg.message_id)
            except:
                pass
    else:
        for i in range(1, int(msg.text.split()[1])+1):
            err = False
            try:
                await bot.delete_message(chat_id=msg.chat.id, \
                                         message_id=msg.message_id-i)
            except:
                err = True
            
        if err:
            await msg.reply(await gettext(msg, 'Some err has occured. Try to be sure, that:\n1. Bot has permissions for deleting messages\n2. You havn\'t deleted any messages in this list', 'err'))
            try:
                await bot.delete_message(chat_id=msg.chat.id, \
                                             message_id=msg.message_id)
            except:
                pass
        else:
            try:
                await bot.delete_message(chat_id=msg.chat.id, \
                                             message_id=msg.message_id)
            except:
                pass
