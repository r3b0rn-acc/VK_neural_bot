import csv


# Токинезация числа в букву в соответствии со словарем
def tsfr_from_idx_to_char(nums, idx_to_char):
    string = ""

    # Расшифровка массива в соответствии со словарем
    for i in nums:
        if i != 0 and i != 1:
            string += str(idx_to_char.get(i)) + " "
        if i == 2:
            string += "-unidentified-" + " "

    return string.rstrip()


# Токинезация из слова в число в соответствии с путем к словарю
def tsfr_from_word_to_idx(string, num_of_zeros,
                          token_dictionary={}, dictionary_path=False,):
    # Заполнение пустого пространства нулями и единицей
    token = [0]*num_of_zeros
    token.append(1)

    if dictionary_path:
        # Считывание данных словаря
        with open(dictionary_path) as f:
            reader = csv.DictReader(f)
            for row in reader:
                token_dictionary[row["word"]] = row["id"]

    # Запись последовательности чисел в массива
    # 2 - неизвестное слово
    for i in string.split(" "):
        token.append(int(token_dictionary.get(i, 2)))

    return token
