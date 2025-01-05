from flask import Flask, jsonify, request, render_template
from dotenv import load_dotenv
import os
from main.main import mainrun
load_dotenv()

app = Flask(__name__)
chat_history = []
@app.route('/')
def index():
    return render_template("index.html")

@app.route("/process", methods = ['POST'])
def process():
    question = request.form.get("question")
    print("xu print question : ", question)
    global chat_history
    chat_history.append(("human", question))
    chat_history_str = " ".join([f"{role} : {text}" for role, text in chat_history])
    res = mainrun(question= question, chat_history=chat_history_str)
    print("res output", res)

    chat_history.append(("ai", res['output']))
    print("chat_history is: ", chat_history)
    return jsonify({
        "question" : question,
        "result": res['output'],
        "chat_history" : chat_history
    })


if __name__ == "__main__":
    app.run(host= "0.0.0.0", debug=True)