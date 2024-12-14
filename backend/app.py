import os
import base64
from flask import Flask, request, jsonify
import torch
from PIL import Image, ImageDraw
import io
import numpy as np
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
print(torch.__version__)
print(torch.cuda.is_available())

# Directory to store uploaded images
UPLOAD_FOLDER = 'uploaded_images'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Load YOLO model and move it to the GPU (if available)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = torch.hub.load('ultralytics/yolov5', 'yolov5s').to(device)

@app.route('/upload_base64', methods=['POST'])
def upload_base64_image():
    try:
        # Get the Base64 image string from the request
        data = request.json

        if 'image' not in data:
            return jsonify({"error": "Image is required."}), 400

        image_base64 = data['image']

        # Decode the Base64 string
        image_data = base64.b64decode(image_base64)
        image_file = f'{UPLOAD_FOLDER}/test.jpg'

        # Save the image to the upload folder
        file_path = os.path.join(UPLOAD_FOLDER, 'test.jpg')
        with open(file_path, 'wb') as f:
            f.write(image_data)

        try:
            # Open the image using PIL
            image = Image.open(image_file)

            # Perform object detection with YOLO (auto converts to tensor)
            results = model(image)

            # Extract results from YOLO (no need to manually unpack)
            results_df = results.pandas().xyxy[0]

            # Convert DataFrame to JSON
            results_json = results_df.to_dict(orient="records")

            # Draw bounding boxes on the image
            draw = ImageDraw.Draw(image)
            for result in results_json:
                xmin, ymin, xmax, ymax = result['xmin'], result['ymin'], result['xmax'], result['ymax']
                label = result['name']
                confidence = result['confidence']
                draw.rectangle([xmin, ymin, xmax, ymax], outline="red", width=3)
                draw.text((xmin, ymin), f"{label} {confidence:.2f}", fill="red")

            # Save the output image to a byte stream
            output_image_stream = io.BytesIO()
            image.save(output_image_stream, format="JPEG")
            output_image_stream.seek(0)

            # Convert the output image to Base64
            processed_image_base64 = base64.b64encode(output_image_stream.getvalue()).decode("utf-8")

            # Return the detection results and processed image
            return jsonify({
                "detections": results_json,
                "processed_image": processed_image_base64
            }), 200

        except Exception as e:
            return jsonify({"error": "Failed to process image.", "details": str(e)}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/hello', methods=['GET'])
def say_hello():
    return jsonify({"message": "Hello, world!"}), 200

if __name__ == '__main__':
    app.run(debug=True)
