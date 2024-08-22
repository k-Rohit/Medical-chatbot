import os
import pinecone
from dotenv import load_dotenv 
from src.helper import load_pdf, text_split, download_hugginface_embeddings
from langchain.vectorstores import Pinecone
from pinecone import Pinecone
from langchain_pinecone import PineconeVectorStore
from uuid import uuid4
from langchain_core.documents import Document

load_dotenv()

PINECONE_API_KEY = os.environ.get('PINECONE_API')
# print(PINECONE_API_KEY)

# Extract the data
extracted_data = load_pdf("data")

# Creating the chunks
text_chunks = text_split(extracted_data)

# Load the embeddings
embeddings = download_hugginface_embeddings()

# Initialise the Pinecone vector store and index
pc = Pinecone(api_key=PINECONE_API_KEY)
index_name = "medical-chatbot2"

existing_indexes = [index_info["name"] for index_info in pc.list_indexes()]

if index_name not in existing_indexes:
    pc.create_index(
        name=index_name,
        dimension=384,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1"),
    )
    while not pc.describe_index(index_name).status["ready"]:
        time.sleep(1)

index = pc.Index(index_name)
vector_store = PineconeVectorStore(index=index, embedding=embeddings)

# Store the documents
documents = [Document(page_content=t.page_content) for t in text_chunks]
uuids = [str(uuid4()) for _ in range(len(documents))]
vector_store.add_documents(documents=documents, ids=uuids)