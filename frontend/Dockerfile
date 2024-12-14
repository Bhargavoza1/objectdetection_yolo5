# Use the official Python 3.9 image as the base image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Install system dependencies (if needed)
RUN apt-get update && apt-get install -y \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Flask and Werkzeug with specific versions for compatibility
RUN pip install --no-cache-dir \
    Flask \
    Pillow \
    requests

# Copy the application code into the container
COPY . /app/

# Expose the port on which the Flask app will run
EXPOSE 80

# Set environment variable for Flask
ENV FLASK_APP=app.py

# Command to run the Flask app with custom host and port
CMD ["flask", "run", "--host=0.0.0.0", "--port=80"]
