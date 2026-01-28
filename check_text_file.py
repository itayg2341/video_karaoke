import os

def check_text_file():
    """Check if there is any text file in the root directory"""
    files = os.listdir('.')
    text_files = [f for f in files if f.endswith('.txt')]
    
    if text_files:
        print(f"Found text file(s): {text_files}")
        return True
    else:
        print("No text files found in root directory")
        return False

if __name__ == '__main__':
    check_text_file()
