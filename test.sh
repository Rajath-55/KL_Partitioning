#!/bin/bash

# Change to the App directory
cd ./App

# Loop over all files in the directory
for file in *
do
    # Check if it is a file (not a directory)
    if [[ -f $file ]]; then
        # Print the filename
        echo $file
    fi
done

