import chainlit as cl 
import os
from agents import Agent, RunConfig, Runner, AsyncOpenAI, OpenAIChatCompletionsModel 
from dotenv import load_dotenv, find_dotenv

# Fetching Api key from .env file
gemini_api_key = os.getenv("GEMINI_API_KEY")

load_dotenv(find_dotenv())

# Step 1 : Provider
provider = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# Step 2: model 
model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=provider,

)

# Step 3: Configration At Run Level
run_config = RunConfig(
    model=model,
    model_provider = provider,
    tracing_disabled=True,
)

# Step 4:Making Agent
agent1 = Agent(
    instructions="You are a helpful assistant.", 
    name="Senior Assitant" 
)

# Step 5: Run Agent
# result= Runner.run_sync(
# agent1,
#     input="Who is Founder of PIA?",
#     run_config= run_config,
# )

# print(result.final_output)

@cl.on_chat_start
async def handel_start_chat():
    cl.user_session.set("history",[])
    await cl.Message(content="Hello, I am a helpful assistant. How can I help you today?").send()


@cl.on_message
async def handel_message(message: cl.Message):
    history = cl.user_session.get("history")
    history.append({"role":"user","content":message.content})
    cl.user_session.set("history",history)
    result= Runner.run_sync(
        agent1,
        input=history,
        run_config= run_config,
    )
    history.append({"role":"assistant","content":result.final_output})
    cl.user_session.set("history",history)
    await cl.Message(content=result.final_output).send()

# @cl.on_chat_start
# async def handel_start_chat():
#     cl.user_session.set("history",[])
#     await cl.Message

 
# @cl.on_message
# async def main(message: cl.Message):
#     result= Runner.run_sync(
#     agent1,
#         input=message.content,
#         run_config= run_config,
#     )
#     await cl.Message(
#         content=result.final_output).send()