#!/bin/bash
#install module metadata
EXIFTOOL_VERSION=12.17
if [ "$RUNNER_OS" == "Windows" ]; then
  echo "TODO for windows"
else
  wget https://falcon.phy.queensu.ca/SNO/~phil/exiftool/Image-ExifTool-$EXIFTOOL_VERSION.tar.gz
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
  git clone git://github.com/smarnach/pyexiftool.git
  cd ./pyexiftool
  python ./setup.py install
  cd ..
  pip install -r ./src/modules/qrbcreader/requirements.txt
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

#install module imagerecognitiontensorflow
pip install -r ./src/modules/imagerecognitiontensorflow/requirements.txt

#install module zipextractor
pip install -r ./src/modules/zipextractor/requirements.txt

#install module qrreader
if [ "$RUNNER_OS" == "Linux" ]; then
  sudo apt-get install -y libzbar0
elif [ "$RUNNER_OS" == "macOS" ]; then
  brew install zbar
else
  echo "TODO for windows"
fi

pip install -r ./src/modules/qrbcreader/requirements.txt