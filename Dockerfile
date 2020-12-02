FROM tensorflow/tensorflow

WORKDIR /app/
RUN pip install opencv-python
RUN pip install pillow
RUN  apt install -y libgl1-mesa-dev
COPY . /app/
CMD [ "python", "/app/src/train.py" ]