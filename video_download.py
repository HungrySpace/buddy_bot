import re
from urllib import request
import requests
import youtube_dl
import os


# = str(input('Введите ссылку на видео: '))


def get_video(link_to_video, context, message):
    try:
        # print(link_to_video)
        # # link_to_video = link_to_video.replace(link_to_video[-1], '')
        # # Получаем ответ страницы и выводим исходный код страницы
        # response = requests.get(link_to_video)
        # name_video = 'video.mp4'
        #
        # text_for_parser = response.content
        # text_for_parser = str(text_for_parser)
        # print(text_for_parser)
        # regxp = '(http[^"]+mp4)'
        # result = []
        # result = re.findall(regxp, text_for_parser)
        # #print(result)
        # print('Начинаем закачку видео... ')
        # print(link_to_video)
        # # ideo = request.urlretrieve(result[0], name_video)
        # video = request.urlopen(result[0])
        # # video = open('video.mp4', 'rb')
        # print('Видео загружено')

        with youtube_dl.YoutubeDL({'outtmpl': 'jopa.mp4'}) as ydl:
            ydl.download([link_to_video])

        context.bot.send_video(message.chat_id, open('jopa.mp4', 'rb'))
        #video = open('jopa.mp4', 'rb')
        os.remove('jopa.mp4')
        context.bot.delete_message(chat_id=message.chat_id,
               message_id=message.message_id,)

        return 1
    except Exception as e:
        return e
