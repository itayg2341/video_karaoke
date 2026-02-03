import json
import sys
import time
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import *
import os
import gc

def get_font(fontsize):
    """Get font with fallback options"""
    try:
        # Try to use a system font that supports Hebrew/Arabic
        font = ImageFont.truetype("DejaVuSans.ttf", fontsize)
    except:
        try:
            font = ImageFont.truetype("arial.ttf", fontsize)
        except:
            # Fallback to default font
            font = ImageFont.load_default()
    return font

def draw_lyrics_on_frame(frame, words_to_show, fontsize, screen_width, screen_height, is_rtl, font):
    """Draw lyrics on a single frame"""
    img = Image.fromarray(frame)
    draw = ImageDraw.Draw(img)
    
    # Calculate text positioning
    line_height = fontsize + 10
    y_position = screen_height - 200  # Position from bottom
    
    # Group words by line (simple approach)
    lines = []
    current_line = []
    current_width = 0
    max_width = screen_width - 100  # Leave margins
    
    for word_text, is_highlight in words_to_show:
        # Estimate word width (rough approximation)
        word_width = len(word_text) * fontsize * 0.6
        
        if current_width + word_width > max_width and current_line:
            lines.append(current_line)
            current_line = []
            current_width = 0
        
        current_line.append((word_text, is_highlight))
        current_width += word_width + fontsize * 0.3  # Add space between words
    
    if current_line:
        lines.append(current_line)
    
    # Draw lines from bottom up
    for line_idx, line in enumerate(reversed(lines[-3:])):  # Show max 3 lines
        line_y = y_position - (line_idx * line_height)
        
        # Calculate total line width for centering
        total_width = sum(len(word) * fontsize * 0.6 for word, _ in line) + \
                     (len(line) - 1) * fontsize * 0.3
        
        x_position = (screen_width - total_width) // 2
        
        # Draw each word in the line
        for word_text, is_highlight in line:
            color = (255, 255, 0) if is_highlight else (255, 255, 255)  # Yellow for highlight, white for normal
            
            # Add text outline for better visibility
            outline_color = (0, 0, 0)
            
            # Draw outline (multiple offsets)
            for dx in [-2, 2]:
                for dy in [-2, 2]:
                    draw.text((x_position + dx, line_y + dy), word_text, font=font, fill=outline_color)
            
            # Draw main text
            draw.text((x_position, line_y), word_text, font=font, fill=color)
            
            # Update x position for next word
            word_width = len(word_text) * fontsize * 0.6
            x_position += word_width + fontsize * 0.3
    
    return np.array(img)

def create_karaoke_video(json_file, background_image, output_video, audio_file=None):
    """Create karaoke video with improved performance and memory management"""
    start_time = time.time()
    
    try:
        # Validate input files
        if not os.path.exists(json_file):
            raise FileNotFoundError(f"JSON file not found: {json_file}")
        if not os.path.exists(background_image):
            raise FileNotFoundError(f"Background image not found: {background_image}")
        if audio_file and not os.path.exists(audio_file):
            raise FileNotFoundError(f"Audio file not found: {audio_file}")
        
        # Load and validate JSON data
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if 'duration' not in data or 'segments' not in data:
            raise ValueError("Invalid JSON format: missing 'duration' or 'segments'")
        
        duration = float(data['duration'])
        segments = data['segments']
        is_rtl = data.get('language') == 'he'
        
        print(f"Video duration: {duration:.2f} seconds")
        print(f"Number of segments: {len(segments)}")
        print(f"Language: {'RTL' if is_rtl else 'LTR'}")
        
        # Load and prepare background image
        print("Loading background image...")
        bg_img = Image.open(background_image)
        screen_width, screen_height = 1920, 1080
        
        # Ensure background image is properly sized
        if bg_img.size != (screen_width, screen_height):
            print(f"Resizing background from {bg_img.size} to {screen_width}x{screen_height}")
            bg_img = bg_img.resize((screen_width, screen_height), Image.Resampling.LANCZOS)
        
        bg_array = np.array(bg_img)
        bg_img.close()  # Free memory
        
        # Video parameters
        fontsize = 45
        fps = 24
        total_frames = int(duration * fps)
        
        # Get font
        font = get_font(fontsize)
        
        # Pre-process segments for faster lookup
        print("Pre-processing segments...")
        segment_lookup = []
        for segment in segments:
            segment_start = float(segment['start'])
            segment_end = float(segment['end'])
            
            words = []
            for word_data in segment.get('words', []):
                words.append({
                    'text': word_data['word'],
                    'start': float(word_data['start']),
                    'end': float(word_data['end'])
                })
            
            segment_lookup.append({
                'start': segment_start,
                'end': segment_end,
                'words': words
            })
        
        # Create video clip using generator for memory efficiency
        print("Creating video frames...")
        
        def make_frame(t):
            """Generate frame at time t"""
            frame = bg_array.copy()
            
            # Find words to show at this time
            words_to_show = []
            for segment in segment_lookup:
                if segment['start'] <= t < segment['end']:
                    for word in segment['words']:
                        is_highlight = word['start'] <= t < word['end']
                        words_to_show.append((word['text'], is_highlight))
            
            # Draw lyrics if needed
            if words_to_show:
                frame = draw_lyrics_on_frame(frame, words_to_show, fontsize, screen_width, screen_height, is_rtl, font)
            
            return frame
        
        # Create video clip
        print("Generating video...")
        video = VideoClip(make_frame, duration=duration)
        
        # Add audio if provided
        if audio_file:
            print(f"Adding audio: {audio_file}")
            audio = AudioFileClip(audio_file)
            
            # Validate audio duration matches video duration
            if abs(audio.duration - duration) > 1.0:
                print(f"Warning: Audio duration ({audio.duration:.2f}s) differs from video duration ({duration:.2f}s)")
            
            video = video.set_audio(audio)
        
        # Write video file with optimized settings
        print(f"Writing video: {output_video}")
        video.write_videofile(
            output_video,
            fps=fps,
            codec='libx264',
            audio_codec='aac' if audio_file else None,
            preset='medium',  # Balance between speed and quality
            threads=4,  # Use multiple threads
            verbose=False,
            logger=None
        )
        
        # Clean up resources
        video.close()
        if audio_file:
            audio.close()
        
        # Force garbage collection
        gc.collect()
        
        # Calculate elapsed time
        end_time = time.time()
        elapsed_time = end_time - start_time
        hours = int(elapsed_time // 3600)
        minutes = int((elapsed_time % 3600) // 60)
        seconds = int(elapsed_time % 60)
        
        print(f"\n✓ Video created successfully!")
        print(f"  Output: {output_video}")
        print(f"  Processing time: {hours}h {minutes}m {seconds}s")
        print(f"  Processing speed: {duration/elapsed_time:.2f}x real-time")
        
        return True
        
    except Exception as e:
        print(f"\n✗ Error creating video: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    finally:
        # Ensure all resources are cleaned up
        gc.collect()

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print("Usage: python app_improved.py lyrics.json background.jpg output.mp4 [audio.mp3]")
        print("\nThis improved version includes:")
        print("  - Better memory management")
        print("  - Error handling and validation")
        print("  - Performance optimizations")
        print("  - Resource cleanup")
        print("  - Progress indicators")
        sys.exit(1)
    
    json_file = sys.argv[1]
    bg_image = sys.argv[2]
    out_video = sys.argv[3]
    audio = sys.argv[4] if len(sys.argv) > 4 else None
    
    success = create_karaoke_video(json_file, bg_image, out_video, audio)
    sys.exit(0 if success else 1)
