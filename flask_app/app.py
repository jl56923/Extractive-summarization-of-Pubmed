from flask import Flask, abort, render_template, jsonify, request
from api import make_abstracts, make_summaries

app = Flask('SummarizerApp')

@app.route('/get_abstracts', methods=['POST'])
def do_abstracts():
    if not request.json:
        abort(400)
    data = request.json

    response = make_abstracts(data)

    return jsonify(response)

@app.route('/get_summaries', methods=['POST'])
def do_summaries():
    if not request.json:
        abort(400)
    data = request.json

    response = make_summaries(data)

    return jsonify(response)

@app.route('/')
def index():
    return render_template('index.html')

app.run(debug=True)
