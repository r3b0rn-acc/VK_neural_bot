from collections import Counter
import numpy as np
import json


# Создание словарей для посимвольной токенизации предложения
def text_to_seq(path):
    # Считывание строк баз
    with open(path, encoding="utf8") as data:
        words = json.load(data)

        text_sample = []

        for i in range(len(words)):
            text_sample.append(words[i][0])

    text_sample = ' '.join(text_sample)

    # Подсчет количества и частоты букв, сортировка
    char_counts = Counter(text_sample)
    char_counts = sorted(char_counts.items(), key=lambda x: x[1], reverse=True)

    # Создание массива с сортированными символами
    sorted_chars = [char for char, _ in char_counts]
    # Создание словарей
    char_to_idx = {char: index + 3 for index, char in (enumerate(sorted_chars))}
    idx_to_char = {v: k for k, v in char_to_idx.items()}
    sequence = np.array([char_to_idx[char] for char in text_sample])

    return sequence, char_to_idx, idx_to_char
