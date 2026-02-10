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
streamlit run news_agent/agent.py web
```

- The app will open in your browser (usually at [http://localhost:8501](http://localhost:8501)).
- Type your questions in the chat. If you ask for a product price, the agent will use the price finder tool.

### Command-line

You can also run the agent in the terminal:

```bash
python news_agent/agent.py
```

Type your questions and see responses in the console.

---

## How it Works

- The agent uses OpenAI's GPT-4o model via LangChain.
- When you ask for a product price, the LLM decides to invoke the `price_finder_tool`.
- The tool returns a simulated price, which the agent includes in its response.
- All conversation history is preserved and shown in the chat interface.

---

## File Structure

- `news_agent/agent.py` — Main agent code (web and CLI).
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
