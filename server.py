import io
import json
from flask import Flask, render_template, request
from lobe import ImageModel
from PIL import Image

app = Flask(__name__)
model = ImageModel.load('Fruits TensorFlow')

prices = {'Apple': 99, 'Banana': 88, 'Grapefruit': 128, 'Orange': 66}

def predict_pil(pil):
    result = model.predict(pil)

    #print(result.prediction)
    for label, prop in result.labels: # Print all classes
        print(f"{label}: {prop*100}%")

    return result.as_dict()


@app.route('/')
def index():
    return render_template('index.html', title='果物屋さん')


@app.route('/predict', methods=['POST'])
def predict():
    img = request.files['image'].read()
    pil = Image.open(io.BytesIO(img))
    ret = predict_pil(pil)
    ret['price'] = prices[ret['Prediction']]
    return json.dumps(ret)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)