from agents import Agent,Runner,AsyncOpenAI,function_tool,set_tracing_disabled ,set_default_openai_api,set_default_openai_client
from openai.types.responses import ResponseTextDeltaEvent 
from tavily import TavilyClient  # type: ignore
import chainlit as cl 
from dotenv import load_dotenv, find_dotenv 
import os

# Fetching Api key from .env file
load_dotenv(find_dotenv())

# Configrations
set_tracing_disabled(disabled=True)
set_default_openai_api("chat_completions")

gemini_api_key = os.getenv("GEMINI_API_KEY")
search_key =  os.getenv("TAVILY_API_KEY")


# Tool Making
@function_tool
def search_online(query: str) -> str:
    """Search the web for answering the given question"""
    print("Searcing from the web...")
    search_client = TavilyClient(api_key= search_key) 
    result = search_client.search(query)
    return result

# # Step 1 : Set Provider
External_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)
set_default_openai_client(External_client)

# Step 2:Making Agent
Main_Agent :Agent= Agent(
    name="Senior Health Assitant" ,
    instructions="You are a helpful health assistant. Your name is Bib_Ai .You are developed by Muhammad Anas Asif . He is Agentic Ai and Cloud first developer. ", 
    model="gemini-2.5-flash-preview-05-20",
    tools=[search_online],
)

@cl.on_chat_start
async def handel_start_chat():
    cl.user_session.set("history",[])
    await cl.Message(content="Hi, I am a helpful health assistant. How can I help you today?").send()

#  With Stream

@cl.on_message
async def handel_message(message: cl.Message):
    history = cl.user_session.get("history")

    #  Initialize a message object
    msg = cl.Message(content="")
    await msg.send()

    history.append({"role":"user","content":message.content})
    cl.user_session.set("history",history)

    result=Runner.run_streamed(
        Main_Agent,
        input=history,
    )

    async for event in result.stream_events():
        if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
            token = event.data.delta
            await msg.stream_token(token)

    history.append({"role":"assistant","content":result.final_output})
    cl.user_session.set("history",history)

    # await cl.Message(content=result.final_output).send()