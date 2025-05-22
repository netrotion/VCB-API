import requests
import base64

image_path = "<your_captcha_image_path>"

url = "http://127.0.0.1:5000/predict"
js = {"data" : f"data:image/jpeg;base64,{base64.b64encode(open(image_path, 'rb').read()).decode()}"}

response = requests.post(url, json=js)

if response.status_code == 200:
    print("Prediction:", response.json()["result"])
else:
    print("Error:", response.status_code, response.text)
