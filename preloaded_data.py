from data_loader import load_text_data
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from config import OPENAI_API_KEY

def load_data(folder_path: str):
    preloaded_data = load_text_data(folder_path)
    
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    docs = text_splitter.split_documents(preloaded_data)

    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)

    db = FAISS.from_documents(docs, embeddings)
    db.save_local("faiss_index")
