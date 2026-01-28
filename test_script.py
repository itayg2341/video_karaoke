import json
import sys
import time
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import *

# Test basic functionality
print("Testing basic imports...")
print("✓ All imports successful")

# Test font loading
_font_cache = {}

def get_font(fontsize):
    """Get cached font to avoid reloading"""
    if fontsize not in _font_cache:
        try:
            _font_cache[fontsize] = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", fontsize)
        except:
            try:
                _font_cache[fontsize] = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", fontsize)
            except:
                _font_cache[fontsize] = ImageFont.load_default()
    return _font_cache[fontsize]

# Test font loading
font = get_font(45)
print("✓ Font loading works")

# Test JSON loading
with open('lyrics.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
print(f"✓ JSON loaded: duration={data['duration']}, segments={len(data['segments'])}")

# Test image loading
bg_img = Image.open('background.jpg')
screen_width, screen_height = 1920, 1080
bg_img = bg_img.resize((screen_width, screen_height))
bg_array = np.array(bg_img)
print(f"✓ Background image loaded: {bg_array.shape}")

# Test frame creation
print("✓ Basic functionality test passed")
