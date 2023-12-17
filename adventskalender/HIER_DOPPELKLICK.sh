#!/bin/bash

# Get the current script's directory
script_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Change to the script's directory
cd "$script_dir"

# Start the Python program
python ./kalender.py
