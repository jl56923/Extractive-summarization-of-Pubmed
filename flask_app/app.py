from flask import Flask, abort, render_template, jsonify, request
from api import make_summarization

app = Flask('SummarizerApp')

@app.route('/summarize', methods=['POST'])
def do_summarization():
    if not request.json:
        abort(400)
    data = request.json

    response = make_summarization(data)
    
    return jsonify(response)

@app.route('/')
def index():
    return render_template('index.html')

app.run(debug=True)
