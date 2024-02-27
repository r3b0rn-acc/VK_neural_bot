import re


# Сортировка полученного сообщения
def sort(string):
    commands = ["/border", "/chance", "/clear",
                "/message", "/citation", "/help"]

    # Очистка от неправильных команд
    if (string.lower().strip()[0] == "/" and
        string.lower().strip().split()[0] not in commands):

        return ""
    elif string.lower().strip().split()[0] in commands:
        return string.lower()

    # Очистка от ссылок
    string = re.sub(r'http\S+', '', string)

    # Очистка от номеров (3 вариаций написания)
    string = re.sub(
        r"(\+\d|\d)(\s|-)\d\d\d(\s|-)\d\d\d(\s|-)\d\d(\s|-)\d\d",
        "", string)

    string = re.sub(
        r"(\+\d|\d)(\(|\s\(|-\()\d\d\d(\)|\)\s|\)-)\d\d\d(\s|-)\d\d(\s|-)\d\d",
        "", string)

    string = re.sub(r"(\+\d|\d)\d\d\d\d\d\d\d\d\d\d", "", string)

    # Очистка от обращений в сообщениях
    string = re.sub(r"\[.+\|.+\],*\s*", "", string)

    string = re.sub(r" +", " ", string)

    string = re.sub(r" (?P<symbol>[.,!?]) ", r"\g<symbol>", string)

    string = re.sub(r"(?P<last_char>\S) (?P<symbol>[.,!?])", r"\g<last_char>\g<symbol> ", string)

    string = re.sub(r"(?P<last_char>[0-9a-zA-Zа-яА-ЯёЁ])(?P<needed_symbol>[.,!?])(?P<other_symbols>[.,!?]+)", r"\g<last_char>\g<needed_symbol>", string)

    string = re.sub(r"(?P<symbol1>[.,!?]) (?P<symbol2>[.,!?])", r"\g<symbol1>\g<symbol2>", string)

    string = re.sub(r"(?P<last_char>[0-9a-zA-Zа-яА-ЯёЁ])(?P<symbol>[.,!?])(?P<first_char>[0-9a-zA-Zа-яА-ЯёЁ])", r"\g<last_char>\g<symbol> \g<first_char>", string)

    if string != "":
        return (string[0].upper() + string[1:]).strip()
    else:
        return ""


if __name__ == "__main__":
    print(sort(" я 8(995) 233-07-93, это моя    некрасивая строка .  но щас  она станет,действительно , пиздатой ,правда.  , ! да ! между прочим ..."))
