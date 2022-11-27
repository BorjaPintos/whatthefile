#!/bin/bash
#install module metadata
EXIFTOOL_VERSION=12.51
if [ "$RUNNER_OS" == "Windows" ]; then
  curl --output exiftool.zip --url https://exiftool.org/exiftool-$EXIFTOOL_VERSION.zip
  unzip -qq ./exiftool.zip -d "./exiftool"
  cp "./exiftool/exiftool(-k).exe" "./exiftool/exiftool.exe"
  echo "./exiftool/" >> $GITHUB_PATH
else
  wget https://exiftool.org/Image-ExifTool-$EXIFTOOL_VERSION.tar.gz --no-check-certificate
  tar -xf Image-ExifTool-$EXIFTOOL_VERSION.tar.gz
  cd Image-ExifTool-$EXIFTOOL_VERSION
  sudo perl Makefile.PL
  sudo make
  sudo make install
  if [ "$RUNNER_OS" == "macOS" ]; then
    sudo cp -r exiftool lib /usr/local/bin
  fi
  cd ..
fi

#install module ocrtesseract
if [ "$RUNNER_OS" == "Linux" ]; then
  sudo apt-get install -y tesseract-ocr
elif [ "$RUNNER_OS" == "macOS" ]; then
  brew install tesseract
else
  choco install tesseract --pre
  echo "C:\Program Files\Tesseract-OCR" >> $GITHUB_PATH
fi

#install module qrreader
if [ "$RUNNER_OS" == "Linux" ]; then
  sudo apt-get install -y libzbar0
elif [ "$RUNNER_OS" == "macOS" ]; then
  brew install zbar
fi

#strings
if [ "$RUNNER_OS" == "Windows" ]; then
  curl --output Strings.zip --url https://download.sysinternals.com/files/Strings.zip
  unzip -qq ./Strings.zip -d "./Strings"
  echo "./Strings/" >> $GITHUB_PATH
fi

sh ./installmodulesrequirements.sh


