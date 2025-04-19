# This Is conversational Agent With Chainlit Integration 
- Firts Practice of **Openai_Agents_SDK** with **Chainlit**.

# Pourpose 
- To Understand and practice the code .

# Step to Make
## Setup
1. Import all Function
2. Get Key from .env file 
## Agents Making
1. Set Provider
```Python
    provider = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)
```
2. Set Model 
```Python
    model = OpenAIChatCompletionsModel(
        model="gemini-2.0-flash",
        openai_client=provider,

    )
```
3. Configration
- Configration also have 3 type .
- Run Level 
- Direct to Agent
- Global  
4. Making Agent 
```Python
    agent1 = Agent(
        instructions="You are a helpful assistant.", 
        name="Senior Assitant" 
    )
```
5. Run Agents
```Python
    result= Runner.run_sync(
    agent1,
        input="Who is Founder of PIA?",
        run_config= run_config,
    )
```

## Last. **Integrate With chainlit**
- Follow ME on Linkdin: [Fiverr](https://www.fiverr.com/s/991k68A)
- Follow ME on Linkdin: [Linkedin](https://www.linkedin.com/in/muhammad-anas35)