from langchain.vectorstores import Chroma
from src.helper import load_embedding,repo_ingeastion
from dotenv import load_dotenv
import os
from flask import Flask,request,jsonify,render_template
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationSummaryMemory

app = Flask(__name__)

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")


embeddings = load_embedding()
persist_directory = 'db'

## Now loading persisted database from disk

vectordb = Chroma(persist_directory=persist_directory,embedding_func=embeddings)


llm = ChatOpenAI(
    model="google/gemini-2.5-flash-lite",
    openai_api_key=os.getenv("OPENROUTER_API_KEY"),
    openai_api_base="https://openrouter.ai/api/v1"
)

memory = ConversationSummaryMemory(llm=llm,memory_key = "chat history",return_message = True)
qa = ConversationalRetrievalChain.from_llm(llm,retriever=vectordb.as_retriever(search_type="mmr", search_kwargs={"k":8}), memory=memory)


@app.route('/',methods=["GET","POST"])
def index():
    return render_template('index.html')

@app.route('/chatbot',methods=["GET","POST"])
def gitRepo():

    if request.method == 'POST':
        user_input = request.form['question']
        repo_ingeastion(user_input)
        os.system("python store_index.py")

    return jsonify({'response': str(user_input)})


@app.route('/get',methods=["GET","POST"])
def chat():
    msg = request.form['msg']
    imput = msg
    print(input)

    if input == 'clear':
        os.system("rm -rf repo")

    result = qa(input)
    print(result['answer'])
    return str(result['answer'])



if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8080,debug=True)