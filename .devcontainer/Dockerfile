# Use official Python base image
FROM python:3.9-slim

# Install necessary dependencies
RUN apt-get update && apt-get install -y openjdk-11-jdk-headless && \
    apt-get clean

# Set environment variables
ENV PYSPARK_PYTHON=python3
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
ENV PATH=$JAVA_HOME/bin:$PATH

# Copy project files
WORKDIR /app
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Start the Flask service
CMD ["python", "src/app.py"]
