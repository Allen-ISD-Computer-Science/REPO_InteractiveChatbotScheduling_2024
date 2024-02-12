#!/bin/bash

# Halt on errors or undefined environment variables
set -eu

# Create local python environment
python3 -m venv .venv
source .venv/bin/activate

# Install required packages
python3 -m pip install \
   nltk \
   flask \
   pandas \
   datetime \
   
    