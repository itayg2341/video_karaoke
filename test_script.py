import json
import sys
import time
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import *

# Test basic imports and functionality
print("Testing basic functionality...")

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
font = get_font(24)
print("✓ Font loading works")

# Test JSON loading
with open('lyrics.json', 'r', encoding='utf-8') as f:
    lyrics_data = json.load(f)
print(f"✓ JSON loading works, language: {lyrics_data['language']}")

# Test image loading
try:
    bg_image = Image.open('background.jpg')
    print(f"✓ Background image loading works, size: {bg_image.size}")
except Exception as e:
    print(f"✗ Background image loading failed: {e}")

print("Basic functionality test completed!")
