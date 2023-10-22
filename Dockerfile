FROM nvcr.io/nvidia/pytorch:23.03-py3

ENV SERVING_PORT=8125

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copy all contents of current folder to /workspace in the container
COPY . .

EXPOSE $SERVING_PORT

CMD ["python", "server.py", "--serving-port", "$SERVING_PORT"]

#build using
# docker build -t stable-diffusion-server .

# run using
# docker run -p 8125:8125 --gpus=all stable-diffusion-server