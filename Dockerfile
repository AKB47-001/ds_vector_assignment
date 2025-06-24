# Use official lightweight Python image
FROM python:3.10-slim

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY src/ ./src/
WORKDIR /app/src

# Expose the default Flask port (adjust dynamically using env)
EXPOSE 5000

# Define environment variables for Flask
ENV FLASK_APP=node.py
ENV FLASK_RUN_HOST=0.0.0.0

# Run the application
CMD ["python", "node.py"]
