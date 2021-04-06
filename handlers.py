import os
from telegram.ext import MessageHandler, Filters


def echo(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)


def setup_dispatcher(dp):
    dp.add_handler(MessageHandler(Filters.text & (~Filters.command), echo))
    return dp
