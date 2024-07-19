#!/bin/bash

# Function to recursively traverse directories and gather image paths
gather_image_paths() {
    local current_dir=$1
    local image_paths=""

    for entry in "$current_dir"/*; do
        if [ -d "$entry" ]; then
            image_paths+=$(gather_image_paths "$entry")
        elif [[ "$entry" =~ \.(jpg|jpeg|png|gif)$ ]]; then
            local filepath="${entry#./}"
            image_paths+="![Alt text](${filepath})\n"
        fi
    done

    echo -e "$image_paths"
}

# Start of the script
readme_file="README.md"

# Initialize README.md content
echo -e "# Image Paths\n" > "$readme_file"
echo -e "$(gather_image_paths ".")" >> "$readme_file"

echo "README.md file has been generated."
