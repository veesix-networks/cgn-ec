# Set python version
ARG BASE_CONTAINER=python:3.12.3-slim

# Set the base image 
FROM --platform=linux/amd64 $BASE_CONTAINER

# Adds metadata to image.
LABEL maintainer="cgn-ec@veesix-networks.co.uk"

# dont write pyc files
ENV PYTHONDONTWRITEBYTECODE 1
# dont buffer to stdout/stderr
ENV PYTHONUNBUFFERED 1

# Make a directory for app
WORKDIR /consumer

# Install dependencies
COPY requirements-consumer.txt .
RUN pip install --upgrade pip && pip install -r requirements-consumer.txt
# RUN pip install --no-cache-dir --user -r /req.txt

# Copy source code
COPY ./consumer .

# Run the application
CMD ["python", "-m", "app_single_process"]