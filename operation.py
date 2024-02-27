import mc
from mc.builtin import validators
import shifr


def coolString(string, separator=[".", "!", "?"]):
    string = string[0].upper() + string[1:]

    for i in separator:
        if i in string:
            string = string.split(i)
            for j in range(1, len(string)):
                if len(string[j]) > 0:
                    string[j] = string[j].lstrip()
                    string[j] = " " + string[j][0].upper() + string[j][1:]
            string = i.join(string)
    return string


# Создание сообщения с использованием базы указанного txt файла
def marcov(messagesPath, key):
    def generate(generator):
        result = generator.generate_phrase(attempts=20, validators=[
                            validators.words_count(minimal=1, maximal=15),
                            validators.chars_count(minimal=1, maximal=150)])
        return result

    with open(messagesPath, "r") as chat:
        sentences = chat.readlines()

    # Расшифровка сообщений
    sentences = [shifr.decode(key, i.encode()) for i in sentences]

    # Создание генератора
    generator = mc.PhraseGenerator(samples=sentences, order=1)

    # Создание сообщения
    result = generate(generator)
    for i in range(5):
        if result.lower() in [i.lower() for i in sentences]:
            result = generate(generator)
        else:
            break

    return coolString(result)
