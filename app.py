import json
import sys
import time
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import *

# Cache the font globally to avoid reloading
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

def draw_lyrics_on_frame(frame, words_to_show, fontsize, screen_width, screen_height, is_rtl, font):
    """Draw lyrics on a frame using PIL with optimized text outline"""
    # Convert numpy array to PIL Image
    img = Image.fromarray(frame.astype('uint8'))
    draw = ImageDraw.Draw(img)
    
    if not words_to_show:
        return np.array(img)
    
    # Calculate text layout
    y_pos = screen_height - 100
    
    # Calculate total width
    spacing = 20
    total_width = 0
    word_widths = []
    
    for word_text, is_highlight in words_to_show:
        bbox = draw.textbbox((0, 0), word_text, font=font)
        width = bbox[2] - bbox[0]
        word_widths.append(width)
        total_width += width + spacing
    
    # Center position
    start_x = max(10, (screen_width - total_width) / 2)
    current_x = start_x
    
    # Draw words with simplified outline (only 8 directions instead of 25)
    if is_rtl:
        # RTL: draw from right to left
        current_x = start_x + total_width
        for (word_text, is_highlight), width in zip(words_to_show, word_widths):
            current_x -= width
            color = (255, 255, 0) if is_highlight else (169, 169, 169)  # Yellow or gray
            # Draw outline in 8 directions only (faster)
            for adj_x, adj_y in [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]:
                draw.text((current_x + adj_x, y_pos + adj_y), word_text, font=font, fill=(0, 0, 0))
            # Draw text on top
            draw.text((current_x, y_pos), word_text, font=font, fill=color)
            current_x -= spacing
    else:
        # LTR: draw from left to right
        for (word_text, is_highlight), width in zip(words_to_show, word_widths):
            color = (255, 255, 0) if is_highlight else (169, 169, 169)  # Yellow or gray
            # Draw outline in 8 directions only (faster)
            for adj_x, adj_y in [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]:
                draw.text((current_x + adj_x, y_pos + adj_y), word_text, font=font, fill=(0, 0, 0))
            # Draw text on top
            draw.text((current_x, y_pos), word_text, font=font, fill=color)
            current_x += width + spacing
    
    return np.array(img)


def main(json_file, background_image, output_video, audio_file=None):
    start_time = time.time()
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    duration = data['duration']
    segments = data['segments']
    is_rtl = data.get('language') == 'he'
    
    # Load background image
    bg_img = Image.open(background_image)
    screen_width, screen_height = 1920, 1080
    bg_img = bg_img.resize((screen_width, screen_height))
    bg_array = np.array(bg_img)
    
    # Create a mapping of time -> words to display
    fontsize = 45
    fps = 24
    total_frames = int(duration * fps)
    
    # Get cached font once
    font = get_font(fontsize)
    
    # Create video by drawing on each frame
    print("Creating frames with lyrics...")
    frames = []
    
    for frame_idx in range(total_frames):
        if frame_idx % 100 == 0:
            print(f"  Frame {frame_idx}/{total_frames}")
        
        current_time = frame_idx / fps
        
        # Start with background
        frame = bg_array.copy()
        
        # Find all words that should be shown at this time
        words_to_show = []
        for segment in segments:
            segment_start = segment['start']
            segment_end = segment['end']
            
            if segment_start <= current_time < segment_end:
                # This segment is active
                for word_data in segment.get('words', []):
                    word_text = word_data['word']
                    word_start = word_data['start']
                    word_end = word_data['end']
                    
                    # Check if word should be highlighted or just shown
                    is_highlight = word_start <= current_time < word_end
                    words_to_show.append((word_text, is_highlight))
        
        # Draw lyrics on this frame
        if words_to_show:
            frame = draw_lyrics_on_frame(frame, words_to_show, fontsize, screen_width, screen_height, is_rtl, font)
        
        frames.append(frame)
    
    print("Creating video clip from frames...")
    # Create video clip from frames
    video = ImageSequenceClip(frames, fps=fps)
    
    # Add audio if provided
    if audio_file:
        print(f"Adding audio from {audio_file}")
        audio = AudioFileClip(audio_file)
        video = video.set_audio(audio)
    
    # Write video file with faster encoding
    print(f"Writing video: {output_video}")
    video.write_videofile(
        output_video,
        fps=fps,
        codec='libx264',
        audio_codec=None,
        verbose=False,
        logger=None
    )
    
    # Calculate and print elapsed time
    end_time = time.time()
    elapsed_time = end_time - start_time
    hours = int(elapsed_time // 3600)
    minutes = int((elapsed_time % 3600) // 60)
    seconds = int(elapsed_time % 60)
    print(f"\n✓ Video created successfully!")
    print(f"  Total time: {hours}h {minutes}m {seconds}s")


if __name__ == '__main__':
    if len(sys.argv) < 4:
        print("Usage: python app.py lyrics.json background.jpg output.mp4 [audio.mp3]")
        sys.exit(1)
    
    json_file = sys.argv[1]
    bg_image = sys.argv[2]
    out_video = sys.argv[3]
    audio = sys.argv[4] if len(sys.argv) > 4 else None
    
    main(json_file, bg_image, out_video, audio)