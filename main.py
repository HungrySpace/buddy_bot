from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, InlineQueryHandler
import logging
from telegram import InlineQueryResultArticle, InputTextMessageContent

updater = Updater(token='1764514462:AAEA6Bf2DWwYcNw4Md78sm75dLncV9_QZME', use_context=True)
PORT = '8443'
TELEGRAM_TOKEN = '1764514462:AAEA6Bf2DWwYcNw4Md78sm75dLncV9_QZME'
# запускаем слушающий вебсервер
updater.start_webhook(
  listen="0.0.0.0",
  port=PORT,  # HEROKU требует, чтобы порт вебсервера задавался через переменные окружения
  url_path=TELEGRAM_TOKEN  # добавляем секретное значение в адрес, который слушаем
)

# говорим Телеграму: "присылай события бота по этому адресу"
HEROKU_APP_NAME = 'app-t-bot'
updater.bot.set_webhook(f"https://{HEROKU_APP_NAME}.herokuapp.com/{TELEGRAM_TOKEN}")
updater.idle()


dispatcher = updater.dispatcher
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")


start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)


def echo(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)


echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
dispatcher.add_handler(echo_handler)


def caps(update, context):
    print()
    if len(context.args) > 0:
        text_caps = ' '.join(context.args).upper()
    else:
        text_caps = 'ты втираешь какую-то дичь!'
    context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)


caps_handler = CommandHandler('caps', caps)
dispatcher.add_handler(caps_handler)


def inline_caps(update, context):
    query = update.inline_query.query
    if not query:
        return
    results = list()
    results.append(
        InlineQueryResultArticle(
            id=query.upper(),
            title='Caps',
            input_message_content=InputTextMessageContent(query.upper())
        )
    )
    context.bot.answer_inline_query(update.inline_query.id, results)


inline_caps_handler = InlineQueryHandler(inline_caps)
dispatcher.add_handler(inline_caps_handler)


def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")


unknown_handler = MessageHandler(Filters.command, unknown)
dispatcher.add_handler(unknown_handler)


updater.start_polling()
