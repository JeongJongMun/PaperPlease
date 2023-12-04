from flask import Flask, render_template, jsonify, request
from flask.json.provider import JSONProvider
import json
import sys
from langchain_utils import agent_executor
from langchain.callbacks import get_openai_callback


app = Flask(__name__)


# API #1: HTML 틀(template) 전달
@app.route('/')
def home():
    return render_template('index.html')

# API #2: 질문
@app.route('/submit', methods=['POST'])
def submit():
    input = request.form['question']
    answer = ""
    
    # Tracking Token Usage
    with get_openai_callback() as callback:
        # for c in chain.stream({"question" : input}):
        #     answer += c
        answer = agent_executor.invoke({'input':input})
        # Print Token Usage
        print(callback)


    return jsonify({'result': 'success', 'answer': answer})


if __name__ == '__main__':
    print(sys.executable)
    app.run('0.0.0.0', port=5000, debug=True)

"""
*Sample Questions
Who is the Author of "Attention is All You Need"?
Which AI Paper is Hottest in 2023? Describe it in 3 sentences.
Tell me about Attention is All You Need. Describe it in 3 sentences.
Who is the Author of 'GLUE: A Multi-Task Benchmark and Analysis Platform for Natural Language Understanding'?
"""