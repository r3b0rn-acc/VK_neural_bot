import os
import shutil
import time
from datetime import datetime
import os.path


# Функция очистки от залежавшихся баз данных
def cleaning(folder):
    # Цикл для сканирования баз
    for num in os.listdir(folder):
        featurePath = str(folder) + str(num) + str("/feature.json")

        # Дата в данный момент
        now = " ".join(time.ctime().split()[1:])
        now = datetime.strptime(now, "%b %d %H:%M:%S %Y")

        # Даты последнего изменения файла
        dateOfChangeFile = " ".join(
            time.ctime(os.path.getmtime(featurePath)).split()[1:])
        dateOfChangeFile = datetime.strptime(dateOfChangeFile,
                                             "%b %d %H:%M:%S %Y")

        path = str(folder) + str(num)
        if (now - dateOfChangeFile).days > 30:
            shutil.rmtree(path, ignore_errors=True)
