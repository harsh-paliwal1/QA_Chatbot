"""
LangChain Q&A Chatbot -- SIMPLE VERSION
--------------------------------------
This is the stripped-down build: one text box, one button, one answer.
No chat history, no sidebar, no model picker.

Build this one FIRST to check that your setup works, then move to app.py
which has the full feature set.

Run with:   streamlit run app_simple.py

API KEY: goes in the .env file, never in this file.
"""

import streamlit as st
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Reads .env locally; does nothing (harmlessly) when deployed.
load_dotenv()


@st.cache_resource
def build_chain():
    llm = ChatGroq(
        model="openai/gpt-oss-120b",
        temperature=0.6,
    )

    prompt = ChatPromptTemplate.from_messages([
        ("system",
         "You are a knowledgeable and friendly assistant. Answer the user's "
         "question clearly and accurately. If you do not know something, say "
         "so instead of guessing."),
        ("human", "{question}"),
    ])

    return prompt | llm | StrOutputParser()


def get_response(question: str) -> str:
    chain = build_chain()
    return chain.invoke({"question": question})


st.set_page_config(page_title="Q&A Demo", page_icon="::")

st.header("LangChain Q&A Chatbot")
st.caption("Powered by Llama 3.3 on Groq")

user_question = st.text_input("Ask me anything:", key="input")

submit = st.button("Get Answer")

if submit and user_question:
    with st.spinner("Thinking..."):
        try:
            answer = get_response(user_question)
            st.subheader("Answer")
            st.write(answer)
        except Exception as e:
            st.error(f"Something went wrong: {e}")

elif submit and not user_question:
    st.warning("Please type a question first.")
