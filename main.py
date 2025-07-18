from flask import Flask, render_template, request, jsonify
from openai import OpenAI
from dotenv import load_dotenv
import os
app = Flask(__name__)

load_dotenv()
client = OpenAI(api_key=os.getenv("openai_key"))

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/hello", methods=["GET"])
def hello():
    return jsonify({"msg": "Hello World"})

@app.route("/api/ask", methods=["POST"])
def ask():
    data = request.get_json()
    userQuestion = data.get("question")

    contentInstructions = '''
                        You are a helpful assistant. Your role is to
                        teach the topic of Artificial Intelligence.
                        Your job is to thoroughly teach all of these
                        topics which may include Large Language Models,
                        Neural Networks, Deep learning, how AI works,
                        Machine Learning, how to train your own model, 
                        the theory behind AI and Machine Learning,
                        if needed, the math that comes with AI, etc. 
                        Your job is to teach it in a way that someone
                        with no knowledge understands these advanced topics.'''
    try:
        response = client.responses.create(
            model = "gpt-4o-mini",
            messages=[{
                "role": "system",
                "content": contentInstructions},
                {
                "role": "user",
                "content": userQuestion}
                ]
        )
        aiAnswer = response["choices"][0]["message"]["content"]
        return jsonify({"answer": aiAnswer})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)