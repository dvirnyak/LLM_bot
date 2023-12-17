from config import vk
import random
from llm import llm_answer

def write_msg(user_id, message):
    vk.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': random.randint(1, 1e18)})

def msg_handler(user_id, request):
    # Каменная логика ответа
    answer = llm_answer(user_id, request)
    write_msg(user_id, answer)
