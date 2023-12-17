import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from config import vk
from msg_handler import msg_handler

def bot():

    longpoll = VkLongPoll(vk)

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            if event.to_me:
                msg_handler(event.user_id, event.text)

if __name__ == "__main__":
    bot()