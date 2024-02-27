from stemmer import Porter
import pickle

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, Dense, SimpleRNN, LSTM, Dropout
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.callbacks import ModelCheckpoint

import numpy as np
import matplotlib.pyplot as plt


model_name = 'model_LSTM_SimpleRNN_test'


with open('data/training/bad_words.txt', 'r', encoding='utf-8') as f:
    bad_words = f.read().split()

with open('data/training/good_words.txt', 'r', encoding='utf-8') as f:
    good_words = f.read().split()





words = list(map(Porter.stem, set([i.strip() for i in (bad_words + good_words)])))
words = [i for i in set(words) if len(i) > 2]
num_characters = 34

tokenizer = Tokenizer(num_words=num_characters, lower=True, char_level=True)
tokenizer.fit_on_texts(words)

with open('data/tokenizers/tokenizer_test.pickle', 'wb') as handle:
    pickle.dump(tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)

data = tokenizer.texts_to_sequences(words)
inp_chars = 15


X = pad_sequences(data, maxlen=inp_chars)
Y = np.array([[0, 1]] * len(bad_words) + [[1, 0]] * len(good_words))

indeces = np.random.choice(X.shape[0], size=X.shape[0], replace=False)
X = X[indeces]
Y = Y[indeces]

x_test = ['*****', 'яблочко', '*****', 'каркуша', '*****',
         'уха', '*****', 'шалаш', '*****', 'шлюпка',
         '*****', 'мандарины', '*****', 'именины',
         '*****', 'юбилей', '*****', 'отбеливающее', '*****',
         'раглядка', '*****', 'гребля']
x_test = pad_sequences(tokenizer.texts_to_sequences(list(map(Porter.stem, x_test))), maxlen=inp_chars)
y_test = np.array([[0, 1] if i % 2 == 0 else [1, 0]
                   for i, _ in enumerate(x_test)])

model = Sequential()
model.add(Embedding(num_characters, 125, input_length=inp_chars))
model.add(LSTM(525, activation='tanh', return_sequences=True))
model.add(LSTM(525, activation='tanh', return_sequences=True))
model.add(SimpleRNN(225, activation='tanh'))
model.add(Dropout(0.2))
model.add(Dense(2, activation='softmax'))
model.summary()

model.compile(loss='categorical_crossentropy', metrics=['accuracy'], optimizer='adam')


checkpoint = ModelCheckpoint(f'models/{model_name}.h5', monitor='val_loss',
                             verbose=1, save_best_only=True, mode='min')
callbacks_list = [checkpoint]

history = model.fit(X, Y, batch_size=16, epochs=10, validation_split=0.05,
                    shuffle=True, callbacks=callbacks_list)


plt.plot([i for i in range(1, len(history.history['accuracy'])+1)],
            history.history['accuracy'],
            label='Доля верных ответов на обучающем наборе')
plt.plot([i for i in range(1, len(history.history['val_accuracy'])+1)],
            history.history['val_accuracy'],
            label='Доля верных ответов на проверочном наборе')
plt.xlabel('Эпоха обучения')
plt.ylabel('Доля верных ответов')
plt.legend()
plt.show()


scores = model.evaluate(x_test, y_test, verbose=1)

print("Доля верных ответов на тестовых данных, в процентах:",
      round(scores[1] * 100, 4))
