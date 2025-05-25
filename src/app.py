import os
import chainlit as cl # type: ignore
from agents.tool import function_tool # type: ignore
from openai.types.responses import ResponseTextDeltaEvent # type: ignore 
from agents import Agent, RunConfig, Runner, AsyncOpenAI, OpenAIChatCompletionsModel # type: ignore 
from tavily import TavilyClient # type: ignore

from dotenv import load_dotenv, find_dotenv # type: ignore

# Fetching Api key from .env file
gemini_api_key = os.getenv("GEMINI_API_KEY")
search_key =  os.getenv("TAVILY_API_KEY")

load_dotenv(find_dotenv())

# Tool Making
@function_tool("search_online") # type: ignore
def search_online(query: str) -> str:
    """Search the web for answering the given question"""
    search_client = TavilyClient(api_key= search_key) # type: ignore
    result = search_client.search(query)
    return result


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
    model_provider=provider, # type: ignore
    tracing_disabled=True,
)
# Step 4:Making Agent
agent1 = Agent(
    name="Senior Health Assitant" ,
    instructions="You are a helpful health assistant. Your name is bib .You are developed by Muhammad Anas Asif . He is Agentic Ai and Cloud first developer. ", 
    tools=[search_online],
)

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