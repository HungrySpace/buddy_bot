from urllib import request
import urllib.request
import re
import requests
import sys

# = str(input('Введите ссылку на видео: '))


def get_video(link_to_video):
    try:
        print(link_to_video)
        # link_to_video = link_to_video.replace(link_to_video[-1], '')
        # Получаем ответ страницы и выводим исходный код страницы
        response = requests.get(link_to_video)
        name_video = 'video.mp4'

        text_for_parser = response.content
        text_for_parser = str(text_for_parser)

        regxp = '(http[^"]+mp4)'
        result = []
        result = re.findall(regxp, text_for_parser)

        print('Начинаем закачку видео... ')
        print(link_to_video)
        # ideo = request.urlretrieve(result[0], name_video)
        video = request.urlopen(result[0])
        # video = open('video.mp4', 'rb')
        print('Видео загружено')
        return video
    except:
        return "Все в говне"
