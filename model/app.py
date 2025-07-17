from flask import Flask, request, jsonify
import tensorflow as tf
import keras
from keras.layers import LSTM
from keras.activations import relu
import numpy as np
import cv2
import os
from utils import preprocess_image, decode_prediction
import base64
from PIL import Image
import io
import urllib

app = Flask(__name__)
@keras.saving.register_keras_serializable()
class FixedLSTM(LSTM):
    def __init__(self, *args, **kwargs):
        kwargs.pop("time_major", None)
        super().__init__(*args, **kwargs)

custom_objects = {
    "LSTM": FixedLSTM,
    "leaky_relu": tf.nn.leaky_relu,
}

with keras.saving.custom_object_scope(custom_objects):
    model = keras.models.load_model("captcha_model.h5")

img_width   = 160
img_height  = 60
max_length  = 5 
characters  = [' ', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
char_to_num = keras.layers.StringLookup(vocabulary=list(characters), mask_token=None)
num_to_char = keras.layers.StringLookup(vocabulary=char_to_num.get_vocabulary(), mask_token=None, invert=True)


@app.route("/predict", methods=["POST"])
def predict():
    """
    data = {
        "data": b64 or link_img
    }
    """
    data = request.get_json()
    if not data or "data" not in data:
        return jsonify({"error": "No data provided"}), 400
    
    image_data = data["data"]

    if image_data.startswith("data:image/jpeg;base64,"):
        image_data  = image_data.replace("data:image/jpeg;base64,", "")
        image_data  = base64.b64decode(image_data)
        image       = Image.open(io.BytesIO(image_data))
        image       = np.array(image.convert("L"))

    elif image_data.startswith("http"):
        image = Image.open(urllib.request.urlopen(image_data))
        image = np.array(image.convert("L"))

    image           = preprocess_image(image, img_width, img_height)
    image_tensor    = tf.convert_to_tensor(image, dtype=tf.float32)
    image_tensor    = tf.expand_dims(image_tensor, axis=0)  # Thêm batch
    preds           = model.predict(image_tensor)
    result_text     = decode_prediction(preds, num_to_char, max_length)

    return jsonify({"result": result_text})

if __name__ == "__main__":
    app.run(port=5000, debug=False)
