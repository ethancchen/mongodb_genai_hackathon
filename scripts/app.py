from flask import Flask, jsonify, request
from llama_index.core import SimpleDirectoryReader, StorageContext, VectorStoreIndex
from llama_index.core.llms import ChatMessage
from llama_index.llms.fireworks import Fireworks

app = Flask(__name__)
llm = Fireworks()


def compile_conversation_history(ch: list[str]) -> list[ChatMessage]:
    lst = []
    for idx, message in enumerate(ch):
        curr_role = "user" if idx % 2 == 0 else "assistant"
        lst.append(ChatMessage(role=curr_role, content=message))
    return lst


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
    base_system_message = "You are a helpful assistant that assists students with questions in a midterm format. Guide students by addressing what they get wrong if they chose the wrong answer. Do not reveal the true answer of the question. The question the student is working to answer is {original_question}."
    messages = [
        ChatMessage(
            role="system",
            content=base_system_message.format(original_question=original_question),
        ),
    ]
    print("ch is", compile_conversation_history)
    messages.extend(compile_conversation_history(conversation_history))
    print(messages)
    resp = llm.chat(messages).message.content
    return jsonify({"message": resp})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5601)
