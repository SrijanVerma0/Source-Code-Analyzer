import shutil
from langchain_community.vectorstores import Chroma
from src.helper import load_embedding, repo_ingeastion
from dotenv import load_dotenv
import os
from flask import Flask, request, jsonify, render_template
from langchain_openai import ChatOpenAI
from langchain_classic.chains import ConversationalRetrievalChain
from langchain_classic.memory import ConversationSummaryMemory

app = Flask(__name__)

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")


embeddings = load_embedding()
persist_directory = 'db'

## Now loading persisted database from disk

vectordb = Chroma(persist_directory=persist_directory, embedding_function=embeddings)  # fixed: embedding_func -> embedding_function


llm = ChatOpenAI(
    model="google/gemini-2.5-flash-lite",
    openai_api_key=os.getenv("OPENROUTER_API_KEY"),
    openai_api_base="https://openrouter.ai/api/v1"
)

memory = ConversationSummaryMemory(llm=llm, memory_key="chat_history", return_messages=True)  # fixed: space in key, return_message -> return_messages
qa = ConversationalRetrievalChain.from_llm(llm, retriever=vectordb.as_retriever(search_type="mmr", search_kwargs={"k": 8}), memory=memory)


@app.route('/', methods=["GET", "POST"])
def index():
    return render_template('index.html')

@app.route('/chatbot', methods=["GET", "POST"])
def gitRepo():

    if request.method == 'POST':
        user_input = request.form['question']
        repo_ingeastion(user_input)
        os.system("python store_index.py")

    return jsonify({'response': str(user_input)})


@app.route('/get', methods=["GET", "POST"])
def chat():
    msg = request.form['msg']
    user_input = msg  # fixed: was 'imput' (typo), then called builtin 'input' instead
    print(user_input)

    if user_input == 'clear':
        shutil.rmtree("repo", ignore_errors=True)  # fixed: rm -rf doesn't work on Windows

    result = qa.invoke({"question": user_input})  # fixed: langchain>=0.2 requires .invoke(dict) not direct call
    print(result['answer'])
    return str(result['answer'])



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)