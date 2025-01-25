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
WORKDIR /api

# Install dependencies
COPY requirements-api.txt .
RUN pip install --upgrade pip && pip install -r requirements-api.txt
# RUN pip install --no-cache-dir --user -r /req.txt

# Copy source code
COPY ./api .

# Run the application
CMD [ "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80", "--forwarded-allow-ips", "*" ]