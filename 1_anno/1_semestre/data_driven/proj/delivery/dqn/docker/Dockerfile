FROM pytorch/pytorch:2.2.0-cuda12.1-cudnn8-runtime

WORKDIR /src
COPY ./requirements.txt .
RUN pip install -r requirements.txt && rm requirements.txt