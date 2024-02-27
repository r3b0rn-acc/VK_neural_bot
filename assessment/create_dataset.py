import os.path
from lemmatization import lemma
from transfers import tsfr_from_word_to_idx
import random
import csv


# Input
file_sentences = "dataset_raw_components/good_sentences.txt"  # Имя файла с предложениями
file_bad = "dataset_raw_components/bad_words.txt"  # Имя файла с ненормативной лексикой

# Output
file_train_data = "datasets/dataset.csv"  # Имя файла готового датасета
file_dictionary = "dataset_raw_components/dictionary.csv"  # Имя файла словаря для токенизации

popular_length = 5000

have_dictionary = False
if os.path.isfile(file_dictionary):
    have_dictionary = True


shuffle = True

max_words_in_sentence = 15

# Чтение файла с плохими словами
with open(file_bad, "r") as w:
    bad_words = set()
    bad_word = w.readline()
    while bad_word:
        bad_word = lemma(bad_word.rstrip("\n"))
        bad_words.add(bad_word)
        bad_word = w.readline()

bad_words = list(bad_words)

token_dictionary = {}

if not have_dictionary:
    word_popularity_dictionary = {}
    with open(file_sentences, "r") as s:
        sentence = s.readline()
        while sentence:
            # Обновление информации в словаре популярности слов
            for i in sentence.split():
                if i not in word_popularity_dictionary.keys():
                    word_popularity_dictionary[i] = 1
                else:
                    word_popularity_dictionary[i] += 1
            sentence = s.readline()

    # Сортировка словаря по популярности слов
    bad_words_dictionary = {bad_words[i]: 0 for i in range(len(bad_words))}

    word_popularity_dictionary = dict(sorted(word_popularity_dictionary.items(),
                                             key=lambda item: item[1],
                                             reverse=True))

    word_popularity_dictionary = dict(list(word_popularity_dictionary.items())[:popular_length])
    word_popularity_dictionary.update(bad_words_dictionary)
    for i in range(len(word_popularity_dictionary.items())):
        token_dictionary[list(word_popularity_dictionary.keys())[i]] = i+3

    if shuffle:
        shuffled_values = list(token_dictionary.values())
        random.shuffle(shuffled_values)
        token_dictionary = {list(token_dictionary.keys())[i]: shuffled_values[i] for i in range(len(shuffled_values))}

    # Запись первых 5000 по популярности слов + мат в новый словарь
    with open(file_dictionary, "w") as f:
        writer = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC,
                            lineterminator="\r")
        writer.writerow(["word", "id"])
        for i in range(len(token_dictionary.items())):
            writer.writerow([list(token_dictionary.keys())[i],
                             list(token_dictionary.values())[i]])

else:
    with open(file_dictionary) as f:
        reader = csv.DictReader(f)
        for row in reader:
            token_dictionary[row["word"]] = row["id"]


with open(file_sentences, "r") as s:
    sentence = s.readline()
    with open(file_train_data, "w") as f:
        writer = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC,
                            lineterminator="\r")
        writer.writerow(["sentence", "grade"])
        while sentence:
            if len(sentence.split()) <= max_words_in_sentence - 1:
                # Лемматизация предложения
                sentence = lemma(sentence)
                # Оценка предложения
                grade = 1

                # Добавление плохих слов случайным образом с вероятностью 50%
                if random.choice([0, 1]) == 1 and len(sentence.split()) < max_words_in_sentence - 1:
                    grade = 0
                    # Сколько плохих слов добавить в предложение (от 1 до 3)
                    bad_words_num_max = (max_words_in_sentence - 1) - len(sentence.split())
                    if bad_words_num_max > 3:
                        bad_words_num_max = 3
                    num_of_bad_words = random.randrange(1, bad_words_num_max + 1)
                    sentence = sentence.split()
                    for i in range(num_of_bad_words):
                        sentence.insert(random.randrange(0, len(sentence) + 2),
                                        random.choice(bad_words))
                    sentence = " ".join(sentence)

                num_of_zeros = max_words_in_sentence - len(sentence.split()) - 1
                sentence = tsfr_from_word_to_idx(sentence,
                                                 num_of_zeros,
                                                 token_dictionary=token_dictionary)
                writer.writerow(["_".join(list(map(str, sentence))), grade])
            sentence = s.readline()
