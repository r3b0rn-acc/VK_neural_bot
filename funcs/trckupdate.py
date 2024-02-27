import json


# Обновление статистики речи
def update_speech_ratio(vk, event, featurePath, quality):
    # Имя отправителя
    name_info = vk.users.get(user_ids=event.object['message']['from_id'],
                             fields="nickname")

    first_name = name_info[0]['first_name']
    last_name = name_info[0]['last_name']
    userID = str(event.object['message']['from_id'])

    member = f"{first_name} {last_name}:{userID}"

    # Обновление базы в соответствии с "качеством" отправленного сообщения
    with open(featurePath, encoding="utf8") as data:
        feature = json.load(data)
    stats = feature[1][member]

    # Если cообщение было "хорошим"
    if quality == 1:
        good_words = stats[0] + 1
        all_words = stats[1] + 1
        feature[1][member] = [good_words, all_words]

    # Если cообщение было "плохим"
    else:
        all_words = stats[1] + 1
        feature[1][member] = [stats[0], all_words]

    # Запись обновленных данных в файл
    with open(featurePath, "w", encoding="utf8") as names:
        json.dump(feature,
                  names,
                  indent=2,
                  ensure_ascii=False)
