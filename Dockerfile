FROM python

RUN python3 -m pip install -U pip
RUN apt update
RUN apt install ffmpeg libsm6 libxext6  -y

ENV DEBIAN_FRONTEND noninteractive

RUN yes | apt install default-jdk
RUN python3 -m pip install opencv-python
RUN python3 -m pip install --upgrade Pillow
RUN python3 -m pip install zxing

 WORKDIR /var/www