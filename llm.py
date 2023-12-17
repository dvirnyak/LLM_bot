from langchain.schema import HumanMessage, SystemMessage
from langchain.chat_models.gigachat import GigaChat

from config import gigachat, GIGACHAT_TOKEN



def llm_answer(user_id, request) -> str:
    messages = [
        SystemMessage(
            content="Ты администрация города Мирный, которая отвечает жителям на их вопросы по городу"
        )
    ]
    messages.append(HumanMessage(content=request))
    gigachat = GigaChat(credentials=GIGACHAT_TOKEN,
                        verify_ssl_certs=False)
    res = gigachat(messages)
    messages.append(res)
    print(res)

    return res.content