import os
import glob

def check_text_file():
    # Check for any .txt files in root directory
    txt_files = glob.glob("*.txt")
    
    if txt_files:
        print("Found text files:")
        for file in txt_files:
            print(f"  - {file}")
            # Check if file is empty
            if os.path.getsize(file) == 0:
                print(f"    File is empty")
            else:
                print(f"    File size: {os.path.getsize(file)} bytes")
    else:
        print("No text files found in root directory")

if __name__ == "__main__":
    check_text_file()
