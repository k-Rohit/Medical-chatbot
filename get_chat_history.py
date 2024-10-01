# import streamlit as st
# from langchain_mongodb.chat_message_histories import MongoDBChatMessageHistory
# from langchain_core.messages import AIMessage, HumanMessage
# from dotenv import load_dotenv
# load_dotenv()


# def see_chat_history():
#     chat_message_history = MongoDBChatMessageHistory(
#         session_id="test_session",
#         connection_string="",
#         database_name="medical_chatbot",
#         collection_name="chat_histories",
#     )
    
#     for index, message in enumerate(chat_message_history.messages):
#         if isinstance(message, AIMessage):
#             with st.chat_message("AI"):
#                 st.write(message.content)
#         elif isinstance(message, HumanMessage):
#             with st.chat_message("Human"):
#                 st.write(message.content)

# if __name__ == "__main__":
#     see_chat_history()

import streamlit as st
from langchain_mongodb.chat_message_histories import MongoDBChatMessageHistory
from langchain_core.messages import AIMessage, HumanMessage
from dotenv import load_dotenv
from pymongo import MongoClient, ASCENDING
from datetime import datetime
import os

# Load environment variables from a .env file
load_dotenv()

# MongoDB connection setup
def get_mongo_client():
    connection_string = os.getenv("MONGODB_CONNECTION_STRING")
    client = MongoClient(connection_string)
    return client

# Create TTL index to expire chat history after 7 days
def create_ttl_index():
    client = get_mongo_client()
    db = client['medical_chatbot']
    collection = db['chat_histories']
    
    # Create the TTL index on 'createdAt' field
    collection.create_index([("createdAt", ASCENDING)], expireAfterSeconds=604800)

# Function to display chat history from MongoDB
def see_chat_history():
    create_ttl_index()  # Ensure the TTL index is created

    chat_message_history = MongoDBChatMessageHistory(
        session_id="test_session",
        connection_string=os.getenv("MONGODB_CONNECTION_STRING"),  # Fetch from environment variable
        database_name="medical_chatbot",
        collection_name="chat_histories",
    )
    
    st.title("Chat History")
    if not chat_message_history.messages:
        st.write("No chat history available.")
    else:
        for index, message in enumerate(chat_message_history.messages):
            if isinstance(message, AIMessage):
                with st.chat_message("AI"):
                    st.write(message.content)
            elif isinstance(message, HumanMessage):
                with st.chat_message("Human"):
                    st.write(message.content)

def save_chat_message(message_content, role="human"):
    client = get_mongo_client()
    db = client['medical_chatbot']
    collection = db['chat_histories']
    
    message_data = {
        "content": message_content,
        "role": role,
        "createdAt": datetime.utcnow() 
    }
    
    collection.insert_one(message_data)

# Function to delete all chat history
def delete_chat_history():
    client = get_mongo_client()
    db = client['medical_chatbot']
    collection = db['chat_histories']
    
    result = collection.delete_many({})
    st.sidebar.write(f"Deleted {result.deleted_count} messages from the chat history.")
    # Button to delete chat history in the sidebar
    st.sidebar.title("Manage Chat History")
    if st.sidebar.button("Delete Chat History"):
        delete_chat_history()
        st.sidebar.success("Chat history has been deleted.")

if __name__ == "__main__":
    see_chat_history()

    
