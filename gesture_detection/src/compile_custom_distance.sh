#!/bin/bash

# Run setup.py from the cpp directory
python3 cpp/setup.py build_ext --inplace

# Check if the build was successful
if [ $? -ne 0 ]; then
    echo "Build failed."
    exit 1
fi

echo "Build process completed!"