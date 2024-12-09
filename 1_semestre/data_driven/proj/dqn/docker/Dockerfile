FROM pytorch/pytorch:2.2.0-cuda12.1-cudnn8-runtime

WORKDIR /src
RUN apt-get update && apt-get install -y libsm6 libxext6 \
       apt-utils \
       build-essential \
       curl \
       xvfb \
       ffmpeg \
       xorg-dev \
       libsdl2-dev \
       swig \
       cmake
RUN apt-get install -y mesa-utils libgl1-mesa-glx libgl1-mesa-dri python3-opengl
RUN pip install --upgrade setuptools
COPY ./requirements.txt .
RUN pip install -r requirements.txt && rm requirements.txt

# CMD [python -m debugpy --listen localhost:5678 --wait-for-client main.py]