import os

# Check if empty.txt exists in root directory
if os.path.exists("empty.txt"):
    print("empty.txt exists in root directory")
    # Check if it's empty
    if os.path.getsize("empty.txt") == 0:
        print("empty.txt is empty")
    else:
        print("empty.txt is not empty")
else:
    print("ERROR: empty.txt does not exist in root directory")
