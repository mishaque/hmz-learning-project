from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm
from dotenv import load_dotenv
import os

load_dotenv()   

def price_finder_tool(product_name: str) -> str:
    # Placeholder function to simulate price finding
    return f"The best price for {product_name} is $99.99 from ExampleStore."

# --- Example Agent using OpenAI's GPT-4o ---
# (Requires OPENAI_API_KEY)
agent_openai = LlmAgent(
    model=LiteLlm(model="openai/gpt-4o"), # LiteLLM model string format
    name="hmz_price_finder_openai",
    instruction="You are an AI agent that helps find best prices for products online.",
    tools=[
        # Define tools here, e.g., web search, price comparison APIs
        price_finder_tool,
    ]
)

root_agent = agent_openai