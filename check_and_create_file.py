import os

# Define the file path
file_path = "empty_file.txt"

# Check if file exists
if os.path.exists(file_path):
    print(f"File {file_path} already exists")
else:
    # Create empty file
    with open(file_path, 'w') as f:
        pass
    print(f"Created empty file {file_path}")
