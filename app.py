import streamlit as st
import openai
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

import os
from dotenv import load_dotenv
load_dotenv()

## Langsmith tracking
os.environ['LANGCHAIN_API_KEY'] = os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "Q&A Chatbot with OpenAI"

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant. Please respond to the user's query."),
        ("user", "Question:{question}")
    ]
)
def generate_response(question,api_key,llm,temperature, max_tokens):
    openai.api_key = api_key
    llm = ChatOpenAI(model = llm)
    output_parser = StrOutputParser()
    chain = prompt | llm | output_parser
    answer = chain.invoke({'question': question})
    return answer


## Title of the appp

st.title("Q&A Chatbot with OpenAI")

## Sidebar
st.sidebar.title("Settings")
api_key = st.sidebar.text_input("Enter your Open API Key", type="password")

## Dropdown to select the model

llm = st.sidebar.selectbox("Select an OpenAI model", ["gpt-4o", "gpt-4-turbo", "gpt-4"])

## Slider to select the temperature

temperature = st.sidebar.slider("Temperature", min_value=0.0, max_value=1.0, value=0.7)
max_tokens = st.sidebar.slider("Max Tokens", min_value=50, max_value=500, value=150)

## main interface

st.write("Ask your question here")
user_input = st.text_area("Question")

if user_input:
    response = generate_response(user_input,api_key,llm,temperature,max_tokens)
    st.write(response)
else:
    st.write("Please enter a question to get a response")