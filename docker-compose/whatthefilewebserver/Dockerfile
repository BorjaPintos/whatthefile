FROM python:3.8-buster

MAINTAINER Borja Pintos

#download
RUN git clone https://github.com/BorjaPintos/whatthefile.git

WORKDIR /whatthefile


RUN pip3 install --upgrade pip
#install basics requirements
RUN pip3 install -r requirements.txt
RUN pip3 install -r requirementsunix.txt

#install module exiftool
ENV EXIFTOOL_VERSION 12.51
RUN curl --insecure https://exiftool.org/Image-ExifTool-${EXIFTOOL_VERSION}.tar.gz --output Image-ExifTool-${EXIFTOOL_VERSION}.tar.gz&& \
tar -xf Image-ExifTool-${EXIFTOOL_VERSION}.tar.gz && \
cd Image-ExifTool-${EXIFTOOL_VERSION} && \
perl Makefile.PL && \
make && \
make test && \
make install &&\
cd .. && \
git clone git://github.com/smarnach/pyexiftool.git && \
cd ./pyexiftool && \
python3 ./setup.py install && \
cd ..

#install module ocrtesseract
RUN apt update && apt install -y tesseract-ocr libgl1-mesa-glx

#install module qrreader
RUN apt install -y libzbar0

#install module whisper
RUN apt install -y ffmpeg

RUN sh installmodulesrequirements.sh

#update system
RUN apt -y upgrade

EXPOSE 8443
# uncomment if you dont use tika
#CMD ["python3.7","whatthefile.py", "whatthefile.ini", "/input"]
# uncomment if you use tika
CMD ["sh", "entrypoint.sh"] 


