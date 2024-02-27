import pymorphy2


morph = pymorphy2.MorphAnalyzer()


# Приведение строки к "инфинитиву"
def lemma(text):
    a = []
    if text.strip() != "":
        check = text.split()
        for i in check:
            if any(c not in "ёйцукенгшщзхъфывапролджэячсмитьбю" for c in i):
                a.append(i)
            else:
                a.append(morph.normal_forms(i)[0])
        a = pastV(a)
        string = ' '.join(a)

    return str(string)


# Перевод сомнительных галголов прошедшего времени к инфинитиву
def pastV(arr):
    n_arr = []
    for i in range(len(arr)):
        # Проверка окончания
        if any(arr[i].endswith(c) for c in ["ал", "ала", "ул", "ула",
                                            "ил", "ила", "ял", "яла",
                                            "ол", "ола", "ёл", "ёла",
                                            "ел", "ела"]):

            # Проверка на наличие правильного инфинитива в списке
            if any(c.normal_form.endswith("ть") for c in morph.parse(arr[i])):
                # Перебор с целью найти инфинитив
                for j in range(len(morph.parse(arr[i]))):
                    p = morph.parse(arr[i])[j]
                    if str(p.normal_form).endswith("ть"):
                        n_arr.append(p.normal_form)
                        break
            else:
                n_arr.append(arr[i])

        else:
            n_arr.append(arr[i])

    return n_arr
