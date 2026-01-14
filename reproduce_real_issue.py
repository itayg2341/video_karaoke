import json
import time
import numpy as np
from PIL import Image, ImageDraw, ImageFont

# Load the full dataset
with open('lyrics.json', 'r') as f:
    lyrics_data = json.load(f)

print(f"Loaded lyrics data: {len(lyrics_data['segments'])} segments")
print(f"Total duration: {lyrics_data['duration']} seconds")

# Simulate the exact processing logic from app.py
def simulate_frame_processing():
    duration = lyrics_data["duration"]
    fps = 24
    total_frames = int(duration * fps)
    
    # Create dummy background
    bg_array = np.zeros((1080, 1920, 3), dtype=np.uint8)
    
    print(f"Processing {total_frames} frames at {fps} fps...")
    
    # Simulate the exact nested loop structure from app.py
    start_time = time.time()
    
    for frame_idx in range(total_frames):
        if frame_idx % 100 == 0:
            current_time = time.time()
            elapsed = current_time - start_time
            print(f"  Frame {frame_idx}/{total_frames} - {elapsed:.2f}s")
        
        current_time = frame_idx / fps
        words_to_show = []
        
        # This is the expensive nested loop from the original code
        for segment in lyrics_data["segments"]:
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
        
        # Simulate frame processing (without actual drawing)
        frame = bg_array.copy()
        # In real app: draw_lyrics_on_frame would be called here
        
        # Simulate frame storage
        # frames.append(frame)  # This would consume huge memory
    
    end_time = time.time()
    total_time = end_time - start_time
    
    print(f"✓ Processing completed in {total_time:.2f} seconds")
    print(f"  Average time per frame: {total_time/total_frames:.4f} seconds")
    print(f"  Estimated memory for frames: {(total_frames * 1080 * 1920 * 3) / (1024**3):.1f} GB")
    
    return total_time

# Run the simulation
total_time = simulate_frame_processing()

# Calculate the severity of the performance issue
if total_time > 60:
    severity = "CRITICAL"
elif total_time > 30:
    severity = "HIGH"
elif total_time > 10:
    severity = "MEDIUM"
else:
    severity = "LOW"

print(f"\n[{severity}] Performance Issue Detected:")
print(f"- Total processing time: {total_time:.1f} seconds")
print(f"- This is O(n²) complexity: O(frames × segments × words)")
print(f"- Memory usage would be prohibitive for full video")
