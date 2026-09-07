# LangChain Q&A Chatbot

A conversational Q&A web app built with LangChain, Groq and Streamlit.
Runs entirely on free-tier services -- no credit card required at any step.

**Live demo:** _PASTE YOUR HUGGING FACE SPACE LINK HERE AFTER DEPLOYING_
`https://huggingface.co/spaces/YOUR_USERNAME/langchain-qa-chatbot`
```

---

## Features

- Conversational chat with full message history kept across turns
- Switchable models (Llama 3.3 70B for quality, Llama 3.1 8B for speed)
- Four assistant personas driven by swappable system prompts
- Temperature slider to control creativity at runtime
- Built with LangChain Expression Language (LCEL) pipelines
- API credentials handled via environment variables and deployment secrets

---

## Tech stack

| Layer | Tool |
|---|---|
| Language | Python 3.10+ |
| LLM framework | LangChain (LCEL) |
| Model provider | Groq (free tier) |
| Model | Llama 3.3 70B / Llama 3.1 8B |
| Frontend | Streamlit |
| Deployment | Hugging Face Spaces (free CPU tier) |

---

## Project structure

```
langchain-qa-chatbot/
├── app.py                  # Main app (chat history, model picker, personas)
├── app_simple.py           # Minimal version -- build this first to test setup
├── langchain_basics.ipynb  # 6 learning experiments explaining each concept
├── requirements.txt        # Pinned dependencies
├── .env                    # YOUR API KEY GOES HERE (never committed)
├── .env.example            # Safe template for other people
├── .gitignore              # Keeps .env and venv out of Git
└── README.md
```

---

## Setup

### 1. Clone and enter the folder

```bash
git clone https://github.com/YOUR_USERNAME/langchain-qa-chatbot.git
cd langchain-qa-chatbot
```

### 2. Create and activate a virtual environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

You should now see `(venv)` at the start of your terminal line.

### 3. Install dependencies

**Windows:**
```bash
pip install -r requirements.txt
```

**macOS / Linux:**
```bash
pip3 install -r requirements.txt
```

### 4. Add your API key

Get a free key at [console.groq.com](https://console.groq.com) -- sign up,
then **API Keys** -> **Create API Key**. No credit card is requested.

Open the `.env` file and replace the placeholder:

```
GROQ_API_KEY=gsk_your_actual_key_here
```

No spaces around the `=`, no quotation marks.

### 5. Run it

```bash
streamlit run app.py
```

Your browser opens at `http://localhost:8501`.

> Do **not** run `python app.py` -- Streamlit apps must be started with
> `streamlit run`, or you get a wall of warnings and a blank page.

---

## Deploying free on Hugging Face Spaces

1. Sign up at [huggingface.co](https://huggingface.co)
2. Profile picture -> **New Space**
3. Name it, choose SDK = **Streamlit**, hardware = **CPU basic (FREE)**, visibility = **Public**
4. Go to **Settings** -> **Variables and secrets** -> **New secret**
   - Name: `GROQ_API_KEY` (exactly this -- capitals and underscores)
   - Value: your Groq key
5. **Files** tab -> **Add file** -> **Upload files** -> upload `app.py` and `requirements.txt` only
6. Wait 3-8 minutes for the first build, then open the **App** tab

> Free Spaces sleep after 48 hours with no visitors and take ~30 seconds to
> wake up. Nothing breaks; just open the link a few minutes before showing it
> to anyone.

---

## Switching to a different free provider

LangChain wraps every provider behind the same interface, so changing the
entire AI backend is a two-line change.

**To Google Gemini:**

1. Get a free key at [aistudio.google.com](https://aistudio.google.com)
2. Add `langchain-google-genai==2.1.12` to `requirements.txt` and reinstall
3. Put `GOOGLE_API_KEY=your_key` in `.env`
4. In `app.py`, change:

```python
# from:
from langchain_groq import ChatGroq
llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=temperature)

# to:
from langchain_google_genai import ChatGoogleGenerativeAI
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=temperature)
```

Every other line -- prompts, chains, parsers, all the Streamlit code --
stays exactly the same.

---

## Troubleshooting

| Error | Fix |
|---|---|
| `ModuleNotFoundError: No module named 'langchain_groq'` | Virtual environment not activated. Check for `(venv)` in your terminal. |
| `GROQ_API_KEY not found` | Check `.env` is named exactly `.env`, has no spaces around `=`, and is saved. |
| `AuthenticationError` / `Invalid API Key` | Key is wrong or has a stray space. Create a fresh one in the Groq console. |
| `NotFoundError: model does not exist` | Groq retired that model. Get a current ID from [console.groq.com/docs/models](https://console.groq.com/docs/models) and replace it in `AVAILABLE_MODELS`. |
| `RateLimitError` / `429` | Wait 60 seconds, or switch to `llama-3.1-8b-instant`. |
| `running scripts is disabled on this system` | Windows PowerShell. Switch your VS Code terminal to Command Prompt. |
| `Port 8501 is already in use` | An old app is running. Press `Ctrl+C` in that terminal, or use `streamlit run app.py --server.port 8502`. |
| Deployed app errors on every question | The Space secret is misspelled. It must be `GROQ_API_KEY`. |

---

## What I'd add next

- RAG over uploaded PDFs, so the bot answers from a specific document
  rather than only from the model's training data
- Streaming responses with `st.write_stream()` for word-by-word output
- Response caching to reduce repeat API calls

---

## License

MIT
