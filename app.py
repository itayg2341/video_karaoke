#!/usr/bin/env python3
"""
Karaoke Video Generator

Creates karaoke videos with synchronized lyrics display.
Optimized for performance and memory usage.
"""

import json
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import *
import os

# Font cache for performance
_font_cache = {}

def get_font(fontsize):
    """Get cached font to avoid reloading with proper error handling"""
    if fontsize not in _font_cache:
        try:
            _font_cache[fontsize] = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", fontsize)
        except (OSError, IOError):
            try:
                _font_cache[fontsize] = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", fontsize)
            except (OSError, IOError):
                _font_cache[fontsize] = ImageFont.load_default()
    return _font_cache[fontsize]

def draw_lyrics_on_frame(frame, words_to_show, fontsize, screen_width, screen_height, is_rtl, font):
    """Draw lyrics on a frame using PIL with optimized text outline"""
    pil_image = Image.fromarray(frame)
    draw = ImageDraw.Draw(pil_image)
    
    # Calculate text positioning
    y_position = screen_height - 150
    x_center = screen_width // 2
    
    # Process words for display
    display_words = []
    for word_text, is_highlight in words_to_show:
        color = (255, 255, 0) if is_highlight else (255, 255, 255)
        display_words.append((word_text, color))
    
    # Join words with spaces
    full_text = ' '.join(word for word, _ in display_words)
    
    # Calculate text size and position
    bbox = draw.textbbox((0, 0), full_text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    x_position = x_center - text_width // 2
    y_position = y_position - text_height // 2
    
    # Draw text outline for better visibility
    outline_color = (0, 0, 0)
    outline_width = 2
    
    # Draw outline
    for dx in range(-outline_width, outline_width + 1):
        for dy in range(-outline_width, outline_width + 1):
            if dx != 0 or dy != 0:
                draw.text((x_position + dx, y_position + dy), full_text, 
                         fill=outline_color, font=font)
    
    # Draw main text
    draw.text((x_position, y_position), full_text, 
             fill=(255, 255, 255), font=font)
    
    return np.array(pil_image)

def build_lyrics_index(segments):
    """Build an optimized index for fast lyrics lookup by time"""
    time_index = {}
    
    for segment_idx, segment in enumerate(segments):
        segment_start = segment['start']
        segment_end = segment['end']
        
        # Index by second for fast lookup
        start_second = int(segment_start)
        end_second = int(segment_end) + 1
        
        for second in range(start_second, end_second + 1):
            if second not in time_index:
                time_index[second] = []
            time_index[second].append(segment_idx)
    
    return time_index

def get_words_for_time(segments, time_index, current_time):
    """Get words to display for current time using optimized index"""
    words_to_show = []
    
    # Get current second for index lookup
    current_second = int(current_time)
    
    # Get candidate segments from index
    candidate_segments = time_index.get(current_second, [])
    
    # Check only relevant segments
    for segment_idx in candidate_segments:
        segment = segments[segment_idx]
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
    
    return words_to_show

def make_frame(t, background_image, segments, time_index, fontsize, screen_width, screen_height, is_rtl, font):
    """Generate a single frame with lyrics"""
    # Start with background
    frame = background_image.copy()
    
    # Get words for current time
    words_to_show = get_words_for_time(segments, time_index, t)
    
    # Draw lyrics on frame
    if words_to_show:
        frame = draw_lyrics_on_frame(frame, words_to_show, fontsize, 
                                   screen_width, screen_height, is_rtl, font)
    
    return frame

def main(json_file, background_image, output_video, audio_file=None):
    """Main function to create karaoke video with optimizations"""
    print("Loading lyrics data...")
    with open(json_file, 'r') as f:
        lyrics_data = json.load(f)
    
    segments = lyrics_data['segments']
    duration = lyrics_data['duration']
    language = lyrics_data.get('language', 'en')
    is_rtl = language in ['ar', 'he', 'fa', 'ur']
    
    print(f"Building lyrics index for {len(segments)} segments...")
    time_index = build_lyrics_index(segments)
    
    print("Loading background image...")
    background = ImageClip(background_image)
    screen_width, screen_height = background.size
    
    # Set up font
    fontsize = 45
    font = get_font(fontsize)
    
    print("Creating video generator...")
    
    # Create video clip using generator function instead of storing all frames
    def frame_generator(t):
        return make_frame(t, background.get_frame(t), segments, time_index, 
                         fontsize, screen_width, screen_height, is_rtl, font)
    
    # Create video clip with generator
    video = VideoClip(frame_generator, duration=duration)
    
    # Set fps
    video = video.set_fps(24)
    
    # Add audio if provided
    if audio_file and os.path.exists(audio_file):
        print("Adding audio...")
        audio = AudioFileClip(audio_file)
        video = video.set_audio(audio)
    
    print("Writing video file...")
    video.write_videofile(
        output_video,
        codec='libx264',
        audio_codec='aac' if audio_file else None,
        temp_audiofile='temp-audio.m4a',
        remove_temp=True,
        logger=None  # Reduce output verbosity
    )
    
    print(f"Video saved to: {output_video}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 4:
        print("Usage: python app.py <lyrics.json> <background.jpg> <output.mp4> [audio.wav]")
        sys.exit(1)
    
    json_file = sys.argv[1]
    background_image = sys.argv[2]
    output_video = sys.argv[3]
    audio_file = sys.argv[4] if len(sys.argv) > 4 else None
    
    main(json_file, background_image, output_video, audio_file)
