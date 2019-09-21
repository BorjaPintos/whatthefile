FROM python:3.7.4-stretch

MAINTAINER Borja Pintos

#download
RUN git clone https://github.com/BorjaPintos/whatthefile.git

WORKDIR /whatthefile

#install basics requirements
RUN pip3.7 install -r requirements.txt

#install module exiftool
RUN wget https://www.sno.phy.queensu.ca/~phil/exiftool/Image-ExifTool-11.65.tar.gz && \
tar -xf Image-ExifTool-11.65.tar.gz && \
cd Image-ExifTool-11.65 && \
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
pip3.7 install -r ./modules/ocrtesseract/requirements.txt

#install module imagerecognitiontensorflow
RUN pip3.7 install -r ./modules/imagerecognitiontensorflow/requirements.txt

#update system
RUN apt -y upgrade

EXPOSE 8080

CMD ["python3.7","analisisFicherosServer.py"]



