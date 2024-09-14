import os
import time
import pinecone
import warnings
import streamlit as st
from datetime import datetime
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from doctor_locator import doctor_locator
from disease_finder import disease_info_page
from src.prompt import prompt_template
from pinecone import Pinecone, ServerlessSpec
from text_to_speech import synthesize_speech
from speech_to_text import recognize_from_microphone
from langchain.chains import LLMChain, RetrievalQA
from langchain_pinecone import PineconeVectorStore
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import AIMessage, HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains.combine_documents import create_stuff_documents_chain
from src.helper import load_pdf, text_split, download_hugginface_embeddings
from langchain.chains import create_history_aware_retriever, create_retrieval_chain

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
    # llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro")
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
    # llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro")
    prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a highly knowledgeable and trusted medical assistant, dedicated to providing accurate, concise, and clear information based on the user's symptoms. "
               "Utilize the context provided to deliver precise medical advice, and prioritize safety and clarity in your responses. "
               "If the information available is insufficient for a confident response, acknowledge your limitations and avoid making assumptions. "
               "For non-medical inquiries, politely inform the user that your expertise is limited to the medical field."
               "\n\nContext: {context}"),
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
# st.title("Medical Chatbot ⚕️")

# with st.sidebar:
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "Doctor Locator", "Disease Information"])  

if page == "Home":
    # Your existing code for the main page
    st.title("Medical Chatbot ⚕️") 
    # making chat persist
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [
        AIMessage(content="Hello I am your medical assistant. How can I help you?")
    ]

    if "vector_store" not in st.session_state:
        st.session_state.vector_store = vector_store   

    retriever_chain = get_context_retriever_chain(vector_store)
    user_query = None
    listening_placeholder = st.empty()

    if st.sidebar.button("Voice Input", use_container_width=True, key="voice_input"):
        listening_placeholder.text("Listening...")
        user_query = recognize_from_microphone()
        if user_query:
            response = get_response(user_query)
            st.session_state.chat_history.append(HumanMessage(content=user_query))
            st.session_state.chat_history.append(AIMessage(content=response))
            retrieved_documents = retriever_chain.invoke({
                "chat_history" : st.session_state.chat_history,
                "input" : user_query
            })
        listening_placeholder.empty()
        st.write("You said: ", user_query)

    if user_query or not user_query:
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
    for index, message in enumerate(st.session_state.chat_history):
        if isinstance(message, AIMessage):
            with st.chat_message("AI"):
                # Display the message
                st.write(message.content)
                # Button to synthesize speech for this message
                if st.button(f"Listen to Response {index}", key=f"listen_button_{index}"):
                    synthesize_speech(message.content)
        elif isinstance(message, HumanMessage):
            with st.chat_message("Human"):
                st.write(message.content)
                    
elif page == "Doctor Locator":
    doctor_locator()
    
elif page == "Disease Information":
    disease_info_page()