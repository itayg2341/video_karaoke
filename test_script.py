import json
import sys
import time
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import *

# Test basic functionality
def test_basic_functionality():
    print("Testing basic functionality...")
    
    # Test JSON loading
    try:
        with open('lyrics.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        print("✓ JSON loaded successfully")
        print(f"  Duration: {data['duration']}")
        print(f"  Segments: {len(data['segments'])}")
        print(f"  Language: {data.get('language', 'unknown')}")
    except Exception as e:
        print(f"✗ JSON loading failed: {e}")
        return False
    
    # Test image loading
    try:
        bg_img = Image.open('background.jpg')
        print(f"✓ Background image loaded: {bg_img.size}")
    except Exception as e:
        print(f"✗ Background image loading failed: {e}")
        return False
    
    # Test audio file
    try:
        audio = AudioFileClip('karaoke.wav')
        print(f"✓ Audio loaded: {audio.duration} seconds")
        audio.close()
    except Exception as e:
        print(f"✗ Audio loading failed: {e}")
        return False
    
    return True

if __name__ == '__main__':
    test_basic_functionality()
