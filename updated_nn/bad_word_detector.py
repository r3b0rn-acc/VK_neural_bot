import pickle
import numpy as np

from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import load_model


with open('data/tokenizers/tokenizer.pickle', 'rb') as handle:
    tokenizer = pickle.load(handle)

model = load_model('models/model_LSTM_SimpleRNN.h5')
inp_chars = 15


def detect(word):
    t = word.lower()
    data = tokenizer.texts_to_sequences([t])
    data_pad = pad_sequences(data, maxlen=inp_chars)

    res = model.predict(data_pad, verbose=0, use_multiprocessing=True)
    return res, str(np.argmax(res)).replace('0', 'хорошее').replace('1', 'плохое')

test_sample = ['*****', 'яблочко', '*****', 'каркуша', '*****',
               'уха', '*****', 'шалаш', '*****', 'шлюпка',
               '*****', 'мандарины', '*****', 'именины',
               '*****', 'юбилей', '*****', 'отбеливающее', '*****',
               'разглядка', '*****', 'гребля', '*****', 'гладь',
               '*****', 'мангуст', '*****', 'копчик', '*****', 'внук',
               '*****', 'хвост', '*****', 'зубочист', '*****', 'выхухоль']

errors = 0
word_types = ['плохое', 'хорошее']
for indx, word in enumerate(test_sample):
    received_word_type = detect(word)[1]
    if received_word_type != word_types[indx%2]:
        print(f'{word.upper()}\nОжидается тип: "{word_types[indx%2]}", Полученный тип: "{received_word_type}"\n')
        errors += 1

print("\nИтого ошибок:", errors, "Всего слов:", len(test_sample))
print("Точность: ", round((1 - errors / len(test_sample))*100), '%', sep='')
