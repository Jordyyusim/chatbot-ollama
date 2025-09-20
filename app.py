from flask import Flask, request
import re
from database import save_conversation
from tools import tool_check_order
from rag import rag_query
from langchain_community.chat_models import ChatOllama
from langchain.memory import ConversationBufferWindowMemory
from langchain.chains import LLMChain
from langchain_core.prompts import ChatPromptTemplate

app = Flask(__name__)

llm = ChatOllama(model="llama3.2:3b")
memory = ConversationBufferWindowMemory(k=3)

prompt = ChatPromptTemplate.from_messages([
    ("system", "Asisten Customer Service Toko Online."),
    ("user", "{input}")
])
chain = LLMChain(llm=llm, prompt=prompt, memory=memory)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_msg = data.get("message")
    print(user_msg)

    # cek ORDER ID di user_msg
    order = re.findall(r"(TKJY\d+)", user_msg, re.IGNORECASE)
    if order:
        print("ada nomor order")
        order_id = order[0]
        reply = tool_check_order(order_id)
    else:
        print("tidak ada nomor order")
        context = rag_query(user_msg)
        prompt_input = f"""
                        Anda adalah virtual asisten toko online.
                        Jawab pertanyaan user secara langsung, pakai konteks yang ada:
                        {context}

                        Pertanyaan user: {user_msg}

                        Jawaban Anda harus jelas, lengkap dan memastikan user percaya kepada kami.
                        """
        reply = chain.invoke({"input": prompt_input}).get("text")
        print(reply)

    save_conversation(user_msg, reply)
    return {"reply": reply}

if __name__ == "__main__":
    app.run(port=5000, debug=True)
