from os import environ, getenv

from flask import Flask, jsonify, request
from flaskcors import CORS, crossorigin
from llama_index.core.llms import ChatMessage
from llama_index.llms.fireworks import Fireworks

app = Flask(__name__)
cors = CORS(app)
llm = Fireworks(model="accounts/fireworks/models/llama-v3-70b-instruct")


def compile_conversation_history(ch: list[str]) -> list[ChatMessage]:
    return [
        ChatMessage(role="user" if idx % 2 == 0 else "assistant", content=message) for idx, message in enumerate(ch)
    ]


@app.route("/")
def home():
    return "Hello World!"


@app.route("/api/get_answer", methods=["POST"])
def get_answer():
    data = request.get_json()
    original_question = data["original_question"]
    conversation_history = data["conversation_history"]
    # odd indices is LLM messages
    # even indices is LLM messages
    # create ChatMessage objects for conversation_history
    base_system_message = "You are a helpful assistant that assists students with questions in a midterm format. Guide students by addressing what they get wrong if they chose the wrong answer. Do not reveal the true answer of the question. The question the student is working to answer is {original_question}."  # noqa: E501
    messages = [
        ChatMessage(
            role="system",
            content=base_system_message.format(original_question=original_question),
        ),
    ]
    messages.extend(compile_conversation_history(conversation_history))
    resp = llm.chat(messages).message.content
    return jsonify({"message": resp})


@app.route("/api/submit", methods=["POST"])
def handle_assignment_submission():
    data = request.get_json()
    question = data["question"]
    conversation_history = data["conversation_history"]


if __name__ == "__main__":
    # FIREWORKS_API_KEY = "FIREWORKS_API_KEY"
    # if FIREWORKS_API_KEY not in environ:
    #     raise ValueError(f"Please provide a {FIREWORKS_API_KEY}.")
    # fw_api_key = getenv(FIREWORKS_API_KEY)
    app.run(host="0.0.0.0", port=5601)
