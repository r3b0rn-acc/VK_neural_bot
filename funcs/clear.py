import json


# Очистка баз сообщений + статистики речи
def clear_chat(goodSentencesPath, badSentencesPath, featurePath):
    open(goodSentencesPath, 'w').close()
    open(badSentencesPath, 'w').close()
    with open(featurePath, encoding="utf8") as f:
        feature = json.load(f)
        feature[1] = {}
    with open(featurePath, 'w') as names:
        json.dump(feature,
                  names,
                  indent=2,
                  ensure_ascii=False)

    message = str("База очищена!")

    return message
