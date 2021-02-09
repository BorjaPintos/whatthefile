#!/bin/bash

python -m pip install --upgrade pip
if [ "$RUNNER_OS" == "Windows" ]; then
  pip install -r requirementswindows.txt
elif [ "$RUNNER_OS" == "macOS" ]; then
  brew install libmagic
  pip install -r requirementsunix.txt
else
  pip install -r requirementsunix.txt
fi