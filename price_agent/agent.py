from dotenv import load_dotenv
import os
import streamlit as st
import sys

from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.messages import AIMessage, HumanMessage
from langchain.agents import create_agent

load_dotenv()

@tool
def price_finder_tool(product_name: str) -> str:
    """Finds the best price for a given product name."""
    # Simulate a more elegant price lookup with formatting and a fake store list
    stores = [
        {"name": "ExampleStore", "price": 99.99, "url": "https://examplestore.com"},
        {"name": "ShopNow", "price": 104.49, "url": "https://shopnow.com"},
        {"name": "BestBuy", "price": 102.00, "url": "https://bestbuy.com"},
    ]
    # Pick the store with the lowest price
    best = min(stores, key=lambda s: s["price"])
    other_stores = [s for s in stores if s != best]
    response = (
        f"💡 **Best price for '{product_name}':**\n"
        f"- **{best['name']}**: ${best['price']:.2f} ([link]({best['url']}))\n"
    )
    if other_stores:
        response += "\nOther offers:\n"
        for s in other_stores:
            response += f"- {s['name']}: ${s['price']:.2f} ([link]({s['url']}))\n"
    return response

llm = ChatOpenAI(
    model="gpt-4o",
    api_key=os.getenv("OPENAI_API_KEY"),
    temperature=0,
)

tools = [price_finder_tool]

SYSTEM_PROMPT = (
    "You are PriceAgent, an AI assistant that answers general questions and helps users find the best prices for products online. "
    "If the user asks for a product price, use the price_finder_tool. "
    "Be concise, friendly, and helpful."
)

agent = create_agent(
    model=llm,
    tools=tools,
    system_prompt=SYSTEM_PROMPT,
)

def run_agent(chat_history):
    """Run the agent with the given chat history and return the assistant's reply."""
    result = agent.invoke({"messages": chat_history})
    last_msg = result["messages"][-1]
    return last_msg.content

def render_chat():
    """Render the chat history in Streamlit's chat interface."""
    for msg in st.session_state.chat_history:
        role = "user" if isinstance(msg, HumanMessage) else "assistant"
        with st.chat_message(role):
            st.markdown(msg.content)

def main_streamlit():
    st.set_page_config(page_title="Price Finder Chat Agent", page_icon="💬")
    st.title("💬 PriceAgent: Your Price Finder Assistant")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    render_chat()

    user_input = st.chat_input("Ask anything (e.g., 'What's the price of iPhone 15?')")
    if user_input:
        st.session_state.chat_history.append(HumanMessage(content=user_input))
        with st.chat_message("user"):
            st.markdown(user_input)
        with st.spinner("PriceAgent is thinking..."):
            ai_text = run_agent(st.session_state.chat_history)
        ai_msg = AIMessage(content=ai_text)
        st.session_state.chat_history.append(ai_msg)
        with st.chat_message("assistant"):
            st.markdown(ai_msg.content)

if __name__ == "__main__":
    # Always launch Streamlit UI if running under Streamlit
    if hasattr(st, "_is_running_with_streamlit") and st._is_running_with_streamlit:
        main_streamlit()
    elif len(sys.argv) > 1 and sys.argv[1] == "web":
        main_streamlit()
    else:
        chat_history = []
        print("Welcome to PriceAgent! Type 'exit' to quit.")
        while True:
            user_input = input("You: ").strip()
            if user_input.lower() == "exit":
                print("Goodbye!")
                break
            chat_history.append(HumanMessage(content=user_input))
            ai_text = run_agent(chat_history)
            ai_msg = AIMessage(content=ai_text)
            chat_history.append(ai_msg)
            print("AI:", ai_msg.content)
