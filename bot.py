# Импорт своих модулей
import shifr
from sorting import sort
from funcs.chance import set_chance
from funcs.border import set_border
from funcs.clear import clear_chat
from funcs.message import do_message
from funcs.citation import do_citation
from cleaning import cleaning
from funcs.help import help
from funcs.exist import chat_folder_create
from funcs.tracking import get_speech_ratio
from funcs.trckupdate import update_speech_ratio
from assessment.appraiser import appraise

# Импорт стандартных модулей
import re
import os
import json
import os.path
from random import random, randrange


class compile:
    def __init__(self, s):
        self.pattern = re.compile(s)

    def match(self, s):
        if self.pattern.match(s) is None:
            return self.pattern
        else:
            return self.pattern.match(s).group(0)


class Bot:
    def __init__(self, vk, longpoll):
        self.__version__ = "3.6.2"
        self.__author__ = "r3b0rn"

        self.vk = vk
        self.longpoll = longpoll

        self.mainPath = os.path.abspath(os.curdir)

    def launch(self, longpoll, VkBotEventType):
        # Основной цикл
        for event in longpoll.listen():
            # Очистка от старых баз
            cleaning(f"{self.mainPath}/data/")

            # Если пришло новое текстовое сообщение
            if (
                event.type == VkBotEventType.MESSAGE_NEW
                and event.object["message"]["text"]
                and event.from_chat
            ):

                self.eventHandling(event)

    def eventHandling(self, event):
        self.event = event

        # Назначение основных переменных бота
        self.randomID = round(random() * 10**9)
        self.chatID = int(event.chat_id)
        self.request = sort(event.object["message"]["text"])
        self.peerID = str(event.object["message"]["peer_id"])

        # Путь к хранилищу баз
        self.dataPath = f"{self.mainPath}/data/"

        self.chatPath = self.dataPath + self.peerID
        self.goodSentencesPath = self.chatPath + "/good_messages.txt"
        self.badSentencesPath = self.chatPath + "/bad_messages.txt"
        self.featurePath = self.chatPath + "/feature.json"

        self.threshold = 60

        self.isThereChat()

        with open(self.featurePath, encoding="utf8") as f:
            self.key = json.load(f)[0]["key"]

        self.percent = get_speech_ratio(self.vk, event, self.featurePath)

        self.set_path_for_user()
        action = self.distributeRequest()
        action()

    def distributeRequest(self):
        actions = {
            compile(r"\/chance\s\S+(\s*\S*)*").match(self.request): lambda: self.mail(
                set_chance(self.request, self.featurePath)),
            compile(r"\/border\s\S+(\s*\S*)*").match(self.request): lambda: self.mail(
                set_border(self.request, self.featurePath)),
            "/clear": lambda: self.mail(clear_chat(self.goodSentencesPath,
                                                   self.badSentencesPath,
                                                   self.featurePath)),
            "/message": lambda: self.mail(do_message(self.sentencesForUser,
                                                     self.key)),
            "/citation": lambda: self.mail(do_citation(self.sentencesForUser,
                                                       self.featurePath,
                                                       self.key)),
            "/help": lambda: self.mail(help())}

        return actions.get(self.request, self.reply)

    def isThereChat(self):
        # Проверка на наличие беседы в базе
        if os.path.exists(self.chatPath) is False:  # Если беседа новая
            # Загрузка файлов в новую папку
            chat_folder_create(
                self.goodSentencesPath,
                self.badSentencesPath,
                self.chatPath,
                self.featurePath)

    def reply(self):
        self.statisticsUpdate()

        # Считывание длины всех баз
        with open(self.goodSentencesPath) as g:
            goodMessagesNumber = len(g.readlines())
        with open(self.badSentencesPath) as b:
            badMessagesNumber = len(b.readlines())
        dataSize = goodMessagesNumber + badMessagesNumber

        with open(self.featurePath, encoding="utf8") as s:
            setings = json.load(s)
        chance = setings[0]["chance"]
        maximal_lines = setings[0]["maximal_lines"]

        # Проверка на возможность отправки сообщения
        if int(dataSize) >= int(maximal_lines) and randrange(1, 101) <= chance:

            self.set_path_for_user()
            # Отправка сообщения
            self.mail(do_message(self.sentencesForUser, self.key))

    # Функция отправки сообщений
    def mail(self, message):
        self.vk.messages.send(
            random_id=self.randomID, chat_id=self.chatID, message=message)

    def set_path_for_user(self):
        if self.percent >= self.threshold:
            self.sentencesForUser = self.goodSentencesPath
        else:
            self.sentencesForUser = self.badSentencesPath

    def statisticsUpdate(self):
        # Определение качества предложения
        quality = appraise(re.sub(r"\W+", " ", self.request))
        # Запись обновленной статистики в базу
        update_speech_ratio(self.vk, self.event, self.featurePath, quality)
        self.percent = get_speech_ratio(self.vk, self.event, self.featurePath)

        if self.request.strip() != "":
            if quality == 1:
                path = self.goodSentencesPath
            else:
                path = self.badSentencesPath
            # Запись в соответствующую базу
            with open(path, "a") as messages:
                self.request = shifr.encode(self.key, self.request)
                messages.write(f"{self.request}\n")
