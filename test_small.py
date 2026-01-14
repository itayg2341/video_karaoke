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

# Test font
font = get_font(45)
print("✓ Font loading works")

# Test image creation
img = Image.new('RGB', (100, 100), color='red')
arr = np.array(img)
print("✓ Image conversion works")

print("✓ All basic tests passed")
