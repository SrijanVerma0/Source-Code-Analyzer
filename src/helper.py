import os
from git import Repo
from langchain.document_loaders.generic import GenericLoader
from langchain.document_loaders.parsers import LanguageParser
from langchain.text_splitter import Language
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings

## clone github repos

def repo_ingeastion(repo_url):
    os.makedirs("repo",exist_ok=True)
    repo_path="repo/"
    Repo.clone_from(repo_url,to_path=repo_path)

## Loads repos as documents
def load_repo(repo_path):
    loader = GenericLoader.from_filesystem(
        repo_path,
        glob="**/*",
        suffixes=[".py"],
        parser = LanguageParser(language=Language.PYTHON,parser_threshhold=500)
    )

    documents = loader.load()

    return documents


def text_splitter(documents):
    documents_splitter = RecursiveCharacterTextSplitter.from_language(
        language=Language.PYTHON,
        chunk_size=2000,
        chunk_overlap=200
    )

    text_chunks = documents_splitter.split_documents(documents)

    return text_chunks


## load embeddings

def load_embedding():
    embeddings = OpenAIEmbeddings(
        model="openai/text-embedding-3-small",
        openai_api_key=os.getenv("OPENROUTER_API_KEY"),
        openai_api_base="https://openrouter.ai/api/v1",
        disallowed_special=()
    )

    return embeddings