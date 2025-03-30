#!/bin/bash

# Check if a filename pattern is provided
if [ -z "$1" ]; then
    echo "Usage: $0 <file_pattern>"
    exit 1
fi

# Loop through matching files
for file in $1; do
    if [ -f "$file" ]; then
        echo "Processing file: $file"
        timescaledb-parallel-copy --table "session_mapping" --file $file --workers 16 --verbose --connection "user=postgres sslmode=disable dbname=cgnat"
        echo "Finished processing: $file"
    else
        echo "No matching files found for pattern: $1"
    fi
done