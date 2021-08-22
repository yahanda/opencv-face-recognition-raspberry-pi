﻿FROM balenalib/raspberrypi3-debian-python:3.7

RUN apt update && apt install -y libjpeg62-turbo libopenjp2-7 libtiff5 libatlas-base-dev libgl1-mesa-glx
RUN pip install --upgrade pip
RUN pip install absl-py six protobuf wrapt gast astor termcolor keras_applications keras_preprocessing --no-deps
RUN pip install numpy --extra-index-url 'https://www.piwheels.org/simple' --no-deps
RUN pip install flask pillow --index-url 'https://www.piwheels.org/simple'

# By default, we run manual image resizing to maintain parity with CVS webservice prediction results.
# If parity is not required, you can enable faster image resizing by uncommenting the following lines.
RUN echo "deb http://security.debian.org/debian-security jessie/updates main" >> /etc/apt/sources.list & apt update -y
RUN apt install -y zlib1g-dev libjpeg-dev gcc libglib2.0-bin libsm6 libxext6 libxrender1 libjasper-dev libpng16-16 libopenexr23 libgstreamer1.0-0 libavcodec58 libavformat58 libswscale5 libqtgui4 libqt4-test libqtcore4 libgtk-3-0 libhdf5-103
RUN pip install opencv-contrib-python --extra-index-url 'https://www.piwheels.org/simple'

COPY app /app

# Expose the port
EXPOSE 80

# Set the working directory
WORKDIR /app

# Run the flask server for the endpoints
CMD python -u app.py