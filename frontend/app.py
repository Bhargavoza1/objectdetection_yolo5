import os
import base64
import requests
from flask import Flask, request, render_template, jsonify
from PIL import Image
import io

app = Flask(__name__)

# Backend URL
BACKEND_URL = 'http://host.docker.internal:8080/upload_base64'  # Ensure this matches your backend URL and port

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_image():
    try:
        # Get the image from the form
        file = request.files['image']
        image = Image.open(file.stream)

        # Convert the image to Base64
        buffered = io.BytesIO()
        image.save(buffered, format="JPEG")
        img_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")

        # Send the image to the backend
        response = requests.post(BACKEND_URL, json={'image': img_base64})

        # Check if the response is successful
        if response.status_code == 200:
            response_data = response.json()
            detections = response_data.get('detections', [])
            processed_image_base64 = response_data.get('processed_image', '')

            # Return the detections and the processed image
            return jsonify({
                "detections": detections,
                "processed_image": processed_image_base64
            }), 200
        else:
            # Handle backend errors
            error_message = response.json().get('error', 'Unknown error')
            return jsonify({"error": f"Backend error: {error_message}"}), response.status_code

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=8080)