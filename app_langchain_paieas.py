from langchain_community.chat_models.pai_eas_endpoint import PaiEasChatEndpoint
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import Runnable
from langchain_core.runnables.config import RunnableConfig

import chainlit as cl

import os

@cl.on_chat_start
async def on_chat_start():
    model = PaiEasChatEndpoint(
        eas_service_token=os.environ['EAS_SERVICE_TOKEN'],
        eas_service_url=os.environ['EAS_SERVICE_URL'],
        temperature=0.1,
        top_p=0.7,
        top_k=50,
        max_new_tokens=512,
        streaming=True
    )
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "You're a very skilled Python developer who provides accurate and eloquent answers to Python programming questions."),
            ("human", "{question}")
        ]
    )
    runnable = prompt | model | StrOutputParser()
    cl.user_session.set("runnable", runnable)

@cl.on_message
async def on_message(message: cl.Message):
    runnable = cl.user_session.get("runnable")
    cb = cl.LangchainCallbackHandler()
    config = RunnableConfig(callbacks=[cb])

    # msg = cl.Message(content="")

    response = await runnable.ainvoke({'question': message.content}, config=config)

    await cl.Message(
        content=response
    ).send()
