# Импорт модулей ВК + модификации
import vk_api
from vk_api.bot_longpoll import VkBotEventType
from mylongpoll import MyVkBotLongPoll

# Импорт своих модулей
from bot import Bot


# API-ключ и id сообщества
with open("token_and_group.txt") as f:
    token = f.readline().strip()
    group_id = f.readline().strip()

# Авторизация от имени сообщества
vk_session = vk_api.VkApi(token=token)
vk_session._auth_token()

# Работа с сообщениями
longpoll = MyVkBotLongPoll(vk_session, group_id)
vk = vk_session.get_api()

b = Bot(vk, longpoll)
b.launch(longpoll, VkBotEventType)
