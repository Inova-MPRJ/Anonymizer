from flask import Flask, jsonify, request
from anonimization import anonymize_text
app = Flask(__name__)

@app.route('/', methods=['POST'])
def index(): # TODO: Fazer rota/função para receber CSV
    data = request.json
    text = data['text']
    anonymized_text = anonymize_text(text)
    return jsonify({"Texto anonimizado": anonymized_text})

if __name__ == '__main__':
    app.run(debug=True)