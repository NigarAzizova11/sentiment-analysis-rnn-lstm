from flask import Flask, request, jsonify, render_template
from tensorflow.keras.models import load_model
from tensorflow.keras.datasets import imdb
from tensorflow.keras.preprocessing.sequence import pad_sequences

app = Flask(__name__)

import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

rnn_model = load_model(os.path.join(BASE_DIR, "simple_rnn_model.h5"))
lstm_model = load_model(os.path.join(BASE_DIR, "lstm_model.h5"))

word_index = imdb.get_word_index()
maxlen = 200


@app.route("/")
def home():
    return render_template("index.html")


def encode_review(text):
    tokens = text.lower().split()
    encoded = []

    for word in tokens:
        if word in word_index:
            encoded.append(word_index[word] + 3)
        else:
            encoded.append(2)   # unknown word

    return pad_sequences([encoded], maxlen=maxlen)


@app.route("/predict", methods=["POST"])
def predict():

    data = request.json
    text = data["text"]

    sequence = encode_review(text)

    rnn_score = float(rnn_model.predict(sequence)[0][0])
    lstm_score = float(lstm_model.predict(sequence)[0][0])

    result = {
        "rnn_result": {
            "score": rnn_score,
            "label": "Positive" if rnn_score > 0.7 else "Negative"
        },
        "lstm_result": {
            "score": lstm_score,
            "label": "Positive" if lstm_score > 0.7 else "Negative"
        }
    }

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)