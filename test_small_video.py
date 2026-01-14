import json
import time
from PIL import Image
import numpy as np
from moviepy.editor import *

# Create a small test dataset
small_lyrics = {
    "language": "en",
    "duration": 5.0,
    "segments": [
        {
            "start": 0.0,
            "end": 2.5,
            "words": [
                {"word": "Hello", "start": 0.0, "end": 1.0},
                {"word": "world", "start": 1.0, "end": 2.5}
            ]
        },
        {
            "start": 2.5,
            "end": 5.0,
            "words": [
                {"word": "This", "start": 2.5, "end": 3.5},
                {"word": "is", "start": 3.5, "end": 4.0},
                {"word": "test", "start": 4.0, "end": 5.0}
            ]
        }
    ]
}

# Save small test data
with open('small_lyrics.json', 'w') as f:
    json.dump(small_lyrics, f)

# Create small background image
bg = Image.new('RGB', (640, 480), color='blue')
bg.save('small_bg.jpg')

print("Testing with small dataset...")
start_time = time.time()

# Test the optimized app
import subprocess
result = subprocess.run([
    'python3', 'app.py', 'small_lyrics.json', 'small_bg.jpg', 
    'small_test.mp4'
], capture_output=True, text=True)

end_time = time.time()
print(f"Video generation took: {end_time - start_time:.2f} seconds")
print(f"Return code: {result.returncode}")
if result.stdout:
    print(f"Output: {result.stdout}")
if result.stderr:
    print(f"Errors: {result.stderr}")

# Check if file was created
import os
if os.path.exists('small_test.mp4'):
    file_size = os.path.getsize('small_test.mp4')
    print(f"✓ Video created successfully! Size: {file_size} bytes")
else:
    print("❌ Video file was not created")
