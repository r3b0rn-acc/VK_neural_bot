import json
from random import choice

from operation import marcov


# Функция создания "цитаты"
def do_citation(sentencesForUser, featurePath, key):
    # Считывание имен из базы
    with open(featurePath, encoding="utf8") as name_list:
        imena = [i[:i.find(":")] for i in list(json.load(name_list)[1].keys())]

    full_imya = choice(imena)
    try:
        # Генерация цитаты
        message = f'"{marcov(sentencesForUser, key)}"   ©{full_imya}'
    # Если не написано ни одно сообщение
    except ValueError:
        message = "Ещё не написано ни одно сообщение!"

    return message
