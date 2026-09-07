"""
LangChain Q&A Chatbot
---------------------
A conversational Q&A web app built with LangChain, Groq and Streamlit.

Run locally with:      streamlit run app.py
(NOT with: python app.py  -- that will not work)

API KEY:
    You do NOT put your API key in this file.
    - Locally:  put it in the .env file  (see .env in this folder)
    - Deployed: add it as a secret named GROQ_API_KEY in your
                Hugging Face Space -> Settings -> Variables and secrets
"""

import streamlit as st
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage, AIMessage


# ---------------------------------------------------------------------
# 1. LOAD THE API KEY
# ---------------------------------------------------------------------
# Locally this reads the .env file sitting next to this script.
# On Hugging Face there is no .env file, so this line quietly does nothing
# and the key is picked up from the Space secret instead. Both paths work,
# which is why there is no if/else here.
load_dotenv()


# ---------------------------------------------------------------------
# 2. CONFIGURATION
# ---------------------------------------------------------------------
# If a model name ever stops working, get a current one from
# https://console.groq.com/docs/models and replace it here.
AVAILABLE_MODELS = {
    "GPT-OSS 120B (best quality)": "openai/gpt-oss-120b",
    "GPT-OSS 20B (fastest)": "openai/gpt-oss-20b",
}

PERSONAS = {
    "Helpful Assistant": (
        "You are a knowledgeable and friendly assistant. Answer the user's "
        "question clearly and accurately. If you do not know something, say "
        "so plainly instead of guessing."
    ),
    "Patient Tutor": (
        "You are a patient tutor for a college student. Explain concepts from "
        "first principles using simple language and a concrete example. Do not "
        "assume prior knowledge. Keep answers under 200 words."
    ),
    "Code Reviewer": (
        "You are an experienced software engineer reviewing code. Point out "
        "bugs, edge cases and readability problems. Be direct and specific. "
        "Show the corrected code in a fenced code block."
    ),
    "Interview Coach": (
        "You are a technical interview coach. Answer as if teaching the user "
        "how to answer this in an interview: give a crisp 30-second answer "
        "first, then the deeper detail an interviewer might probe for."
    ),
}


# ---------------------------------------------------------------------
# 3. BUILD THE CHAIN
# ---------------------------------------------------------------------
# @st.cache_resource makes Streamlit build this once and reuse it.
# Without it, a new model object would be created on every single click,
# because Streamlit re-runs this whole file top to bottom each interaction.
@st.cache_resource
def build_chain(model_name: str, temperature: float, system_prompt: str):
    """Create the prompt -> model -> parser pipeline."""
    llm = ChatGroq(
        model=model_name,
        temperature=temperature,
    )

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{question}"),
    ])

    # The pipe operator (LCEL) reads left to right:
    # take the prompt, feed it to the model, feed that to the parser.
    return prompt | llm | StrOutputParser()


def get_response(question: str, history: list, model_name: str,
                 temperature: float, system_prompt: str) -> str:
    """Send one question through the chain and return the answer text."""
    chain = build_chain(model_name, temperature, system_prompt)
    return chain.invoke({"question": question, "history": history})


# ---------------------------------------------------------------------
# 4. PAGE SETUP
# ---------------------------------------------------------------------
# set_page_config must be the first Streamlit command that runs.
st.set_page_config(
    page_title="LangChain Q&A Chatbot",
    page_icon="::",
    layout="centered",
)

st.title("LangChain Q&A Chatbot")
st.caption("Built with LangChain + Groq + Streamlit")


# ---------------------------------------------------------------------
# 5. SIDEBAR CONTROLS
# ---------------------------------------------------------------------
with st.sidebar:
    st.header("Settings")

    model_label = st.selectbox(
        "Model",
        options=list(AVAILABLE_MODELS.keys()),
        index=0,
        help="70B gives better answers. 8B is faster and has a higher rate limit.",
    )
    model_name = AVAILABLE_MODELS[model_label]

    persona_label = st.selectbox(
        "Assistant persona",
        options=list(PERSONAS.keys()),
        index=0,
        help="This changes the system message sent to the model.",
    )
    system_prompt = PERSONAS[persona_label]

    temperature = st.slider(
        "Temperature",
        min_value=0.0,
        max_value=1.0,
        value=0.6,
        step=0.1,
        help="0 = safe and repeatable. 1 = creative and more error-prone.",
    )

    st.divider()

    if st.button("Clear conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.divider()
    st.caption(
        "Your API key is read from the .env file locally, or from the "
        "GROQ_API_KEY secret when deployed."
    )


# ---------------------------------------------------------------------
# 6. CHAT HISTORY
# ---------------------------------------------------------------------
# st.session_state survives across re-runs, so this is where the
# conversation is stored. Everything else is rebuilt on every click.
if "messages" not in st.session_state:
    st.session_state.messages = []

# Redraw the whole conversation so far.
for message in st.session_state.messages:
    role = "user" if isinstance(message, HumanMessage) else "assistant"
    with st.chat_message(role):
        st.markdown(message.content)


# ---------------------------------------------------------------------
# 7. HANDLE NEW INPUT
# ---------------------------------------------------------------------
user_question = st.chat_input("Ask me anything...")

if user_question:
    # Show what the user just typed.
    with st.chat_message("user"):
        st.markdown(user_question)

    # Pass the conversation so far (excluding the new question) as history.
    history = st.session_state.messages.copy()

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                answer = get_response(
                    question=user_question,
                    history=history,
                    model_name=model_name,
                    temperature=temperature,
                    system_prompt=system_prompt,
                )
                st.markdown(answer)

                # Save both turns so they survive the next re-run.
                st.session_state.messages.append(HumanMessage(content=user_question))
                st.session_state.messages.append(AIMessage(content=answer))

            except Exception as e:
                st.error(f"Something went wrong: {e}")
                st.info(
                    "Common causes: the GROQ_API_KEY is missing or wrong, "
                    "or the model name is no longer available. "
                    "See the README for the fix."
                )
