import re
import json


# Функция установки границы обучения
def set_border(request, featurePath):
    # Число из сообщения
    maximal_lines = re.match(r'\/border+\s\S+', request.lower())
    maximal_lines = maximal_lines.group(0).split(' ')[-1]

    if maximal_lines.isdigit() == False:
        return "Граница должна быть числом!"

    maximal_lines = int(maximal_lines)

    # Если число введено не корректно
    if maximal_lines <= 0:
        message = str(f"""Невозможно установить границу {maximal_lines}\n
Граница установлена на 1 строку""")
        maximal_lines = 1
    # Если число введено корректно
    else:
        message = "Граница задана!"

    with open(featurePath, encoding="utf8") as f:
        params = json.load(f)

    params[0]["maximal_lines"] = maximal_lines

    # Запись новых настроек
    with open(featurePath, 'w', encoding="utf8") as new_settings:
        json.dump(params,
                  new_settings,
                  indent=2,
                  ensure_ascii=False)

    return message
