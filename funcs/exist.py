import os
import json
import secrets


# Процедура создания папки и основных файлов беседы
def chat_folder_create(goodSentencesPath, badSentencesPath, chatPath, featurePath):
    os.mkdir(chatPath)
    open(goodSentencesPath, 'tw', encoding='utf-8').close()
    open(badSentencesPath, 'tw', encoding='utf-8').close()

    # Генерация ключа
    alphabet = "qwertyuiopasdfghjklzxcvbnm"
    key = "".join([str(secrets.choice(alphabet)) for i in range(10)])

    # Назначение стандартных настроек
    preset = {
        "maximal_lines": 500,
        "chance": 10,
        "key": key
    }

    # Запись стандартных настроек
    with open(featurePath, 'w') as settings:
        json.dump([preset, {}],
                  settings,
                  indent=2,
                  ensure_ascii=False)
