import json
import sys
import time
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import *
import app

# Test the main functions
print("Testing font caching...")
font = app.get_font(45)
print(f"Font loaded: {font}")

print("Testing lyrics data loading...")
with open('lyrics.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
print(f"Lyrics data loaded: {len(data['segments'])} segments")

print("Testing background image loading...")
bg_img = Image.open('background.jpg')
print(f"Background image size: {bg_img.size}")

print("All basic tests passed!")
