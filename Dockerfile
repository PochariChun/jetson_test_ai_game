# Use the official NVIDIA Deep Learning image as the base image
FROM nvcr.io/nvidia/dli/dli-nano-ai:v2.0.1-r32.5.0

# Install the 'jieba' and 'paho-mqtt' Python packages using pip3
RUN pip3 install jieba
RUN pip3 install paho-mqtt

# Alias 'python' to 'python3' and 'pip' to 'pip3'
RUN echo 'alias python=python3' >> ~/.bashrc
RUN echo 'alias pip=pip3' >> ~/.bashrc

# Source the .bashrc to activate the aliases
RUN source ~/.bashrc || true

# Install ffmpeg (you can use the package manager available in the base image)
RUN apt-get install -y ffmpeg || true

# Define the command to run when the container starts
CMD ["docker", "run", "--runtime", "nvidia", "-it", "--rm", "--network", "host", \
    "--volume", "~/nvdli-data:/nvdli-nano/data", "--device", "/dev/video0", \
    "nvcr.io/nvidia/dli/dli-nano-ai:v2.0.1-r32.5.0"]

# Add a version label
LABEL version="1.0"
