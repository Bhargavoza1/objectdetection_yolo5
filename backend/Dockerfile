# Use the NVIDIA CUDA base image with Python
FROM nvidia/cuda:12.6.3-cudnn-devel-ubuntu22.04
ENV DEBIAN_FRONTEND=noninteractive
# Set environment variables to ensure Python output is not buffered
ENV PYTHONUNBUFFERED 1

# Install system dependencies (for OpenCV, etc.)
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    python3-pip \
    python3-dev \
    curl \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip3 install --upgrade pip
RUN pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu124
RUN pip3 install opencv-python
RUN pip3 install pandas
RUN pip3 install requests
RUN pip3 install ultralytics
RUN pip3 install yolov5-utils
RUN pip3 install flask
RUN pip3 install flask-cors
RUN pip3 install --upgrade Pillow

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Create image storage directory
RUN mkdir -p /app/uploaded_images

# Expose the Flask app port
EXPOSE 8080

# Run the Flask app
CMD ["flask", "run", "--host=0.0.0.0", "--port=8080"]
