import config
import datetime
from aiogram import Bot, Dispatcher, types
from aiogram.utils.executor import Executor

bot = Bot(config.TOKEN)
dis = Dispatcher(bot)
ex = Executor(dis)

@dis.message_handler(commands=['help'])
async def onhelp(ctx):
    await ctx.reply('''
Litemod - это бот модератор для телеграмм с открытым кодом! Вся информация про меня доступна в канале @litemodnews. Вот список моих команд:

/help - написать этот текст
/who - узнать роль человека
/kick - кикнуть пользователя (для адм)
/ban - забанить пользователя (для адм)
/mute кол-во минут причина - замутить пользователя (для адм)
/unmute - размутить пользователя (для адм)
/del - удалить несколько сообщений (для адм)
/ad - создать объявление (для адм)
/setadmin - назначить админа (для владельца)
/deladmin - удалить админа (для владельца)
''')

@dis.message_handler(commands=['who'])
async def onwho(ctx):
    try:
        getfrom = await bot.get_chat_member(ctx.chat.id, ctx.reply_to_message.from_user.id)
        await ctx.reply('Роль ' + getfrom.user.username + ': ' + getfrom.status)
    except:
        await ctx.reply('Эта команда должна быть ответом на сообщение!')

@dis.message_handler(commands=['kick'])
async def onkick(ctx):
    getfrom = await bot.get_chat_member(ctx.chat.id, ctx.from_user.id)
    if getfrom.status in ['administrator', 'creator']:
        try:
            await bot.kick_chat_member(ctx.chat.id, ctx.reply_to_message.from_user.id)
            await ctx.reply('@' + ctx.reply_to_message.from_user.username + ' был успешно кикнут!')
        except:
            await ctx.reply('Не удалось кикнуть пользователя.')
    else:
        await ctx.reply('Вы не админ!')

@dis.message_handler(commands=['ban'])
async def onban(ctx):
    getfrom = await bot.get_chat_member(ctx.chat.id, ctx.from_user.id)
    if getfrom.status in ['administrator', 'creator']:
        try:
            await bot.ban_chat_member(ctx.chat.id, ctx.reply_to_message.from_user.id)
            await bot.delete_message(ctx.chat.id, ctx.reply_to_message.message_id)
            await ctx.reply('@' + ctx.reply_to_message.from_user.username + ' был успешно забанен!')
        except:
            await ctx.reply('Не удалось забанить пользователя.')
    else:
        await ctx.reply('Вы не админ!')

@dis.message_handler(commands=['mute'])
async def onmute(ctx):
    getfrom = await bot.get_chat_member(ctx.chat.id, ctx.from_user.id)
    if getfrom.status in ['administrator', 'creator']:
        try:
            if len(ctx.text.split()) >= 3:
                await bot.restrict_chat_member(ctx.chat.id, ctx.reply_to_message.from_user.id, types.ChatPermissions(can_send_messages=False), until_date=datetime.timedelta(minutes=int(ctx.text.split()[1])))
                await ctx.reply('@' + ctx.reply_to_message.from_user.username + ' был замучен на ' + ctx.text.split()[1] + ' минут.\nПричина: '+' '.join(ctx.text.split()[2:]))
            else:
                await ctx.reply('Недостаточно аргументов!\nНужно писать: /mute (кол-во минут) (причина)')
        except:
            await ctx.reply('Не удалось замутить пользователя.')
    else:
        await ctx.reply('Вы не админ!')

@dis.message_handler(commands=['unmute'])
async def onunmute(ctx):
    getfrom = await bot.get_chat_member(ctx.chat.id, ctx.from_user.id)
    if getfrom.status in ['administrator', 'creator']:
        try:
            await bot.restrict_chat_member(ctx.chat.id, ctx.reply_to_message.from_user.id, types.ChatPermissions(can_send_messages=True))
            await ctx.reply('@' + ctx.reply_to_message.from_user.username + ' был успешно размучен!')
        except:
            await ctx.reply('Не удалось размутить пользователя.')
    else:
        await ctx.reply('Вы не админ!')

@dis.message_handler(commands=['del'])
async def ondel(ctx):
    getfrom = await bot.get_chat_member(ctx.chat.id, ctx.from_user.id)
    if getfrom.status in ['administrator', 'creator']:
        if len(ctx.text.split()) >= 2:
            try:
                for i in range(int(ctx.text.split()[1])):
                    await bot.delete_message(ctx.chat.id, ctx.reply_to_message.message_id + i)
            except:
                await ctx.reply('Не удалось удалить все сообщения.')
        else:
            await ctx.reply('Недостаточно аргументов!\nНужно писать: /del (кол-во сообщений которых нужно удалить)')
    else:
        await ctx.reply('Вы не админ!')

@dis.message_handler(commands=['ad'])
async def onad(ctx):
    getfrom = await bot.get_chat_member(ctx.chat.id, ctx.from_user.id)
    if getfrom.status in ['administrator', 'creator']:
        if len(ctx.text.split()) >= 2:
            try:
                await bot.send_message(ctx.chat.id, 'Объявление от админа @' + ctx.from_user.username + ' :\n\n' + ' '.join(ctx.text.split()[1:]))
                await bot.delete_message(ctx.chat.id, ctx.message_id)
            except:
                await ctx.reply('Не удалось отправить объявление.')
        else:
            await ctx.reply('Недостаточно аргументов!\nНужно писать: /ad (текст)')
    else:
        await ctx.reply('Вы не админ!')

@dis.message_handler(commands=['setadmin'])
async def onsetadmin(ctx):
    getfrom = await bot.get_chat_member(ctx.chat.id, ctx.from_user.id)
    if getfrom.status == 'creator':
        try:
            await bot.promote_chat_member(ctx.chat.id, ctx.reply_to_message.from_user.id, can_manage_chat=True, can_pin_messages=True)
            await ctx.reply('Админ успешно назначен!')
        except:
            await ctx.reply('Не удалось назначить админа.')
    else:
        await ctx.reply('Вы не владелец!')

@dis.message_handler(commands=['deladmin'])
async def ondeladmin(ctx):
    getfrom = await bot.get_chat_member(ctx.chat.id, ctx.from_user.id)
    if getfrom.status == 'creator':
        try:
            await bot.promote_chat_member(ctx.chat.id, ctx.reply_to_message.from_user.id, can_manage_chat=False, can_pin_messages=False)
            await ctx.reply('Админ успешно удален!')
        except:
            await ctx.reply('Не удалось удалить админа.')
    else:
        await ctx.reply('Вы не владелец!')

ex.start_polling()
