import json
import time
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import ImageSequenceClip

# Load data
with open('lyrics.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Load background image
bg_img = Image.open('background.jpg')
screen_width, screen_height = 1920, 1080
bg_img = bg_img.resize((screen_width, screen_height))
bg_array = np.array(bg_img)

# Test parameters
fontsize = 45
fps = 24
test_frames = 10  # Just test 10 frames

# Get font
_font_cache = {}
def get_font(fontsize):
    if fontsize not in _font_cache:
        try:
            _font_cache[fontsize] = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", fontsize)
        except:
            try:
                _font_cache[fontsize] = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", fontsize)
            except:
                _font_cache[fontsize] = ImageFont.load_default()
    return _font_cache[fontsize]

font = get_font(fontsize)

# Test frame creation
print(f"Testing {test_frames} frames...")
frames = []

for frame_idx in range(test_frames):
    current_time = frame_idx / fps
    frame = bg_array.copy()
    
    # Find words to show (simplified logic)
    words_to_show = []
    for segment in data['segments'][:1]:  # Just first segment
        if segment['start'] <= current_time < segment['end']:
            for word_data in segment.get('words', []):
                word_text = word_data['word']
                word_start = word_data['start']
                word_end = word_data['end']
                is_highlight = word_start <= current_time < word_end
                words_to_show.append((word_text, is_highlight))
    
    # Simple text drawing test
    if words_to_show:
        img = Image.fromarray(frame.astype('uint8'))
        draw = ImageDraw.Draw(img)
        y_pos = screen_height - 100
        
        # Test drawing one word
        word_text, is_highlight = words_to_show[0]
        color = (255, 255, 0) if is_highlight else (169, 169, 169)
        draw.text((100, y_pos), word_text, font=font, fill=color)
        frame = np.array(img)
    
    frames.append(frame)

print(f"✓ Created {len(frames)} test frames")
print("✓ Small test completed successfully")
