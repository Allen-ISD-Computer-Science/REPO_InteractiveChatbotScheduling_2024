#!/bin/bash

# Halt on errors or undefined environment variables
set -eu

# Activate local python environment
source .venv/bin/activate

# Run main
PORT=$VAPOR_LOCAL_PORT python3 chatbot.py