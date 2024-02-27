import re
import json


# Функция установки шанса сообщения бота
def set_chance(request, featurePath):

    # Число из сообщения
    chance = re.match(r'\/chance+\s\S+', request.lower())
    chance = chance.group(0).split(' ')[-1].rstrip("%")

    if chance.isdigit() == False:
        return "Шанс должен быть числом!"

    chance = int(chance)

    # Если число введено не корректно
    if chance > 100:
        message = str(f"""Невозможно установить шанс {chance}%.\n
Установлен шанс 100%""")
        chance = 100

    # Если число введено не корректно
    elif chance < 0:
        message = str(f"""Невозможно установить шанс {chance}%.\n
Установлен шанс 0%""")
        chance = 0

    # Если число введено корректно
    else:
        message = str("Шанс задан!")

    with open(featurePath, encoding="utf8") as f:
        params = json.load(f)

    params[0]["chance"] = chance

    # Запись новых настроек
    with open(featurePath, 'w', encoding="utf8") as new_settings:
        json.dump(params,
                  new_settings,
                  indent=2,
                  ensure_ascii=False)

    return message
