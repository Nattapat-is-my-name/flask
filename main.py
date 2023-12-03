from flask import Flask, request, jsonify
from PIL import Image
from io import BytesIO
from ultralytics import YOLO
import requests
from flask_cors import CORS
import dill
from collections import Counter

app = Flask(__name__)
CORS(app)



def perform_object_detection(image_bytes):
 
    if isinstance(image_bytes, str): 
        response = requests.get(image_bytes)
        image = Image.open(BytesIO(response.content)).convert("RGB")
    else:
        image = Image.open(BytesIO(image_bytes)).convert("RGB")

 
    model = YOLO('best.pt')
    names = model.names
    results = model.predict(image, save=True, imgsz=640, conf=0.7)
 
    
    print(results[0].boxes.cls)
    if len(results[0].boxes.cls) == 0:
           print("No fruit detected")
           return  "No fruit detected"
    else:
        print(results[0].boxes.cls[0])
        list_fruit = []
        for i in results[0].boxes.cls:
            list_fruit.append(names[int(i)])
        print(list_fruit)
        result = Counter(list_fruit)
    return result
          

@app.route('/') 
def index():
    return 'Hello Boss!'


@app.route('/detect', methods=['POST'])
def detect_objects():
    image_bytes = request.files['image'].read()
    detected_objects = perform_object_detection(image_bytes)
    return jsonify(detected_objects)


if __name__ == '__main__':
    app.run(debug=True, port=8000) 