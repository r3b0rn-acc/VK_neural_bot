import json


def put_in_base(name_database, cell, feature, featurePath):
    name_database.update(cell)
    feature[1] = name_database
    with open(featurePath, "w", encoding="utf8") as names:
        json.dump(feature,
                  names,
                  indent=2,
                  ensure_ascii=False)


# Процент качества речи пользователя
def get_speech_ratio(vk, event, featurePath):
    # Имя отправителя
    with open(featurePath, encoding="utf8") as data:
        feature = json.load(data)

    name_database = feature[1]
    members_names = [i[:i.find(":")] for i in list(name_database.keys())]
    members_id = [i[i.find(":")+1:] for i in list(name_database.keys())]

    name_info = vk.users.get(user_ids=event.object['message']['from_id'],
                             fields="nickname")

    first_name = name_info[0]['first_name']
    last_name = name_info[0]['last_name']
    full_name = f"{first_name} {last_name}"
    userID = str(event.object['message']['from_id'])

    member = f"{full_name}:{userID}"

    # Проверка на наличие id в базе
    if userID not in members_id:
        # Запись пользователя в базу
        put_in_base(name_database, {member: [0, 0]}, feature, featurePath)

    # Проверка на отличия id и имени в базе
    elif full_name not in members_names and userID in members_id:
        indx = members_id.index(userID)
        stats = name_database[f"{members_names[indx]}:{members_id[indx]}"]

        del name_database[f"{members_names[indx]}:{members_id[indx]}"]
        put_in_base(name_database, {member: stats}, feature, featurePath)

    # "качество" речи участника
    stats = name_database[member]

    try:
        return (stats[0] / stats[1]) * 100
    # Исключение ошибки при первом сообщении
    except ZeroDivisionError:
        return 100
