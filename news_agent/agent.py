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
    return f"The best price for {product_name} is $99.99 from ExampleStore."

llm = ChatOpenAI(
    model="gpt-4o",
    api_key=os.getenv("OPENAI_API_KEY"),
    temperature=0,
)

tools = [price_finder_tool]

agent = create_agent(
    model=llm,  # (some installs also accept model="gpt-4.1" style strings)
    tools=tools,
    system_prompt=(
        "You are an AI assistant. If the user asks for a product price, "
        "use the price_finder_tool. Otherwise, answer normally."
    ),
)

def run_agent(chat_history):
    # chat_history is a list of langchain_core.messages (HumanMessage/AIMessage)
    result = agent.invoke({"messages": chat_history})
    # create_agent returns a result containing messages; last one is the assistant response
    last_msg = result["messages"][-1]
    return last_msg.content

def main_streamlit():
    st.title("Price Finder Chat Agent")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Display chat history as an interactive conversation
    for msg in st.session_state.chat_history:
        if isinstance(msg, HumanMessage):
            with st.chat_message("user"):
                st.markdown(msg.content)
        else:
            with st.chat_message("assistant"):
                st.markdown(msg.content)

    user_input = st.chat_input("Ask me anything...")
    if user_input:
        # Show user message immediately
        st.session_state.chat_history.append(HumanMessage(content=user_input))
        with st.chat_message("user"):
            st.markdown(user_input)
        with st.spinner("Thinking..."):
            ai_text = run_agent(st.session_state.chat_history)
        ai_msg = AIMessage(content=ai_text)
        st.session_state.chat_history.append(ai_msg)
        with st.chat_message("assistant"):
            st.markdown(ai_msg.content)

if __name__ == "__main__":
    # Detect if running under Streamlit and always launch the web interface
    if hasattr(st, "_is_running_with_streamlit") and st._is_running_with_streamlit:
        main_streamlit()
    elif len(sys.argv) > 1 and sys.argv[1] == "web":
        main_streamlit()
    else:
        chat_history = []
        print("Type 'exit' to quit.")
        while True:
            user_input = input("You: ").strip()
            if user_input.lower() == "exit":
                break
            chat_history.append(HumanMessage(content=user_input))
            ai_text = run_agent(chat_history)
            ai_msg = AIMessage(content=ai_text)
            chat_history.append(ai_msg)
            print("AI:", ai_msg.content)
