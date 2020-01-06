from flask import Flask, jsonify, request
import logging
import json
import pickle
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences

MAX_SEQUENCE_LENGTH = 30  # max length of text (words) including padding

app = Flask(__name__)

if __name__ != '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)


@app.route('/', methods=['GET'])
def home():
    return "Hello world!"


@app.route('/getEmotion', methods=['POST'])
def getEmotion():
    input = json.loads(request.data.decode('utf-8'))['text']
    with open('tokenizer.pickle', 'rb') as handle:
        tokenizer = pickle.load(handle)

    model = load_model('model/BalanceNet.h5')
    classes = ["neutral", "happy", "sad", "hate", "anger"]
    sequences_test = tokenizer.texts_to_sequences([input])
    data_int_t = pad_sequences(
        sequences_test, padding='pre', maxlen=(MAX_SEQUENCE_LENGTH-5))
    data_test = pad_sequences(
        data_int_t, padding='post', maxlen=(MAX_SEQUENCE_LENGTH))
    y_prob = model.predict(data_test)
    for n, prediction in enumerate(y_prob):
        pred = y_prob.argmax(axis=-1)[n]
        respObj = {'data': {'emotion': int(pred)}}
    app.logger.info(input, int(pred))
    return jsonify(respObj)


# app.run(host='0.0.0.0', port=8080)
