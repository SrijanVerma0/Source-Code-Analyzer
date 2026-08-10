from src.helper import load_repo, text_splitter, load_embedding, repo_ingeastion
from dotenv import load_dotenv
from langchain_community.vectorstores import Chroma
import os

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")


documents = load_repo('repo/')
text_chunks = text_splitter(documents)
embeddings = load_embedding()

## storing vectors in ChromaDB

vectordb = Chroma.from_documents(text_chunks, embedding=embeddings, persist_directory='./db')
vectordb.persist()  # fixed: missing parentheses — was a no-op