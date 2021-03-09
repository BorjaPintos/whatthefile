#!/bin/bash

#install module certificatereader
pip install -r ./src/modules/certificatereader/requirements.txt

#install module evtxreader
pip install -r ./src/modules/evtxreader/requirements.txt

#install module imagerecognitiontensorflow
pip install -r ./src/modules/imagerecognitiontensorflow/requirements.txt

#install module metadata
EXIFTOOL_VERSION=12.18
if [ "$RUNNER_OS" == "Windows" ]; then
  echo "TODO for windows"
else
  wget https://exiftool.org/Image-ExifTool-$EXIFTOOL_VERSION.tar.gz --no-check-certificate
  tar -xf Image-ExifTool-$EXIFTOOL_VERSION.tar.gz
  cd Image-ExifTool-$EXIFTOOL_VERSION
  sudo perl Makefile.PL
  sudo make
  #sudo make test
  sudo make install
  if [ "$RUNNER_OS" == "macOS" ]; then
    sudo cp -r exiftool lib /usr/local/bin
  fi
  cd ..
  pip install -r ./src/modules/metadata/requirements.txt
fi

#install module ocrtesseract
if [ "$RUNNER_OS" == "Linux" ]; then
  sudo apt-get install -y tesseract-ocr
elif [ "$RUNNER_OS" == "macOS" ]; then
  brew install tesseract
else
  echo "TODO for windows"
fi
pip install -r ./src/modules/ocrtesseract/requirements.txt


#install module pstostparser
pip install -r ./src/modules/pstostparser/requirements.txt

#install module qrreader
if [ "$RUNNER_OS" == "Linux" ]; then
  sudo apt-get install -y libzbar0
elif [ "$RUNNER_OS" == "macOS" ]; then
  brew install zbar
else
  echo "TODO for windows"
fi

pip install -r ./src/modules/qrbcreader/requirements.txt

#install module tikaparser
pip install -r ./src/modules/tikaparser/requirements.txt

#install module windowsprefetch
pip install -r ./src/modules/windowsprefetch/requirements.txt

#install module windowsregistry
pip install -r ./src/modules/windowsregistry/requirements.txt

#install module zipextractor
pip install -r ./src/modules/zipextractor/requirements.txt


