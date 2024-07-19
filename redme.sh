#!/bin/bash

# Function to recursively traverse directories and generate README.md content with image paths
generate_readme() {
    local current_dir=$1
    local indent=$2
    local readme_content=""

    for entry in "$current_dir"/*; do
        if [ -d "$entry" ]; then
            local dirname=$(basename "$entry")
            readme_content+="${indent}├── ${dirname}\n"
            readme_content+=$(generate_readme "$entry" "    $indent")
        elif [[ "$entry" =~ \.(jpg|jpeg|png|gif)$ ]]; then
            local filepath="${entry#./}"
            readme_content+="${indent}│   ├── ![Alt text](${filepath})\n"
        fi
    done

    echo -e "$readme_content"
}

# Start of the script
base_dir="."
readme_file="README.md"

# Initialize README.md content
echo -e "# Directory Structure with Images\n" > "$readme_file"
echo -e "README.md\n└── allinone\n$(generate_readme "allinone" "    ")\n" >> "$readme_file"

echo "README.md file has been generated."

