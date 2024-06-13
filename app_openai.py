import chainlit as cl
from openai import AsyncOpenAI

client = AsyncOpenAI()

settings = {
    "model": "gpt-3.5-turbo",
    "temperature": 0
}

@cl.on_message
async def main(message: cl.Message):
    # Your custom logic goes here...
    response = await client.chat.completions.create(
        messages=[
            {
                "content": "You are a helpful bot, you always reply in Indonesian",
                "role": "system"
            },
            {
                "content": message.content,
                "role": "user"
            }
        ],
        **settings
    )

    # Send a repsonse back to the user
    await cl.Message(
        # content=f"Received: {message.content}",
        content=response.choices[0].message.content
    ).send()
