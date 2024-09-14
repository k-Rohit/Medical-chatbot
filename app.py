import os
import pinecone
import warnings
import streamlit as st
from dotenv import load_dotenv
from src.prompt import prompt_template
from langchain_groq import ChatGroq
from doctor_locator import doctor_locator
# from disease_finder import disease_info_page
from pinecone import Pinecone, ServerlessSpec
from langchain.chains import LLMChain, RetrievalQA
from langchain_pinecone import PineconeVectorStore
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import AIMessage, HumanMessage
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains.combine_documents import create_stuff_documents_chain
from src.helper import load_pdf, text_split, download_hugginface_embeddings
# from crew_ai.agent_doc.src.agent_doc.crew import *

warnings.filterwarnings("ignore")
load_dotenv()

PINECONE_API_KEY = os.environ.get('PINECONE_API')
if "GOOGLE_API_KEY" not in os.environ:
    os.environ["GOOGLE_API_KEY"] = getpass.getpass("Provide your Google API Key")
if "GROQ_API_KEY" not in os.environ:
    os.environ["GROQ_API_KEY"] = getpass.getpass("Enter your Groq API key: ")

# Load the embeddings
embeddings = download_hugginface_embeddings()

# Initialise the Pinecone vector store and index
pc = Pinecone(api_key=PINECONE_API_KEY)
index_name = "medical-chatbot3"
index = pc.Index(index_name)
vector_store = PineconeVectorStore(index=index, embedding=embeddings)

def get_context_retriever_chain(vector_store):
    llm = ChatGroq(model="mixtral-8x7b-32768")
    retriever = vector_store.as_retriever(
    search_type="similarity_score_threshold",
    search_kwargs={"k": 2, "score_threshold": 0.6},
    )
    prompt = ChatPromptTemplate.from_messages([
        MessagesPlaceholder(variable_name="chat_history"),
        ("user","{input}"),
        ("user","Given the above conversation, generate a search query to look up in order to get information relevant to the conversation")
    ])
    retriever_chain = create_history_aware_retriever(llm, retriever, prompt)
    return retriever_chain

def get_conversational_rag_chain(retriever_chain):
    llm = ChatGroq(model="mixtral-8x7b-32768")
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a trusted medical assistant. "
                   "Use the information provided to accurately and concisely answer the user's question. "
                   "If you don’t have enough information to provide a confident answer, acknowledge that you don’t know and refrain from making up any information. If anyone asks information other than medical feild just say you don't know"
                   ":\n\n{context}"),
        MessagesPlaceholder(variable_name="chat_history"),
        ("user", "{input}"),
    ])
    stuff_documents_chain = create_stuff_documents_chain(llm, prompt)
    return create_retrieval_chain(retriever_chain, stuff_documents_chain)
    
def get_response(user_input):
    retriever_chain = get_context_retriever_chain(st.session_state.vector_store)
    conversation_rag_chain = get_conversational_rag_chain(retriever_chain)
    response = conversation_rag_chain.invoke({
        "chat_history": st.session_state.chat_history,
        "input": user_input
    })
    return response['answer']

# UI Code - 

st.set_page_config(page_title="Medical Chatbot ",page_icon="⚕️")
st.title("Medical Chatbot ⚕️")

# making chat persist
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
    AIMessage(content="Hello I am your medical assiatant. How can I help you?")
]

if "vector_store" not in st.session_state:
    st.session_state.vector_store = vector_store   

retriever_chain = get_context_retriever_chain(vector_store)
user_query = st.chat_input("Type your message here...")

if user_query:
    response = get_response(user_query)
    st.session_state.chat_history.append(HumanMessage(content=user_query))
    st.session_state.chat_history.append(AIMessage(content=response))
    retrieved_documents = retriever_chain.invoke({
        "chat_history" : st.session_state.chat_history,
        "input" : user_query
    })

# conversation
for message in st.session_state.chat_history:
    if isinstance(message, AIMessage):
        with st.chat_message("AI"):
            st.write(message.content)
    elif isinstance(message, HumanMessage):
        with st.chat_message("Human"):
            st.write(message.content)
            
        
