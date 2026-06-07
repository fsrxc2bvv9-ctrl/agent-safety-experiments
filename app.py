from smolagents import CodeAgent, InferenceClientModel, tool


@tool
def get_weather(location: str) -> str:
    """Return fake weather for a given location.

    Args:
        location: City or location name.
    """
    return f"The weather in {location} is sunny and 22°C."


model = InferenceClientModel(
    model_id="Qwen/Qwen2.5-Coder-32B-Instruct"
)

agent = CodeAgent(
    tools=[get_weather],
    model=model,
    max_steps=4
)

result = agent.run("What is the weather in London?")

print("\nFINAL RESULT:")
print(result)
