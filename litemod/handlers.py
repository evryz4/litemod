from datetime import timedelta, datetime

from aiogram import Router, F, Bot, MagicFilter
from aiogram.types import Message, ChatPermissions
from aiogram.filters import Command
from aiogram.enums.parse_mode import ParseMode

from sqlitewithoutsql.database import Database
from sqlitewithoutsql.sqltype import Sqltype

from filters import init, AdminFilter
from config import *

bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)

init(_bot=bot)

router = Router()

async def gettext(msg: Message, txt: str, msgtype: str = 'ok', **other_rows):
    now = datetime.now()
    time = now.strftime("%H:%M:%S")

    ret = f'user: @{msg.from_user.username}\ntime: {time}\ntype: [{msgtype.upper()}]\ntext: "{txt}"'

    for row in other_rows:
        ret += f'\n{row}: {other_rows[row]}'

    return ret

db = Database('litemod/litemod.db')
db.new_table('warns', chatid=Sqltype.INT, userid=Sqltype.INT, quantity=Sqltype.INT)
if len(db.get_table('warns')) == 0:
    db.insert('warns', 1, 1, 1)

@router.message(Command('start'))
async def start_handler(msg: Message):
    await msg.reply(await gettext(msg, 'Hi, It\'s opensource moderaton bot for telegram. Channel - @litemodnews'))
    
    if msg.chat.type not in ['group', 'supergroup']:
        await msg.reply(await gettext(msg, 'Add bot to the server!', 'warning'))
    else:
        await msg.reply(await gettext(msg, 'Write /help for see the command list', 'info'))


@router.message(Command('help'))
async def help_handler(msg: Message):
    await msg.reply(await gettext(msg, 'Command list:\n/start - see the start text\n/help - see this menu\n/del (reply) / [quantity] delete replied message / last [quantity messages]\n/ban [reason] (reply) - ban user\n/warn [reason] - warn user (3 warns - ban)\n/mute (nothing) / [time quantity] [m/h/d] [reason] (reply) - mute the user forever / until entered time\n/unmute (reply) - unmute the user'))

@router.message(Command('del'), AdminFilter())
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

@router.message(Command('ban'), F.reply_to_message != None, AdminFilter())
async def ban_handler(msg: Message):
    try:
        await bot.ban_chat_member(chat_id=msg.chat.id, \
                                  user_id=msg.reply_to_message.from_user.id)
        if len(msg.text.split()) > 1:
            await msg.reply(await gettext(msg, f'User has been banned succesfully:', banned='@'+msg.reply_to_message.from_user.username, reason=f'"{' '.join(msg.text.split()[1:])}"'))
        else:
            await msg.reply(await gettext(msg, 'User has been banned succesfully', banned='@'+msg.reply_to_message.from_user.username))
    except:
        await msg.reply(await gettext(msg, 'Some err has occured. Try to be sure, that:\n1. Bot has permissions for ban users\n2. Bot is higher in permissions than user is going to be banned', 'err'))

@router.message(Command('warn'), F.reply_to_message != None, AdminFilter())
async def warn_handler(msg: Message):
    warns = db.get_table('warns')
    exists = True
    for row in warns:
        if warns[row]['chatid'] == msg.chat.id and warns[row]['userid'] == msg.from_user.id:
            if warns[row]['quantity'] >= 2 :
                await bot.ban_chat_member(msg.chat.id, msg.reply_to_message.from_user.id)
                await msg.reply(await gettext(msg, 'User has got 3 warns and has been succesfully banned', warned='@'+msg.reply_to_message.from_user.username), reason=f'"{' '.join(msg.text.split()[1:])}"')
            else:
                db.edit('warns', row, 'quantity', warns[row]['quantity'] + 1)
                await msg(await gettext(msg, f'User has been succesfully warned. Total warns: {warns[row]['quantity'] + 1}', reason=f'"{' '.join(msg.text.split()[1:])}"', warned='@'+msg.reply_to_message.from_user.username))
            exists = False
    if exists:
        db.insert('warns', msg.chat.id, msg.from_user.id, 1)
        await msg.reply(await gettext(msg, f'User has been succesfully warned.', reason=f'"{' '.join(msg.text.split()[1:])}"', warned='@'+msg.reply_to_message.from_user.username))

@router.message(Command('mute'), (F.reply_to_message != None), AdminFilter())
async def mute_handler(msg: Message):
    if len(msg.text.split()) == 1:
        await bot.restrict_chat_member(msg.chat.id, msg.reply_to_message.from_user.id, ChatPermissions(can_send_messages=False))
        await msg.reply(await gettext(msg, 'User has succesfully muted'))
        return 0

    if msg.text.split()[2] == 'm':
        td = timedelta(minutes=int(msg.text.split()[1]))
    elif msg.text.split()[2] == 'h':
        td = timedelta(hours=int(msg.text.split()[1]))
    elif msg.text.split()[2] == 'd':
        td = timedelta(days=int(msg.text.split()[1]))

    dt = datetime.now() + td

    await bot.restrict_chat_member(msg.chat.id, msg.reply_to_message.from_user.id, ChatPermissions(can_send_messages=False), until_date=dt.timestamp())

    if len(msg.text.split()) > 3:
        await msg.reply(await gettext(msg, 'User has succesfully muted', muted='@'+msg.reply_to_message.from_user.username, until=dt.strftime("%D | %H:%M:%S"), reason=f'"{' '.join(msg.text.split()[3:])}"'))
    else:
        await msg.reply(await gettext(msg, 'User has succesfully muted', muted='@'+'@'+msg.reply_to_message.from_user.username, until=dt.strftime("%D | %H:%M:%S")))

@router.message(Command('unmute'), F.reply_to_message != None, AdminFilter())
async def unmute_handler(msg: Message):
    await bot.restrict_chat_member(msg.chat.id, msg.reply_to_message.from_user.id, ChatPermissions(can_send_messages=True))
    await msg.reply(await gettext(msg, 'User has succesfully unmuted', unmuted='@'+msg.reply_to_message.from_user.username))
