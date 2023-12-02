from flask import Flask, request, jsonify
from PIL import Image
from io import BytesIO
from ultralytics import YOLO
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Load a model

# Function to perform object detection using YOLO
def perform_object_detection(image_bytes):
    # Check if the input is a URL or bytes of an image
    if isinstance(image_bytes, str):  # If it's a URL
        response = requests.get(image_bytes)
        image = Image.open(BytesIO(response.content)).convert("RGB")
    else:  # Assuming it's bytes of an image
        image = Image.open(BytesIO(image_bytes)).convert("RGB")

    # Perform the object detection on the image using YOLO or another model
    model = YOLO('best.pt')
    names = model.names
    results = model.predict(image, save=True, imgsz=640, conf=0.25)
    # Assuming the YOLO model returns predictions
    

    # cls = int(results[0].boxes.cls)
    list_fruit = []
    for i in results[0].boxes.cls:
          list_fruit.append(names[int(i)])
    print(list_fruit)
    result_fruit = []
    fruit =  ["apple", "banana", "avocado", "kiwi", "lemon", "mango", "pineapple", "strawberry"]
 
          
 
         
    # # Save to a file
    # with open('predictions.txt', 'w') as file:
    #     file.write(str(predictions))  # Saving predictions as a string

    return list_fruit  # Return the predictions

@app.route('/') 
def index():
    return 'Hello World!' 


# @app.route('/getResults' , methods=['get'])
# def result():
#       def clear_list():
#             list_fruit.clear()
            
# return jsonify(list_fruit,clear_list())
# #how to return a list and clear it after returning it

@app.route('/your-endpoint', methods=['POST'])
def handle_form_data():
    field1 = request.form.get('field1')
    field2 = request.form.get('field2')
    # Access other fields as needed
    
    # Perform desired operations with the received data
    # ...
    
    return 'Data received successfully'

@app.route('/detect', methods=['POST'])
def detect_objects():
    # Get the image bytes from the request
    print(request.files)
    image_bytes = request.files['image'].read()
    # print(image_bytes)
    # Perform object detection
    detected_objects = perform_object_detection(image_bytes)
    # Return the detected objects in JSON format
    return jsonify(detected_objects)

if __name__ == '__main__':
    app.run(debug=True, port=8000, host='0.0.0.0')
