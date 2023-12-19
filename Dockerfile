# Use the official NVIDIA Deep Learning image as the base image
FROM nvcr.io/nvidia/dli/dli-nano-ai:v2.0.1-r32.5.0

# Install the 'jieba' Python package using pip3
RUN pip3 install jieba
RUN pip3 install paho-mqtt

# Additional configurations or commands if needed
# ...

# Set the working directory (optional)
# WORKDIR /app

# Define the command to run when the container starts (optional)
# CMD ["/bin/bash"]
