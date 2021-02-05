FROM python:3.7.4-stretch

MAINTAINER Borja Pintos

#download
RUN git clone https://github.com/BorjaPintos/whatthefile.git

WORKDIR /whatthefile

#install basics requirements
RUN pip3.7 install -r requirementsunix.txt

#install module exiftool
ENV EXIFTOOL_VERSION 12.17
RUN wget https://www.sno.phy.queensu.ca/~phil/exiftool/Image-ExifTool-${EXIFTOOL_VERSION}.tar.gz && \
tar -xf Image-ExifTool-${EXIFTOOL_VERSION}.tar.gz && \
cd Image-ExifTool-${EXIFTOOL_VERSION} && \
perl Makefile.PL && \
make && \
make test && \
make install &&\
cd .. && \
git clone git://github.com/smarnach/pyexiftool.git && \
cd ./pyexiftool && \
python3.7 ./setup.py install && \
cd ..

#install module ocrtesseract
RUN apt update && apt install -y tesseract-ocr && \
pip3.7 install -r ./src/modules/ocrtesseract/requirements.txt --extra-index-url https://www.piwheels.hostedpi.com/simple

#install module imagerecognitiontensorflow
RUN pip3.7 install -r ./src/modules/imagerecognitiontensorflow/requirements.txt --extra-index-url https://www.piwheels.hostedpi.com/simple

#install module zipextractor
RUN pip3.7 install -r ./src/modules/zipextractor/requirements.txt

#install module qrreader
RUN apt install -y libzbar0 && \
pip3.7 install -r ./src/modules/qrbcreader/requirements.txt

#update system
RUN apt -y upgrade

EXPOSE 8443

CMD ["python3.7","application/web/runpro.py"]



