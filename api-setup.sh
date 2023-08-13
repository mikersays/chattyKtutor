#!/bin/bash

# Ask the user for their API key
echo "Please enter your OpenAI API key:"
read API_KEY

# Use sed to replace the placeholder with the actual API key in chattytutor.py
sed -i "s/<API key>/$API_KEY/g" chattytutor.py

echo "API key set successfully!"

# Install Python packages from requirements.txt
echo "Installing required Python packages from requirements.txt..."
pip install -r requirements.txt

echo "Setup completed successfully!"
