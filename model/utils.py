import cv2
import numpy as np
import tensorflow as tf

def preprocess_image(img, img_width, img_height):
    img = cv2.resize(img, (img_width, img_height))
    img = img.astype("float32") / 255.0
    img = img.T
    img = np.expand_dims(img, axis=-1)
    return img


def decode_prediction(preds, num_to_char, max_length) -> str:
    input_len = np.ones(preds.shape[0]) * preds.shape[1]
    results = tf.keras.backend.ctc_decode(preds, input_length=input_len, greedy=True)[0][0][:, :max_length]

    output_text = []
    for res in results:
        text = tf.strings.reduce_join(num_to_char(res)).numpy().decode("utf-8")
        output_text.append(text)

    return output_text[0] if output_text else ""
