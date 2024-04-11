#!/bin/bash

# Check if at least one argument is provided
if [ $# -eq 0 ]; then
  echo "Usage: $0 test_image_url"
  exit 1
fi

# Assign the argument to test_image_url variable
test_image_url="$1"

# Run your Python script with the argument
python main.py "$test_image_url"

echo "Script execution completed."
