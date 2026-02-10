# Price Finder Chat Agent

This project is an interactive AI chat agent that can answer general questions and, when asked about product prices, will use a tool to fetch (simulated) price information. It uses [LangChain](https://python.langchain.com/), [OpenAI GPT-4o](https://platform.openai.com/docs/models/gpt-4o), and [Streamlit](https://streamlit.io/) for a web-based chat interface.

---

## Features

- **Conversational AI:** Ask anything, get helpful answers.
- **Price Finder Tool:** When you ask for a product price, the agent uses a tool to fetch the best price.
- **Web Chat UI:** Interactive chat interface in your browser.
- **Command-line Mode:** Optional CLI chat if not run via Streamlit.

---

## Setup

1. **Clone the repository** (if needed):

   ```bash
   git clone <your-repo-url>
   cd hmz-learning-project
   ```

2. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Set your OpenAI API key:**

   Create a `.env` file in the project root with:

   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```

---

## Usage

### Web (Recommended)

Start the Streamlit app:

```bash
streamlit run price_agent/agent.py web
```

- The app will open in your browser (usually at [http://localhost:8501](http://localhost:8501)).
- Type your questions in the chat. If you ask for a product price, the agent will use the price finder tool.

### Command-line

You can also run the agent in the terminal:

```bash
python price_agent/agent.py
```

Type your questions and see responses in the console.

---

## How it Works

- The agent uses OpenAI's GPT-4o model via LangChain.
- When you ask for a product price, the LLM decides to invoke the `price_finder_tool`.
- The tool returns a simulated price, which the agent includes in its response.
- All conversation history is preserved and shown in the chat interface.

---

## How LangChain Works in `agent.py`

The core logic of this project is built using [LangChain](https://python.langchain.com/), which provides abstractions for LLMs, tools, and agent orchestration. Here’s how it works in `price_agent/agent.py`:

- **LLM Setup:**  
  The agent uses OpenAI's GPT-4o model via the `ChatOpenAI` wrapper from LangChain.

- **Tool Definition:**  
  The `@tool` decorator from LangChain is used to define `price_finder_tool`, which simulates fetching product prices from multiple stores.

- **Agent Creation:**  
  The agent is created using `create_agent`, which combines the LLM, the list of tools, and a system prompt. The system prompt instructs the agent to use the price finder tool when appropriate.

- **Conversation Handling:**  
  - In the web UI (Streamlit), user messages and AI responses are stored in a chat history.
  - Each time the user sends a message, the full chat history is passed to the agent.
  - The agent decides, based on the user's input and the system prompt, whether to answer directly or invoke the price finder tool.
  - If the tool is invoked, its output is included in the AI's response.

- **Streaming and Display:**  
  - The Streamlit interface displays the conversation interactively.
  - The command-line interface works similarly, printing messages to the console.

**Summary:**  
LangChain enables the agent to combine LLM reasoning with tool use, so the AI can both chat naturally and call external functions (like price lookup) when needed—all orchestrated in a single, unified workflow.

---

## Using Azure OpenAI Instead of OpenAI

If you want to use [Azure OpenAI Service](https://learn.microsoft.com/en-us/azure/ai-services/openai/overview) instead of OpenAI, follow these steps:

1. **Install the Azure OpenAI LangChain integration:**

   ```bash
   pip install langchain-azure-openai
   ```

2. **Update the import and LLM setup in `price_agent/agent.py`:**

   Replace:
   ```python
   from langchain_openai import ChatOpenAI
   ```

   With:
   ```python
   from langchain_azure_openai import AzureChatOpenAI
   ```

   And update the LLM initialization:
   ```python
   llm = AzureChatOpenAI(
       openai_api_version="2023-05-15",  # or your Azure OpenAI API version
       azure_deployment="your-deployment-name",
       azure_endpoint="https://your-resource-name.openai.azure.com/",
       api_key=os.getenv("AZURE_OPENAI_API_KEY"),
       temperature=0,
   )
   ```

3. **Set your Azure OpenAI credentials in `.env`:**

   ```
   AZURE_OPENAI_API_KEY=your_azure_openai_api_key
   ```

   Optionally, you can also set `AZURE_OPENAI_ENDPOINT` and `AZURE_OPENAI_DEPLOYMENT` as environment variables and reference them in your code.

4. **Restart your app.**

**Note:**  
- The rest of the code and usage remains the same.
- Make sure your Azure deployment and model names match your Azure OpenAI setup.

---

## File Structure

- `price_agent/agent.py` — Main agent code (web and CLI).
- `requirements.txt` — Python dependencies.
- `.env` — Your OpenAI API key (not included in version control).

---

## Customization

- **Add more tools:** Define new `@tool` functions and add them to the `tools` list.
- **Change the model:** Adjust the `model` parameter in `ChatOpenAI`.
- **Improve the price finder:** Replace the placeholder logic in `price_finder_tool` with real API calls.

---

## License

MIT License (or your chosen license).

---
