import os
import random
from telegram.ext import MessageHandler, Filters, CommandHandler
import sqlite3
from video_download import get_video


def echo(update, context):
    print(update.message.chat.id)
    context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)


def handle_start_help(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Я тут! у меня появились две команды. Первая это "
                                                                    "узнать что либо у меня [Бот. твое сообщение] и "
                                                                    "Вторая это обучение [Бот! твое сообщение # ответ "
                                                                    "на него]")


def start_message(update, context):
    message = update.message.text
    message_id = update.message.chat.id
    print(message, message_id)

    message_txt = str(update.message.text)
    if message_txt.lower().find('бот') == 0:
        if len(message_txt) > 3:
            if message_txt[3] == ".":
                message_txt = message_txt[4:len(message_txt)].lower().strip()
                otvet = sql_table(message_txt, ".")
                # print(otvet)
                context.bot.send_message(chat_id=message_id, text=str(otvet))
            elif message_txt[3] == "!":
                if len(message_txt) > 4:
                    if message_txt.find('#') > 0:
                        arrOtvet = message_txt.split('#')
                        txtValue = str(arrOtvet[1]).lower().strip()
                        message_txt = message_txt[4:message_txt.find("#")].lower().strip()
                        otvet = sql_table(message_txt, "!", txtValue)
                        context.bot.send_message(chat_id=message_id, text=str(otvet))
    elif message_txt.lower().find('https://') == 0:
        #context.bot.send_message(chat_id="-1001263523681", text=str("загружаю(возможно)"))
        context.bot.send_message(chat_id=message_id, text=str("загружаю(возможно)"))
        try:
            context.bot.send_video(message_id, get_video(message_txt, context, message_id))
        except Exception as e:
            print(e)
            context.bot.send_message(chat_id=message_id, text=str(e))


def sql_table(Mmessage, command, val=None):
    print('прошел7')
    con = sqlite3.connect('mydatabase.db')
    cursorObj = con.cursor()
    print(command)
    if command == "!":
        print('прошел8')
        add = [Mmessage, val]
        dda = [val, Mmessage]
        # print(add[0])
        cursorObj.execute('''SELECT message FROM employees WHERE message=?''', [Mmessage])
        exists = cursorObj.fetchall()
        if not exists:
            print('прошел9')
            cursorObj.execute('INSERT INTO employees VALUES(?,?)', add)
            con.commit()
        else:
            print('прошел10')
            # messageValue - изменяемая , message - искомая
            cursorObj.execute('SELECT messageValue FROM employees where message = ?', (Mmessage,))
            dda[0] = str(cursorObj.fetchone()[0]) + "#" + str(dda[0])
            # print(dda[0])
            cursorObj.execute('UPDATE employees SET messageValue = ? where message = ?', dda)
            con.commit()
        arrOtv = ["Вроде понял", "Договорились", "Заметано", "Думаю дошло до меня", "лан, так и быть, запишу"]
        ovt = arrOtv[random.randint(0, 4)]

    else:
        cursorObj.execute('''SELECT message FROM employees WHERE message=?''', [Mmessage])
        exists = cursorObj.fetchall()
        if exists:
            print('прошел11 = ', Mmessage)
            cursorObj.execute('SELECT messageValue FROM employees where message = ?', (Mmessage,))
            ovt = cursorObj.fetchone()[0]
            if str(ovt).find('#') > 0:
                arrOtv = str(ovt).split('#')
                ovt = arrOtv[random.randint(0, len(arrOtv) - 1)]
        else:
            arrOtv = ["Упс, Я хз что ответить...", "Чё?", "Блин, что то знакомое", "Зашиши ка мне это в базу",
                      "непонятно..."]
            ovt = arrOtv[random.randint(0, 4)]
    print('прошел12')
    con.close()
    print(ovt)
    print(
        '############################################################################################################')
    return ovt


def setup_dispatcher(dp):
    dp.add_handler(CommandHandler('help', handle_start_help))
    dp.add_handler(MessageHandler(Filters.text & (~Filters.command), start_message))
    # dp.add_handler(MessageHandler(Filters.text & (~Filters.command), echo))
    return dp
