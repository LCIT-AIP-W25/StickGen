# Base image with CUDA support for running Diffusion model
FROM nvidia/cuda:12.2.0-base-ubuntu20.04

# Environment setup
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1
ENV FLASH_ATTENTION_FORCE_DISABLED=1  # Prevent flash attention errors

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3 python3-pip git wget curl \
    && apt-get clean

# Copy and install Python requirements
COPY requirements.txt .
RUN pip3 install --upgrade pip && pip3 install -r requirements.txt

#  Install Redis Python client
RUN pip3 install redis

# Copy your backend application code
COPY . /app
WORKDIR /app

# Expose the port Flask runs on
EXPOSE 5001

# Run your app
CMD ["python3", "app.py"]
