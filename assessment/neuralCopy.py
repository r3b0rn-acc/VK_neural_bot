from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Embedding, Flatten, Dropout
from tensorflow.keras.callbacks import ModelCheckpoint
from tensorflow.keras.models import load_model
import matplotlib.pyplot as plt
import numpy as np
import csv


class Neural:
    def __init__(self, data_path="datasets/dataset.csv", max_length=15,
                 batch_size=64, epochs=8):
        # Максимальный размер входных данных
        self.max_length = max_length
        # Меньше --> дольше
        self.batch_size = batch_size
        # Больше --> дольше
        self.epochs = epochs
        # Пути к данным
        self.data_path = data_path

        self.max_token_id = 8581

    def read_dataset(self):
        with open(self.data_path) as f:
            reader = csv.reader(f)
            dataset_rows_total_num = len(list(reader)) - 1

        x_train = []
        x_test = []

        y_train = []
        y_test = []

        with open(self.data_path) as f:
            reader = csv.DictReader(f)
            row_number = 1
            for row in reader:
                if row_number <= dataset_rows_total_num // 10:
                    x_test.append(list(map(int, row["sentence"].split("_"))))
                    y_test.append(int(row["grade"]))
                else:
                    x_train.append(list(map(int, row["sentence"].split("_"))))
                    y_train.append(int(row["grade"]))
                row_number += 1

        self.x_train = np.array(x_train)
        self.x_test = np.array(x_test)

        self.y_train = np.array(y_train).reshape((-1, 1))
        self.y_test = np.array(y_test).reshape((-1, 1))

    def model_trainig(self):
        self.read_dataset()

        # Создание модели плотного векторного представления
        model = Sequential()
        model.add(Embedding(self.max_token_id + 1, 2,
                            input_length=self.max_length))
        model.add(Dense(64, activation='elu'))
        model.add(Dense(32, activation='elu'))
        model.add(Dropout(0.25))
        model.add(Dense(8, activation='elu'))
        model.add(Flatten())
        model.add(Dense(1, activation='sigmoid'))

        # Компиляция модели
        model.compile(optimizer="adam",
                      loss="binary_crossentropy",
                      metrics=['accuracy'])

        # Запись модели в файл
        filepath = "network/Copyspeecher_dense_test.h5"
        checkpoint = ModelCheckpoint(filepath, monitor='val_loss', verbose=1,
                                     save_best_only=True, mode='min')
        callbacks_list = [checkpoint]

        # Обучение модели
        history = model.fit(self.x_train,
                            self.y_train,
                            epochs=self.epochs,
                            batch_size=self.batch_size,
                            validation_split=0.05,
                            callbacks=callbacks_list)

        # График обучения модели
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

        model = load_model(filepath)

        # Проверка модели на тестовых данных
        scores = model.evaluate(self.x_test, self.y_test, verbose=1)

        print("Доля верных ответов на тестовых данных, в процентах:",
              round(scores[1] * 100, 4))


n = Neural()
n.model_trainig()
