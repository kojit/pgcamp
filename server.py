import io
import os
import json
from flask import Flask, render_template, request
from PIL import Image

from tf_model_helper import TFModel

app = Flask(__name__)

# Path to signature.json and model file
ASSETS_PATH = os.path.join(".", "./model")
TF_MODEL = TFModel(ASSETS_PATH)
PRICES = {'Apple': 99, 'Banana': 88, 'Grapefruit': 128, 'Orange': 66}


def predict_pil(pil):
    result = TF_MODEL.predict(pil)

    #print(result['predictions'])
    predictions = {}
    for p in result['predictions']:
        print(f"{p['label']}: {p['confidence']*100}%")
        predictions[p['label']] = p['confidence']*100

    maxLabel = max((v, k) for k, v in predictions.items())[1]
    return maxLabel


@app.route('/')
def index():
    return render_template('index.html', title='果物屋さん')


@app.route('/predict', methods=['POST'])
def predict():
    img = request.files['image'].read()
    pil = Image.open(io.BytesIO(img))
    label = predict_pil(pil)
    return json.dumps({'prediction': label, 'price': PRICES[label]})


if __name__ == "__main__":
    #app.run(debug=True, host='0.0.0.0', port=5000)
    #app.run(host='127.0.0.1', port=5000, debug=True)
    app.run(debug=True, port=5000)
