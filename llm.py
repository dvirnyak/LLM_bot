import json

from langchain.schema import HumanMessage, SystemMessage
from langchain.chat_models.gigachat import GigaChat

from config import gigachat, GIGACHAT_TOKEN, Session
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from docarray import BaseDoc
from docarray.typing import NdArray
from langchain.embeddings import GPT4AllEmbeddings
from langchain.retrievers import DocArrayRetriever
from models import *

embeddings = GPT4AllEmbeddings()

class MyDoc(BaseDoc):
    text: str
    text_embedding: NdArray[384]


from docarray.index import InMemoryExactNNIndex

# initialize the index
def create_retriever():
    db = InMemoryExactNNIndex[MyDoc]()
    session = Session()
    documents = session.query(Document).all()
    docs_for_retriever = []
    for document in documents:
        text_embedding = json.loads(document.text_embedding)
        doc = MyDoc(text=document.text, text_embedding=text_embedding)
        docs_for_retriever.append(doc)

    db.index(docs_for_retriever)
    retriever = DocArrayRetriever(
        index = db,
        embeddings = embeddings,
        search_field = "text_embedding",
        content_field = "text")

    return retriever


def llm_answer(user_id, messages, request) -> str:
    if messages is None or len(messages) == 0:
        messages = [
            SystemMessage(
                content="Ты администрация города Мирный, которая отвечает жителям на их вопросы по городу."
                        "Следующие запросы будут от жителя. Отвечай развёрнуто"
            )
        ]
    messages.append(HumanMessage(content=request))
    gigachat = GigaChat(credentials=GIGACHAT_TOKEN,
                        verify_ssl_certs=False)

    retriever = create_retriever()

    qa = ConversationalRetrievalChain.from_llm(gigachat, retriever=retriever)

    res = gigachat(messages)
    messages.append(res)
    print(res)

    return res.content