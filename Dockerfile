# Use the official NVIDIA Deep Learning image as the base image
FROM nvcr.io/nvidia/dli/dli-nano-ai:v2.0.1-r32.5.0

# Install Python 3.8
RUN apt-get update && \
    apt-get install -y python3.8 python3.8-distutils && \
    rm -rf /var/lib/apt/lists/* && \
    update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.8 1 && \
    update-alternatives --config python3 || true

# Install ffmpeg and other required packages
USER root
RUN apt-get update && \
    apt-get install -y \
    ffmpeg \
    libcanberra-gtk-module \
    libcanberra-gtk3-module \
    libgtk2.0-dev \
    pkg-config \
    || true

# Install pip
RUN python3.9.6 -m pip install --upgrade pip || true

# Install required Python packages
RUN python3 -m pip install \
    numpy \
    mediapipe \
    opencv-python-headless \
    paho-mqtt \
    SpeechRecognition \
    || true

# Alias 'python' to 'python3' and 'pip' to 'pip3'
ENV PATH="/root/.local/bin:${PATH}"

# Set the environment variable to display graphics
ENV DISPLAY=:0

# Set the GTK_MODULES environment variable
ENV GTK_MODULES=canberra-gtk-module

# Map the X11 socket directory from the host to the container
VOLUME /tmp/.X11-unix 

# Define the command to run when the container starts
CMD ["bash"] || true

# Add a version label
LABEL version="1.9"
