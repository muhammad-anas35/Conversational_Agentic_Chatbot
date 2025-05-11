import os
import chainlit as cl 
from openai.types.responses import ResponseTextDeltaEvent
from agents import Agent, RunConfig, Runner, AsyncOpenAI, OpenAIChatCompletionsModel 

from dotenv import load_dotenv, find_dotenv

# Fetching Api key from .env file
gemini_api_key = os.getenv("GEMINI_API_KEY")

load_dotenv(find_dotenv())

# Step 1 : Set Provider
provider = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# Step 2: Set model 
model = OpenAIChatCompletionsModel(
        model="gemini-2.0-flash",
        openai_client=provider,

)

# Step 3: Configration At Run Level
run_config = RunConfig(
    model=model,
    model_provider=provider,
    tracing_disabled=True,
)

# agent1 = Agent(
#         instructions="You are a helpful assistant.", 
#         name="Senior Assitant" 
#     )

# Step 4:Making Agent
agent1 = Agent(
    instructions="You are a helpful health assistant. Your name is bib .You are developed by devloper whose name is MUhammad Anas . He is Agentic first and cloud first developer. ", 
    name="Senior Health Assitant" 
)

# Step 5: Run Agent
# result= Runner.run_sync(
#     agent1,
#         input="Who is Founder of PIA?",
#         run_config= run_config,
# )

# print(result.final_output)



@cl.on_chat_start
async def handel_start_chat():
    cl.user_session.set("history",[])
    await cl.Message(content="Hello, I am a helpful health assistant. How can I help you today?").send()

#  With Stream

@cl.on_message
async def handel_message(message: cl.Message):
    history = cl.user_session.get("history")

    #  Initialize a message object
    msg = cl.Message(content="")
    await msg.send()

    history.append({"role":"user","content":message.content})
    cl.user_session.set("history",history)

    result= Runner.run_streamed(
        agent1,
        input=history,
        run_config= run_config,
    )

    async for event in result.stream_events():
        if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
            token = event.data.delta
            await msg.stream_token(token)

    history.append({"role":"assistant","content":result.final_output})
    cl.user_session.set("history",history)

    # await cl.Message(content=result.final_output).send()

# async def main():
#     agent=Agent(
#         name="Senior Assitant" ,
#         instructions="You are a helpful assistant."
#     )

#     result= Runner.run_streamed(
#         agent1,
#         input="Tell me 5 joke",
#          run_config= run_config,
#     )
#     async for event in result.stream_events():
#         if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
#             print(event.data.delta,end="",flush=True)
# asyncio.run(main())