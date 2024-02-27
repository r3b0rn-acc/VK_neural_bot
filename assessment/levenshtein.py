import json
from fuzzywuzzy import fuzz


# Считывание списка слов
path = "assessment/dataset_raw_components/words_full.json"
with open(path, encoding="utf8") as f:
    a = json.load(f)

# Создание алфавита и массива, разбитого на 34 зоны
alphabet = list("-абвгдежзийклмнопрстуфхцчшщъыьэюяё")
arr = [[] for i in range(len(alphabet))]

# Добавление в зоны слова в соответствии с буквой, на которую они начинаются
k = 0
for i in range(len(a)):
    if i + 1 < len(a):
        if a[i][0] == a[i + 1][0]:
            arr[k].append(a[i])
        else:
            arr[k].append(a[i])
            k += 1


def leven(string):
    # Форматирование входящей строки
    string = string.split(" ")

    num_of_letters = 5

    rep = [0 for i in string if len(i) >= num_of_letters]
    count = -1

    # Прогон по каждому слову
    for c in range(len(string)):
        # Если в слове не менее num_of_letters букв
        if (len(string[c]) >= num_of_letters and
           all(b in "ёйцукенгшщзхъфывапролджэячсмитьбю" for b in string[c])):
            percent = 80
            count += 1
            # Цикл в диапазоне зоны буквы
            for i in range(len(arr[alphabet.index(string[c][0])])):
                similar = int(fuzz.ratio(string[c],
                                         arr[alphabet.index(string[c][0])][i]))
                # Если слово схоже со словарным больше чем на 85%
                if similar > percent:
                    percent = similar
                    # Если еще не в списке
                    if ((similar, string[c],
                         arr[alphabet.index(string[c][0])][i]) not in rep):

                        # Добавление в список объекта форматом:
                        # Схожесть, исходное слово, форматированное слово
                        rep[count] = ([similar, string[c],
                                      arr[alphabet.index(string[c][0])][i]])

    # Сборка строки обратно в строку
    string = " ".join(string)

    # Замена слов
    for i in range(len(rep)):
        if rep[i] != 0:
            string = string.replace(rep[i][1], rep[i][2])

    return string
