import re
from math import ceil

import numpy as np
from tensorflow.keras.models import load_model

from assessment.lemmatization import lemma
from assessment.levenshtein import leven
from transfers import tsfr_from_word_to_idx

# Загрузка обученной модели
model = load_model("assessment/network/11speecher_dense_test.h5")


# Разделение большого массива на равные части
def parting(xs, parts):
    part_len = ceil(len(xs) / parts)
    return [xs[part_len * k:part_len * (k+1)] for k in range(parts)]


# Функция определения качества речи
def appraise(input_string):
    dictionary_path = "assessment/dataset_raw_components/dictionary.csv"

    # Обработка входящей строки
    input_string = re.sub(r'[0-9]', '', input_string).lower().strip()

    # Распределение входящих данных
    if len(input_string.split(" ")) < 15:
        num_of_zeros = 15 - len(input_string.split()) - 1
        if num_of_zeros == 14:
            return 1

        # Запись обработанного входящего предложения в переменную в виде чисел
        X = tsfr_from_word_to_idx(lemma(input_string),
                                  num_of_zeros,
                                  dictionary_path=dictionary_path)

        X = np.array([X])

        # Вывод нейросети
        prediction = model.predict(X, verbose=0)

    else:
        prediction = []
        multiply = lambda arr: arr[0] * multiply(arr[1:]) if arr else 1
        parts = ceil(len(input_string.split(" ")) / 14)
        array = parting(input_string.split(" "), parts)
        for i in range(len(array)):
            num_of_zeros = 15 - len(array[i]) - 1

            # Запись входящего предложения в переменную в виде чисел
            X = tsfr_from_word_to_idx(lemma(leven(" ".join(array[i]).strip())),
                                      num_of_zeros,
                                      dictionary_path=dictionary_path)


            X = np.array([X])

            # Добывление нового вывода нейросети
            prediction.append(model.predict(X, verbose=0))

        prediction = multiply(prediction)**(1 / len(prediction))

    # print(prediction, lemma(leven(input_string)))

    if prediction >= 0.575:
        return 1
    else:
        return 0
