from vk_api.bot_longpoll import VkBotLongPoll
from datetime import datetime


# Модернизация лонгпула
class MyVkBotLongPoll(VkBotLongPoll):
    def err(self, e):
        error_time = "".join(str(datetime.now().time()).split(".")[0])
        print("Longpoll Error (VK): ", e, "\n", error_time, "\n")

    def listen(self):
        while True:
            try:
                for event in self.check():
                    yield event
            # Перехват ошибок и корректный вывод в консоль
            except Exception as e:
                self.err(e)
