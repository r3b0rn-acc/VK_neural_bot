from operation import marcov


# Функция отправки сообщения
def do_message(sentencesForUser, key):
    # Генерация сообщение
    try:
        message = marcov(sentencesForUser, key)
    # Если не написано ни одно сообщение
    except ValueError:
        message = "Ещё не написано ни одно сообщение!"

    return message
