FROM python

RUN python3 -m pip install -U pip
RUN apt update
RUN apt install ffmpeg libsm6 libxext6  -y
RUN python3 -m pip install --upgrade Pillow
RUN python3 -m pip install pdf417decoder

WORKDIR /var/www
