from flask import Flask, jsonify, request
from llama_index.core import SimpleDirectoryReader, StorageContext, VectorStoreIndex
from llama_index.core.llms import ChatMessage
from llama_index.llms.fireworks import Fireworks

app = Flask(__name__)


@app.route("/")
def home():
    return "Hello World!"


@app.route("/api/get_answer", methods=["POST"])
def get_answer():
    data = request.get_json()
    original_question = data["original_question"]
    conversation_history = data["conversation_history"]
    # even indices is LLM messages
    # odd indices is LLM messages
    messages = [
        ChatMessage(
            role="system",
            content="You are a helpful assistant that assists students with questions in a midterm format. Guide students by addressing what they got wrong if they chose the wrong answer. Do not reveal the true answer of the question.",
        ),
        ChatMessage(role="user", content="What is your name"),
    ]
    resp = Fireworks().chat(messages).message.content
    return jsonify({"message": resp})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5601)
